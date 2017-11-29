#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-12-17

import random
from task import FishTask
from const import Message
from rank import FishRank
from props import FishProps
from account import FishAccount
from framework.context import Context
from framework.util.tool import Tool
from framework.util.tool import Time
from framework.util.tool import Algorithm
from framework.entity.msgpack import MsgPack
from lemon.entity.gametimer import GameTimer

import time

class FishEntity(object):
    def __init__(self):
        from lemon.tasklet.entity import EntityTasklet
        self.timer = GameTimer(EntityTasklet)

    def onMessage(self, cmd, uid, gid, mi):
        mo = None
        if cmd == Message.MSG_SYS_ROOM_LIST | Message.ID_REQ:
            self.on_room_list(uid, gid, mi)
        elif cmd == Message.MSG_SYS_RANK_LIST | Message.ID_REQ:
            mo = FishRank.get_ranks(uid, gid, mi)
        elif cmd == Message.MSG_SYS_BENEFIT | Message.ID_REQ:
            mo = self.on_benefit(uid, gid, mi)
        elif cmd == Message.MSG_SYS_SIGN_IN | Message.ID_REQ:
            mo = self.on_sign_in(uid, gid, mi)
        elif cmd == Message.MSG_SYS_CONFIG | Message.ID_REQ:
            mo = self.on_get_config(uid, gid, mi)
        elif cmd == Message.MSG_SYS_PROPS_LIST | Message.ID_REQ:
            mo = self.on_props_list(uid, gid, mi)
        elif cmd == Message.MSG_SYS_USE_PROPS | Message.ID_REQ:
            mo = self.on_use_props(uid, gid, mi)
        elif cmd == Message.MSG_SYS_RAFFLE | Message.ID_REQ:
            mo = self.on_raffle(uid, gid, mi)
        elif cmd == Message.MSG_SYS_TASK_LIST | Message.ID_REQ:
            mo = FishTask.on_task_list(uid, gid, mi)
        elif cmd == Message.MSG_SYS_CONSUME_TASK | Message.ID_REQ:
            mo = FishTask.on_consume_task(uid, gid, mi)
        elif cmd == Message.MSG_SYS_PRESENT | Message.ID_REQ:
            mo = self.on_present(uid, gid, mi)
        elif cmd == Message.MSG_SYS_EXCHANGE | Message.ID_REQ:
            mo = self.on_exchange(uid, gid, mi)
        elif cmd == Message.MSG_SYS_INNER_BUY | Message.ID_REQ:
            mo = self.on_inner_buy(uid, gid, mi)
        elif cmd == Message.MSG_SYS_UP_BARREL | Message.ID_REQ:
            mo = self.on_up_barrel(uid, gid, mi)
        elif cmd == Message.MSG_SYS_RESOLVE_STONE | Message.ID_REQ:
            mo = self.on_resolve_stone(uid, gid, mi)
        elif cmd == Message.MSG_SYS_CONSUME_CDKEY | Message.ID_REQ:
            mo = self.on_consume_cdkey(uid, gid, mi)

        if isinstance(mo, MsgPack):
            Context.GData.send_to_connect(uid, mo)

    def on_sign_in(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_SIGN_IN | Message.ID_ACK)
        conf = Context.Configure.get_game_item_json(gid, 'login.reward')
        if not conf:
            Context.Log.error('miss config')
            return mo.set_error(1, 'miss config')

        now_day, last_login, ns_login = FishAccount.get_login_info(uid, gid)
        if now_day == last_login:
            return mo.set_error(2, 'already sign in')
        elif now_day == last_login + 1:  # 连续登陆
            ns_login += 1
        else:
            ns_login = 0
        FishAccount.set_login_info(uid, gid, now_day, ns_login)
        vip_level = FishAccount.get_vip_level(uid, gid)

        if vip_level:
            conf = conf['vip']
        else:
            conf = conf['common']
        reward = conf[ns_login % len(conf)]
        real, final = Context.UserAttr.incr_chip(uid, gid, reward, 'signin.reward')

        pipe_args = []
        delta_chip = real
        # 领取月卡奖励
        success, left_days = FishProps.use_vip(uid, gid)
        if success:
            conf = Context.Configure.get_game_item_json(gid, 'month.card.reward')
            reward = FishProps.issue_rewards(uid, gid, conf, 'month.card.reward')
            if 'diamond' in reward:
                mo.set_param('diamond', reward['diamond'])
                pipe_args.append('login.carrying.volume.diamond')
                pipe_args.append(reward['reward']['diamond'])
            if 'coupon' in reward:
                mo.set_param('coupon', reward['coupon'])
                pipe_args.append('login.carrying.volume.coupon')
                pipe_args.append(reward['reward']['coupon'])
            if 'chip' in reward:
                final = reward['chip']
                delta_chip += reward['reward']['chip']

        pipe_args.append('login.carrying.volume.chip')
        pipe_args.append(delta_chip)
        pipe_args.append('carrying.volume.chip')
        pipe_args.append(delta_chip)
        Context.Daily.mincr_daily_data(uid, gid, *pipe_args)

        if vip_level:
            vip_conf = Context.Configure.get_game_item_json(gid, 'vip.config')[vip_level-1]
            stone_count = vip_conf.get('stone', 0)
            if stone_count:
                FishProps.mincr_props(uid, gid, 'vip_reward', 215, stone_count, 216,
                                      stone_count, 217, stone_count, 218, stone_count)
            chip_num = vip_conf.get('chip')
            if chip_num and chip_num > final:
                add_num = chip_num - final
                real, final = Context.UserAttr.incr_chip(uid, gid, add_num, 'vip_reward')
        if final:
            mo.set_param('chip', final)
        return mo

    def on_room_list(self, uid, gid, mi):
        room_config = Context.Configure.get_room_config(gid)
        if not room_config:
            Context.Log.error(uid, 'req room list, but no config fetch')
            return False

        conf = Context.copy_json_obj(room_config)
        mo = MsgPack(Message.MSG_SYS_ROOM_LIST | Message.ID_ACK)
        mo.set_param('room_list', conf)
        return Context.GData.send_to_connect(uid, mo)

    def on_benefit(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_BENEFIT | Message.ID_ACK)
        conf = Context.Configure.get_game_item_json(gid, 'benefit.config')
        total_times = len(conf['reward'])
        benefit_times, bankrupt_ts = Context.Daily.get_daily_data(uid, gid, 'benefit_times', 'bankrupt_ts')
        benefit_times = Tool.to_int(benefit_times, 0)
        if benefit_times >= total_times:
            return mo.set_error(1, 'none')
        now_ts = Time.current_ts()
        if not bankrupt_ts or int(bankrupt_ts) > now_ts:
            return mo.set_error(2, 'wait')

        result = Context.Daily.issue_benefit(uid, gid)
        if not result:
            return mo.set_error(3, 'failed')

        Context.Daily.del_daily_data(uid, gid, 'bankrupt_ts')
        mo.update_param(result)
        return mo

    def on_get_config(self, uid, gid, mi):
        which = mi.get_param('which')
        if isinstance(which, (str, unicode)):
            which = [which]

        mo = MsgPack(Message.MSG_SYS_CONFIG | Message.ID_ACK)
        for name in which:
            if name == 'vip':
                conf = self.get_vip_config(uid, gid)
            elif name == 'shop':
                conf = self.get_shop_config(uid, gid)
            elif name == 'raffle':
                conf = self.get_raffle_config(uid, gid)
            elif name == 'props':
                conf = FishProps.get_props_config(gid)
            elif name == 'unlock':
                conf = self.get_unlock_config(uid, gid)
            elif name == 'barrel':
                conf = self.get_barrel_config(uid, gid)
            elif name == 'exchange':
                conf = self.get_exchange_config(uid, gid)
            elif name == 'benefit':
                conf = self.get_benefit_config(uid, gid)
            elif name == 'html':
                conf = self.get_html_config(uid, gid)
            elif name == 'exp':
                conf = self.get_exp_config(uid, gid)
            elif name == 'upbrrel':
                conf = self.get_upbrrel_config(uid, gid)
            else:
                continue
            mo.set_param(name, conf)
        return mo

    def get_vip_config(self, uid, gid):
        vip = Context.Configure.get_game_item_json(gid, 'vip.config')
        return vip

    def get_shop_config(self, uid, gid):
        product_config = Context.Configure.get_game_item_json(gid, 'product.config')
        shop_config = Context.Configure.get_game_item_json(gid, 'shop.config')
        if not shop_config or not product_config:
            return {}

        product_config = Context.copy_json_obj(product_config)
        attrs = list(shop_config['chip'])
        attrs.extend(shop_config['first'])
        fileds = []
        for attr in attrs:
            fileds.append('product_%s' % attr)
            fileds.append('reset_%s' % attr)

        counts = Context.Data.get_game_attrs(uid, gid, fileds)
        kvs = Tool.make_dict(attrs, counts[::2])
        reset_kvs = Tool.make_dict(attrs, counts[1::2])
        info = {}
        for k, pids in shop_config.iteritems():
            group = []
            for pid in pids:
                product = product_config[pid]
                del product['name']
                if k in ('chip', 'diamond'):
                    del product['content']
                if 'first' in product:
                    del product['first']
                if k == 'first' and kvs[pid] is None:
                    product['first'] = 1
                elif k == 'chip' and (kvs[pid] is None or reset_kvs[pid]):
                    product['first'] = 1
                product['id'] = pid
                group.append(product)
            info[k] = group
        info['card'] = info['card'][0]      # 只要一个
        if not counts[-2]:
            info['first'] = info['first'][1]  # 只要一个

        return info

    def get_raffle_config(self, uid, gid):
        raffle_config = Context.Configure.get_game_item_json(gid, 'raffle.config')
        raffle_config = Context.copy_json_obj(raffle_config)
        loop_config = raffle_config['loop']
        raffle_config = raffle_config['config']
        for item in raffle_config:
            for i, reward in enumerate(item['reward']):
                item['reward'][i] = reward[1]

        class_pool, loop_times = Context.Daily.get_daily_data(uid, gid, 'fake.bonus.count', 'bonus.loop.times')
        class_pool = Tool.to_int(class_pool, 0)
        loop_times = Tool.to_int(loop_times, 0)
        if loop_times > len(loop_config) - 1:
            this_count = loop_config[-1]
        else:
            this_count = loop_config[loop_times]
        info = {'config': raffle_config}
        bonus_pool = Context.Data.get_game_attr_int(uid, gid, 'bonus_pool', 0)
        info['pool'] = bonus_pool
        info['progress'] = [class_pool, this_count]
        return info

    def get_upbrrel_config(self, uid, gid):
        """
        发一个
        """
        config = Context.Configure.get_game_item_json(gid, 'barrel.unlock.config')
        barrel_level = Context.Data.get_game_attr_int(uid, gid, 'barrel_level', 1)

        level = barrel_level + 1
        conf = {}
        if 36 < level <= 54:
            conf = config[level-1]
        return conf

    def get_unlock_config(self, uid, gid):
        """
        前端显示5个
        """
        config = Context.Configure.get_game_item_json(gid, 'barrel.unlock.config')
        barrel_level = Context.Data.get_game_attr_int(uid, gid, 'barrel_level', 1)

        start = barrel_level - 2
        end = start + 5
        if start < 1:
            conf = config[1:6]
        elif end >= 36:
            conf = config[31:38]
        else:
            conf = config[start:end]

        return conf

    def get_barrel_config(self, uid, gid):
        return Context.Configure.get_game_item_json(gid, 'barrel.level.config')

    def get_exchange_config(self, uid, gid):
        return Context.Configure.get_game_item_json(gid, 'exchange.config')

    def get_benefit_config(self, uid, gid):
        conf = Context.Configure.get_game_item_json(gid, 'benefit.config')
        benefit_times, bankrupt_ts = Context.Daily.get_daily_data(uid, gid, 'benefit_times', 'bankrupt_ts')
        benefit_times = int(benefit_times) if benefit_times else 0
        _info = {
            'which': benefit_times,      # 已领取几次
            'conf': conf['reward']
        }
        if bankrupt_ts is not None:
            now_ts = Time.current_ts()
            bankrupt_ts = int(bankrupt_ts)
            if now_ts > bankrupt_ts:
                _info['wait'] = 0
            else:
                _info['wait'] = bankrupt_ts - now_ts
        return _info

    def on_props_list(self, uid, gid, mi):
        props_list = FishProps.get_props_list(uid, gid)
        info = {
            'c': Context.UserAttr.get_chip(uid, gid, 0),
            'd': Context.UserAttr.get_diamond(uid, gid, 0),
            'o': Context.UserAttr.get_coupon(uid, gid, 0)
        }
        if props_list:
            info['p'] = props_list

        # 升级礼包
        conf = Context.Configure.get_game_item_json(gid, 'exp.level.reward')
        level, _ = FishAccount.get_exp_info(uid, gid)
        if level < len(conf):
            info['up'] = FishProps.convert_reward(conf[level])

        mo = MsgPack(Message.MSG_SYS_PROPS_LIST | Message.ID_ACK)
        mo.update_param(info)
        return mo

    def on_use_props(self, uid, gid, mi):
        _id = mi.get_param('id')
        _count = mi.get_param('count')
        mo = MsgPack(Message.MSG_SYS_USE_PROPS | Message.ID_ACK)
        if _id not in [FishProps.PROP_EGG_BRONZE, FishProps.PROP_EGG_SILVER,
                       FishProps.PROP_EGG_GOLD, FishProps.PROP_EGG_COLOR]:
            return mo.set_error(1, 'can not use')

        if not isinstance(_count, int) or _count <= 0:
            return mo.set_error(2, 'count error')

        conf = FishProps.get_config_by_id(gid, _id)
        if not conf:
            Context.Log.error('not found props:', uid, gid, _id, _count)
            return mo.set_error(4, 'not found props')

        real, final = FishProps.incr_props(uid, gid, _id, -_count, 'entity.use')
        if real != -_count:
            return mo.set_error(3, 'not enough')

        if _count == 1:
            reward = conf['content']
        else:
            reward = FishProps.merge_reward(*[conf['content']] * _count)
        reward = Context.copy_json_obj(reward)
        reward = self.deal_reward(reward)
        reward = FishProps.issue_rewards(uid, gid, reward, 'entity.use')
        reward = FishProps.convert_reward(reward)
        mo.update_param(reward)
        return mo

    def deal_reward(self, rewards):
        if not rewards:
            return {}
        props = rewards.get('props')
        if not props:
            return rewards

        _props = []
        for prop in props:
            count = prop['count']
            if 'dRate' in prop:
                count = 0
                for _ in range(prop['count']):
                    if random.random() <= prop.get('dRate'):
                        count += 1
            if count:
                _props.append({'id': prop['id'], 'count': count})
        rewards['props'] = _props
        return rewards

    def on_raffle(self, uid, gid, mi):
        _id = mi.get_param('i')
        _button = mi.get_param('bt')
        mo = MsgPack(Message.MSG_SYS_RAFFLE | Message.ID_ACK)
        raffle_config = Context.Configure.get_game_item_json(gid, 'raffle.config')
        raffle_config = Context.copy_json_obj(raffle_config)
        loop_config = raffle_config['loop']
        raffle_config = raffle_config['config']
        class_pool, loop_times = Context.Daily.get_daily_data(uid, gid, 'fake.bonus.count', 'bonus.loop.times')
        class_pool = Tool.to_int(class_pool, 0)
        loop_times = Tool.to_int(loop_times, 0)
        if loop_times > len(loop_config) - 1:
            this_count = loop_config[-1]
        else:
            this_count = loop_config[loop_times]
        if class_pool < this_count:
            return mo.set_error(1, 'lack fish')

        for item in raffle_config:
            if item['id'] == _id:
                bonus_pool = Context.Data.get_game_attr_int(uid, gid, 'bonus_pool', 0)
                if bonus_pool < item['limit']:
                    return mo.set_error(2, 'lack chip')
                # 发放奖励
                index, which = Algorithm.choice_by_ratio(item['reward'], 10000, func=lambda l: l[0])
                reward = FishProps.issue_rewards(uid, gid, which[1], 'bonus.raffle')
                mo.set_param('bt', _button)
                mo.set_param('i', index + 1)
                rw = FishProps.convert_reward(reward)
                mo.update_param(rw)
                # 重置数据
                pipe_args = ['fake.bonus.count', -class_pool, 'bonus.loop.times', 1]
                Context.Daily.mincr_daily_data(uid, gid, *pipe_args)
                Context.Data.hincr_game(uid, gid, 'bonus_pool', -bonus_pool)
                self.__pub_raffle_led(uid, gid, item['name'], reward)
                return mo

        return mo.set_error(3, 'error id')

    def __pub_raffle_led(self, uid, gid, level, reward_info):
        if 'reward' in reward_info:
            reward = reward_info['reward']
            name = None
            if 'chip' in reward:
                Context.Data.hincr_game(uid, gid, 'chip_pool', -reward['chip'])
            elif 'coupon' in reward:
                name = u'%d鱼券' % reward['coupon']
            elif 'diamond' in reward:
                name = u'%d钻石' % reward['diamond']
            elif 'props' in reward:
                props = reward['props']
                for one in props:
                    name = FishProps.get_props_desc(one['id'])
                    break
            if name:
                nick = Context.Data.get_attr(uid, 'nick')
                if nick:
                    led = u'恭喜%s玩家，在%s中抽中%s' % (nick.decode('utf-8'), level, name)
                    mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                    mo.set_param('game', {'list': [led], 'ts': Time.current_ts()})
                    Context.GData.broadcast_to_system(mo)

    def on_present(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_PRESENT | Message.ID_ACK)
        _id = mi.get_param('id')
        if not isinstance(_id, int):
            return mo.set_error(1, 'error param')
        _count = mi.get_param('count')
        if not isinstance(_count, int) or _count <= 0:
            return mo.set_error(2, 'error param')
        if _id not in [201, 202, 203, 204, 205, 211, 212, 213, 214, 215, 216, 217, 218, 219]:
            return mo.set_error(3, 'error id')
        ta = mi.get_param('ta')
        if ta < 0 or not Context.UserAttr.check_exist(ta, gid):
            return mo.set_error(4, 'error uid')
        conf = FishProps.get_config_by_id(gid, _id)
        if conf:
            if 'count' in conf:
                if _count % conf['count'] != 0:
                    return mo.set_error(5, 'error count')
            if 'present' in conf:
                pay_total = Context.Data.get_game_attr_int(uid, gid, 'pay_total', 0)
                if conf['present']['pay'] > pay_total:
                    return mo.set_error(7, 'pay limit')
            real, final = FishProps.incr_props(uid, gid, _id, -_count, 'present.props', ta=ta)
            if real != -_count:
                return mo.set_error(6, 'not enough')
            mo.set_param('id', _id)
            mo.set_param('count', final)
            FishProps.incr_props(ta, gid, _id, _count, 'present.props', ta=uid)
            return mo

        Context.Log.error('no props config found', _id)
        return mo.set_error(7, 'unknown')

    def on_exchange(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_EXCHANGE | Message.ID_ACK)
        _id = mi.get_param('id')
        if not isinstance(_id, int):
            return mo.set_error(1, 'error param')

        conf = Context.Configure.get_game_item_json(gid, 'exchange.config')
        if _id >= len(conf):
            return mo.set_error(1, 'error id')

        info = conf[_id]
        to_type = info['type']
        if to_type not in ('diamond', 'props', 'phone'):
            raise Exception(str(to_type) + '<----error type, please check config')

        real, final = Context.UserAttr.incr_coupon(uid, gid, -info['cost'], 'exchange.' + to_type)
        if real != -info['cost']:
            return mo.set_error(2, 'not enough')
        mo.set_param('coupon', final)
        record = {
            'uid': uid,
            'type': 'exchange',
            'ts': Time.current_ts(),
            'from': 'coupon',
            'to': to_type,
            'cost': info['cost'],
            'count': info['count'],
            'desc': info['desc']
        }
        if info['type'] == 'diamond':   # 兑换钻石
            real, final = Context.UserAttr.incr_diamond(uid, gid, info['count'], 'exchange.diamond')
            mo.set_param('diamond', final)
            state = 1
        elif info['type'] == 'props':   # 兑换道具
            real, final = FishProps.incr_props(uid, gid, info['id'], info['count'], 'exchange.props')
            mo.set_param('id', info['id'])
            mo.set_param('count', final)
            state = 1
            record['id'] = info['id']
        elif info['type'] == 'phone':
            state = 0
            record['phone'] = mi.get_param('phone')
        else:
            raise Exception('something error, please check config')

        seq_num = Context.RedisMix.hash_incrby('game.%d.info.hash' % gid, 'exchange.history.seq', 1)
        Context.RedisCluster.hash_set(uid, 'history:%d:%d' % (gid, uid), seq_num, state)

        record = Context.json_dumps(record)
        Context.RedisMix.hash_mset('game.%d.exchange.record' % gid, seq_num, record)
        fmt = Time.current_time('%Y-%m-%d')
        Context.RedisStat.hash_set('history:%d:%s' % (gid, fmt), seq_num, uid)
        return mo

    def on_inner_buy(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_INNER_BUY | Message.ID_ACK)
        _id = mi.get_param('id')
        if not isinstance(_id, int):
            return mo.set_error(1, 'error param')
        _count = mi.get_param('count')
        if not isinstance(_count, int) or _count <= 0:
            return mo.set_error(2, 'error param')
        if _id not in [201, 202, 203, 204, 205]:
            return mo.set_error(3, 'error id')
        conf = FishProps.get_config_by_id(gid, _id)
        if conf:
            if 'count' in conf:
                if _count % conf['count'] != 0:
                    return mo.set_error(5, 'error count')
            real, final = Context.UserAttr.incr_diamond(uid, gid, -conf['diamond'], 'inner.buy.%d' % _id)
            if real != -conf['diamond']:
                return mo.set_error(6, 'not enough')
            mo.set_param('diamond', final)
            real, final = FishProps.incr_props(uid, gid, _id, _count, 'inner.buy')
            mo.set_param('id', _id)
            mo.set_param('count', final)
            return mo

        Context.Log.error('no props config found', _id)
        return mo.set_error(7, 'unknown')

    def get_html_config(self, uid, gid):
        html_conf = Context.Configure.get_game_item_json(gid, 'html.config')
        return html_conf

    def get_exp_config(self, uid, gid):
        return Context.Configure.get_game_item_json(gid, 'exp.level')

    def on_product_deliver(self, uid, gid, mi):
        orderId = mi.get_param('orderId')
        productId = mi.get_param('productId')
        payType = mi.get_param('payType')
        channel = mi.get_param('channel')
        cost = mi.get_param('cost')
        param = {
            'orderId': orderId,
            'productId': productId,
            'payType': payType,
            'channel': channel,
            'cost': cost
        }
        Context.Log.report('product.issue: [%d, %d, %s, %s]' % (uid, gid, orderId, param))
        all_product = Context.Configure.get_game_item_json(gid, 'product.config')
        if productId not in all_product:
            Context.Log.error('productId not exist', orderId, productId, all_product)
            return MsgPack.Error(0, 1, 'no product found')

        shop_config = Context.Configure.get_game_item_json(gid, 'shop.config')

        pipe_args = ['product_%s' % productId, 1]
        times = Context.Data.hincr_game(uid, gid, 'product_%s' % productId, 1)

        # 记录充值相关字段
        pay_total = FishProps.incr_pay(uid, gid, cost, 'buy.product', orderId=orderId)
        today_pay_times, _ = Context.Daily.mincr_daily_data(uid, gid, 'pay_times', 1, 'pay_total', cost)

        is_reset_chance, is_first_double = False, False
        if productId in shop_config['chip']:
            if times == 1:
                is_first_double = True
            else:
                reset_choice = Context.Data.get_game_attr_int(uid, gid, 'reset_' + str(productId), 0)
                if reset_choice:
                    is_reset_chance = True

        product = all_product[productId]
        if is_reset_chance:  # reset chance
            reward = self.__rebate_reward(gid, pay_total, product['first'], channel)
            FishProps.issue_rewards(uid, gid, reward, 'buy.product', orderId=orderId, reset=1)
            Context.Data.del_game_attrs(uid, gid, 'reset_' + str(productId))
        elif is_first_double:
            reward = self.__rebate_reward(gid, pay_total, product['first'], channel)
            FishProps.issue_rewards(uid, gid, reward, 'buy.product', orderId=orderId, first=1)
        elif productId in shop_config['card']:
            state, days = FishProps.incr_vip(uid, gid, 30, 'buy.product', orderId=orderId)
            if state == 0:  # 今日未领取
                sign_in = Context.Daily.get_daily_data(uid, gid, 'sign_in')
                if sign_in:
                    success, left_days = FishProps.use_vip(uid, gid)
                    if success:
                        conf = Context.Configure.get_game_item_json(gid, 'month.card.reward')
                        FishProps.issue_rewards(uid, gid, conf, 'month.card.reward')
        else:
            reward = self.__rebate_reward(gid, pay_total, product['content'], channel)
            FishProps.issue_rewards(uid, gid, reward, 'buy.product', orderId=orderId)

        if today_pay_times == 1:      # today first pay
            pipe_args.append(channel + '.pay.user.count')
            pipe_args.append(1)
        pipe_args.append(channel + '.pay.user.pay_total')
        pipe_args.append(cost)
        pipe_args.append(channel + '.user.pay.times')
        pipe_args.append(1)

        if pay_total == cost:   # life first pay
            pipe_args.append(channel + '.new.pay.user.count')
            pipe_args.append(1)
            pipe_args.append('new_pay_user')
            pipe_args.append(1)
            new_pay_user = 1
        else:
            new_pay_user = Context.Daily.get_daily_data(uid, gid, 'new_pay_user')

        if new_pay_user:
            pipe_args.append(channel + '.new.pay.user.pay_total')
            pipe_args.append(cost)

        Context.Stat.mincr_daily_data(gid, *pipe_args)

        key = 'game.%d.info.hash' % gid
        pipe_args = []
        if pay_total == cost:
            pipe_args.append(channel + '.pay.user.count')
            pipe_args.append(1)

        pipe_args.append(channel + '.pay.user.pay_total')
        pipe_args.append(cost)
        pipe_args.append(channel + '.user.pay.times')
        pipe_args.append(1)
        Context.RedisMix.hash_mincrby(key, *pipe_args)

        self.__handle_pay_effect(uid, gid, cost, today_pay_times)

        return MsgPack(0, {'msg': u'已到货'})

    def __handle_pay_effect(self, uid, gid, cost, today_pay_times):
        try:
            conf = Context.Configure.get_game_item_json(gid, 'odds.addition.pay')
            if today_pay_times <= conf['total']:
                add_chip = int(cost * conf['multi'] * (1 - (today_pay_times - 1) * conf['damping']))
                if add_chip > 0:
                    Context.Daily.incr_daily_data(uid, gid, 'chip.pool', add_chip)
                    Context.Daily.incr_daily_data(uid, gid, 'common.chip.pool', int(add_chip * 0.33333))
        except Exception, e:
            Context.Log.exception()

    def __rebate_reward(self, gid, pay_total, reward, channel):
        reward = Context.copy_json_obj(reward)
        if 'chip' in reward:
            vip_config = Context.Configure.get_game_item_json(gid, 'vip.config')
            if vip_config:
                for item in reversed(vip_config):
                    if pay_total > item['pay'] and 'rebate' in item:
                        rebate = item['rebate']
                        reward['chip'] += int(reward['chip'] * rebate)
                        break

        return reward

    def on_up_barrel(self, uid, gid, mi):
        # 强化万倍炮
        # up type 1 石头 2 精华
        mo = MsgPack(Message.MSG_SYS_UP_BARREL | Message.ID_ACK)
        up_type = mi.get_param('up_ty')
        conf = Context.Configure.get_game_item_json(gid, 'barrel.unlock.config')
        if not conf:
            return mo.set_error(1, 'system error')

        next_level = Context.Data.get_game_attr_int(uid, gid, 'barrel_level', 1) + 1
        # if next_level > len(conf):
        if next_level <= 36 or next_level > 54:
            return mo.set_error(2, 'level error')
        level_conf = conf[next_level - 1]

        diamond_count = level_conf['diamond']
        real, final = Context.UserAttr.incr_diamond(uid, gid, -diamond_count, 'up.barrel')
        if real != -diamond_count:
            return mo.set_error(3, 'lack diamond')

        if up_type == 1:
            count = -level_conf['stone']
            if not FishProps.mincr_props(uid, gid, 'on_up_barrel', 215, count,
                                         216, count, 217, count, 218, count):
                Context.UserAttr.incr_diamond(uid, gid, diamond_count,
                                              'up.barrel.error')
                return mo.set_error(3, 'lack stone')
            res, gem = self.do_up_barrel(level_conf)
            if res:
                Context.Data.set_game_attr(uid, gid, 'barrel_level', next_level)
            else:
                FishProps.mincr_props(uid, gid, 'on_up_barrel.fail_reurn', 219, gem)
                mo.set_param('num', gem)
        elif up_type == 2:
            count = -level_conf['stone']
            count_gem = -level_conf['gem']
            if not FishProps.mincr_props(uid, gid, 'on_up_barrel', 215, count,
                                         216, count, 217, count, 218, count,
                                         219, count_gem):
                Context.UserAttr.incr_diamond(uid, gid, diamond_count, 'up.barrel.error')
                return mo.set_error(3, 'lack item')
            Context.Data.set_game_attr(uid, gid, 'barrel_level', next_level)
        else:
            return mo.set_error(4, 'type error')
        return mo

    def do_up_barrel(self, conf):
        if random.random() <= conf['ratio']:
            return 1, 0
        else:
            return 0, random.randint(conf['fail_gem'][0], conf['fail_gem'][1])

    def on_resolve_stone(self, uid, gid, mi):
        # 分解强化石
        mo = MsgPack(Message.MSG_SYS_RESOLVE_STONE | Message.ID_ACK)

        stone_id = mi.get_param('id')
        if stone_id not in [215, 216, 217, 218]:
            return mo.set_error(1, 'id error')
        conf = FishProps.get_config_by_id(gid, stone_id)
        count = -conf['count']
        if not FishProps.mincr_props(uid, gid, 'on_resolve_stone', stone_id, count):
            return mo.set_error(2, 'lack stone')
        gem_count = random.randint(conf['resolve'][0], conf['resolve'][1])
        FishProps.mincr_props(uid, gid, 'on_resolve_stone', 219, gem_count)
        mo.set_param('num', gem_count)
        return mo

    def on_consume_cdkey(self, uid, gid, mi):
        code = mi.get_param('code')
        imei = mi.get_param('imei')
        timestamp = (int(time.time()))
        # data = {'appId': 1002, 'code': code, 'userChannel': 0, 'imei': imei, 'userId': uid,'timestamp': timestamp ,'token':'asdsd'}
        data = 'code=' + str(code) + '&' + 'userId=' + str(uid) + '&' + 'timestamp=' + str(timestamp) + '&token=asdsd'
        cdkey_server_url = Context.Configure.get_game_item(gid, 'cdkey.server.url')
        Context.Log.info("cdkey_server_url:", cdkey_server_url)
        result = Context.WebPage.wait_for_json(cdkey_server_url, postdata=data)
        mo = MsgPack(Message.MSG_SYS_CONSUME_CDKEY | Message.ID_ACK)
        if result['result'] != 1:  # 错误
            mo.set_error(result['result'])
        else:
            try:
                Context.Log.info("desc:", result['desc'])
                reward = self.__convert_cdkey_desc(result['desc'])
                rewards = FishProps.issue_rewards(uid, gid, reward, 'cdkey.reward')
                _rewards = FishProps.convert_reward(rewards)
                mo.update_param(_rewards)
            except Exception, e:
                Context.Log.exception(uid, gid, result)
                return
        return mo

    def __convert_cdkey_desc(self, desc):
        # desc = Context.json_loads(desc)
        reward = {}
        if 'c' in desc:
            reward['chip'] = desc['c']
        if 'o' in desc:
            reward['coupon'] = desc['o']
        if 'd' in desc:
            reward['diamond'] = desc['d']
        if 'p' in desc:
            props = []
            for k, v in desc['p']:
                props.append({'id': k, 'count': v})
            reward['props'] = props
        return reward


FishEntity = FishEntity()
