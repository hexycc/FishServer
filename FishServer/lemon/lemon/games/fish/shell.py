#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-03-03

import re
from props import FishProps
from account import FishAccount
from sdk.const import Const
from sdk.modules.entity import Entity
from sdk.modules.account import Account
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Tool
from framework.entity.msgpack import MsgPack
from framework.entity.const import Message
from framework.entity.manager import TaskManager


class FishShell(object):
    def __init__(self):
        self.json_path = {
            # gm
            '/v1/shell/query/overview': self.query_overview,
            '/v1/shell/gm/reward/vip': self.gm_reward_vip,
            '/v1/shell/gm/reward/card': self.gm_reward_card,
            '/v1/shell/gm/reward/egg': self.gm_reward_egg,
            '/v1/shell/gm/pool/pump': self.gm_pool_pump,
            '/v1/shell/gm/exchange/phone': self.gm_exchange_phone,
            '/v1/shell/gm/account/block': self.gm_account_block,
            '/v1/shell/gm/notice/global': self.gm_notice_global,
            '/v1/shell/query/chip/pump': self.query_chip_pump,
            '/v1/shell/query/history/phone': self.query_history_phone,
            '/v1/shell/query/chip/consume': self.query_chip_consume,
            '/v1/shell/query/chip/produce': self.query_chip_produce,
            '/v1/shell/query/diamond/consume': self.query_diamond_consume,
            '/v1/shell/query/diamond/produce': self.query_diamond_produce,
            '/v1/shell/query/props/egg/fall': self.query_egg_fall,
            '/v1/shell/query/shot': self.query_shot,
            '/v1/shell/query/raffle': self.query_raffle,
            '/v1/shell/query/chip/carrying': self.query_carrying,
            '/v1/shell/query/user/info': self.query_user_info,
            '/v1/shell/query/pay/detail': self.query_pay_detail,
        }

    def query_overview(self, gid, mi, request):
        kvs = Context.Stat.get_daily_data(gid)
        out_chip_pump = 0
        out_chip, in_chip = 0, 0
        in_diamond, out_diamond = 0, 0
        fall_egg, shot_times = 0, 0
        new_user_count, login_user_count = 0, 0
        today_pay_total = 0
        for k, v in kvs.iteritems():
            if k.startswith('in.chip.'):
                in_chip += int(v)
            elif k.startswith('out.chip.'):
                if (k.startswith('out.chip.pump.') or k.startswith('out.chip.buff.pump.') or
                        k.startswith('out.chip.red.pump.')):
                    out_chip_pump += int(v)
                else:   # pump 已经被game.shot.bullet包含
                    out_chip += int(v)
            elif k.startswith('in.diamond.'):
                in_diamond += int(v)
            elif k.startswith('out.diamond.'):
                out_diamond += int(v)
            elif k.startswith('shot.times.'):
                shot_times += int(v)
            elif k.endswith('.new.user.count'):
                new_user_count += int(v)
            elif k.endswith('.login.user.count'):
                login_user_count += int(v)
            elif k.endswith('.new.pay.user.pay_total'):
                pass
            elif k.endswith('.pay.user.pay_total'):
                today_pay_total += int(v)
            elif re.match(r'in\.props\.21[1234]\.fish\.fall\.', k):
                fall_egg += int(v)

        room_types = (201, 202, 203)

        # pool.chip
        pool_chip = []
        for room_type in room_types:
            fields = ['pool.shot.%d' % room_type, 'pool.reward.%d' % room_type,
                      'out.chip.pump.%d' % room_type, 'official.macro.control.%d' % room_type]
            _shot, _reward, _pump, _control = Context.RedisMix.hash_mget('game.%d.info.hash' % gid, *fields)
            _shot = Tool.to_int(_shot, 0)
            _reward = Tool.to_int(_reward, 0)
            _pump = Tool.to_int(_pump, 0)
            _control = Tool.to_int(_control, 0)
            pool_chip.append(_shot - _pump - _reward + _control)

        # red.pool.chip
        _shot, _reward, _pump = Context.RedisMix.hash_mget('game.%d.info.hash' % gid, 'red.pool.shot.203',
                                                           'red.pool.reward.203', 'out.chip.red.pump.203')
        _shot = Tool.to_int(_shot, 0)
        _reward = Tool.to_int(_reward, 0)
        _pump = Tool.to_int(_pump, 0)
        red_pool_chip = _shot - _pump - _reward

        carrying_volume, login_carrying_volume = 0, 0
        if 'carrying.volume.chip' in kvs:
            carrying_volume = int(kvs['carrying.volume.chip'])
        if 'login.carrying.volume.chip' in kvs:
            login_carrying_volume = int(kvs['login.carrying.volume.chip'])
        # online
        total, online_list = 0, []
        onlines = Context.Online.get_online(gid, *room_types)
        for _online in onlines:
            _online = Tool.to_int(_online, 0)
            online_list.append(_online)

        # total
        kvs = Context.RedisMix.hash_getall('game.%d.info.hash' % gid)
        user_count, pay_user, pay_total = 0, 0, 0
        for k, v in kvs.iteritems():
            if k.endswith('.new.user.count'):
                user_count += int(v)
            elif k.endswith('.pay.user.count'):
                pay_user += int(v)
            elif k.endswith('.pay.user.pay_total'):
                pay_total += int(v)

        param = {
            'total': {
                'user.count': user_count,
                'pay.user.count': pay_user,
                'pay.total': pay_total
            },
            'today': {
                'new.user.count': new_user_count,
                'login.user.count': login_user_count,
                'pay.total': today_pay_total,
                'out.chip.pump': out_chip_pump,
                'out.chip': out_chip,
                'in.chip': in_chip,
                'out.diamond': out_diamond,
                'in.diamond': in_diamond,
                'online': online_list,
                'fall.egg': fall_egg,
                'shot.times': shot_times,
                'pool.chip': pool_chip,
                'red.pool.chip': red_pool_chip,
                'carrying.volume': carrying_volume,
                'login.carrying.volume': login_carrying_volume
            }
        }
        return MsgPack(0, param)

    def gm_reward_vip(self, gid, mi, request):
        uid = mi.get_param('userId')
        rmb = mi.get_param('rmb')
        if not isinstance(rmb, int):
            return MsgPack.Error(0, 1, 'int please')

        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 2, 'not exist')

        if rmb < 0:
            pay_total = Context.Data.get_game_attr_int(uid, gid, 'pay_total', 0)
            if pay_total < -rmb:
                return MsgPack.Error(0, 3, 'too much')

        final = FishProps.incr_pay(uid, gid, rmb, 'gm.reward')
        level = FishAccount.get_vip_level(uid, gid, final)
        mo = MsgPack(0)
        mo.set_param('level', level)
        mo.set_param('pay_total', final)
        return mo

    def gm_reward_card(self, gid, mi, request):
        uid = mi.get_param('userId')
        days = mi.get_param('days')
        if days <= 0:
            return MsgPack.Error(0, 1, 'error days')

        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 2, 'not exist')

        state, days = FishProps.incr_vip(uid, gid, days, 'gm.reward')
        mo = MsgPack(0)
        mo.set_param('days', days)
        return mo

    def gm_reward_egg(self, gid, mi, request):
        uid = mi.get_param('userId')
        _id = mi.get_param('id')
        _count = mi.get_param('count')
        if _id not in (201, 202, 203, 204, 205, 211, 212, 213, 214, 215, 216, 217, 218, 219):
            return MsgPack.Error(0, 1, 'error id')

        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 3, 'user not exist')

        real, final = FishProps.incr_props(uid, gid, _id, _count, 'gm.reward')
        mo = MsgPack(0)
        mo.set_param('delta', real)
        mo.set_param('id', _id)
        mo.set_param('count', final)
        return mo

    def gm_pool_pump(self, gid, mi, request):
        delta = mi.get_param('delta')
        assert isinstance(delta, int)
        room_type = mi.get_param('room_type')
        assert room_type in (201, 202, 203)
        final = Context.RedisMix.hash_incrby('game.%d.info.hash' % gid, 'official.macro.control.%d' % room_type, delta)
        fields = ['pool.shot.%d' % room_type, 'pool.reward.%d' % room_type, 'out.chip.pump.%d' % room_type]
        shot, reward, pump = Context.RedisMix.hash_mget('game.%d.info.hash' % gid, *fields)
        shot = Tool.to_int(shot, 0)
        reward = Tool.to_int(reward, 0)
        pump = Tool.to_int(pump, 0)
        mo = MsgPack(0)
        mo.set_param('delta', delta)
        mo.set_param('room_type', room_type)
        mo.set_param('pool', shot - pump - reward + final)
        return mo

    def gm_exchange_phone(self, gid, mi, request):
        uid = mi.get_param('userId')
        seq = mi.get_param('seq')
        state = Context.RedisCluster.hash_get_int(uid, 'history:%d:%d' % (gid, uid), seq)
        if state is None:
            return MsgPack.Error(0, 1, 'error seq')
        if state == 1:
            return MsgPack.Error(0, 2, 'already exchange')
        Context.RedisCluster.hash_set(uid, 'history:%d:%d' % (gid, uid), seq, 1)
        return MsgPack(0)

    def gm_account_block(self, gid, mi, request):
        uid = mi.get_param('userId')
        odds = mi.get_param('odds')
        if odds is None:
            Context.Data.del_game_attrs(uid, gid, 'block')
        else:
            if not Context.UserAttr.check_exist(uid, gid):
                return MsgPack.Error(0, 1, 'not exist')
            if odds <= 0 or odds > 1:
                return MsgPack.Error(0, 2, 'odds limit (0, 1]')
            Context.Data.set_game_attr(uid, gid, 'block', odds)
        return MsgPack(0)

    def gm_notice_global(self, gid, mi, request):
        led = mi.get_param('led')
        start = mi.get_param('start')
        end = mi.get_param('end')
        now_ts = Time.current_ts()
        if now_ts > end:
            return MsgPack(0)
        Context.RedisCache.hash_mset('global.notice', 'led', led, 'start', start, 'end', end)
        if now_ts >= start:
            self._do_notice(led, end)
            return MsgPack(0)
        TaskManager.set_timeout(self.do_notice, start-now_ts, led, end)
        return MsgPack(0)

    def do_notice(self, led, end):
        TaskManager.add_simple_task(self._do_notice, led, end)

    def _do_notice(self, led, end):
        now_ts = Time.current_ts()
        mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
        mo.set_param('global', {'list': [led], 'end': end, 'now_ts': now_ts})
        Context.GData.broadcast_to_system(mo)

    def query_history_phone(self, gid, mi, request):
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        uid_seq_map, all_seq_list = {}, []
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            records = Context.RedisStat.hash_getall('history:%d:%s' % (gid, fmt))
            for seq, uid in records.iteritems():
                if uid not in uid_seq_map:
                    uid_seq_map[uid] = []
                uid_seq_map[uid].append(int(seq))
                all_seq_list.append(int(seq))
            start_day = Time.next_days(start_day)

        _list = []
        if all_seq_list:
            seq_record_map = Context.RedisMix.hash_mget_as_dict('game.%d.exchange.record' % gid, *all_seq_list)
            for uid, seq_list in uid_seq_map.iteritems():
                states = Context.RedisCluster.hash_mget(uid, 'history:%d:%s' % (gid, uid), *seq_list)
                for seq, state in zip(seq_list, states):
                    if state is not None and seq in seq_record_map:
                        record = Context.json_loads(seq_record_map[seq])
                        if record['type'] == 'exchange' and record['to'] == 'phone':
                            record = {
                                'uid': int(uid),
                                'ts': record['ts'],
                                'count': record['count'],
                                'phone': record['phone'],
                                'state': int(state),
                                'seq': seq,
                            }
                            _list.append(record)

        mo = MsgPack(0)
        mo.set_param('exchange', _list)
        return mo

    def query_chip_pump(self, gid, mi, request):
        room_types = (201, 202, 203)
        fields = []
        for room_type in room_types:
            fields.append('out.chip.pump.%d' % room_type)
            fields.append('out.chip.buff.pump.%d' % room_type)
            fields.append('out.chip.red.pump.%d' % room_type)
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            chips = Context.Stat.get_day_data(gid, fmt, *fields)
            info = []
            for i in range(0, len(chips), 3):
                total = 0
                for j in range(3):
                    if chips[i + j]:
                        total += int(chips[i + j])
                info.append(total)
            mo.set_param(fmt, info)
            start_day = Time.next_days(start_day)
        return mo

    def query_chip_consume(self, gid, mi, request):
        room_types = (201, 202, 203)
        mini_games = (10002, 10003)
        fields = ['out.chip.attack']
        for room_type in room_types:
            fields.append('out.chip.game.shot.bullet.%d' % room_type)
        for game in mini_games:
            fields.append('out.chip.game.%d' % game)
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            chips = Context.Stat.get_day_data(gid, fmt, *fields)
            attack = Tool.to_int(chips[0], 0)
            info = []
            for chip in chips[1:]:
                if chip:
                    info.append(int(chip))
                else:
                    info.append(0)
            info[2] += attack
            mo.set_param(fmt, info)
            start_day = Time.next_days(start_day)
        return mo

    def query_chip_produce(self, gid, mi, request):
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            kvs = Context.Stat.get_day_data(gid, fmt)
            task_total, catch_total = 0, 0
            _kvs = {}
            for k, v in kvs.iteritems():
                if k.startswith('in.chip.'):
                    if k.startswith('in.chip.task.reward.'):
                        task_total += int(v)
                    elif k.startswith('in.chip.catch.fish.'):
                        catch_total += int(v)
                    else:
                        _kvs[k] = int(v)
            _kvs['in.chip.task.reward'] = task_total
            _kvs['in.chip.catch.fish'] = catch_total
            _kvs['in.chip.buy.product'] = int(kvs.get('in.chip.buy.product', 0))
            mo.set_param(fmt, _kvs)
            start_day = Time.next_days(start_day)
        return mo

    def query_diamond_consume(self, gid, mi, request):
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            kvs = Context.Stat.get_day_data(gid, fmt)
            _kvs, total = {}, 0
            for k, v in kvs.iteritems():
                if k.startswith('out.diamond.'):
                    if k.startswith('out.diamond.inner.buy.'):
                        k = 'out.diamond.buy.' + k[-3:]
                    elif k.startswith('out.diamond.table.buy.'):
                        k = 'out.diamond.buy.' + k[-3:]
                    if k in _kvs:
                        _kvs[k] += int(v)
                    else:
                        _kvs[k] = int(v)
                    total += int(v)
            _kvs['total'] = total
            mo.set_param(fmt, _kvs)
            start_day = Time.next_days(start_day)
        return mo

    def query_diamond_produce(self, gid, mi, request):
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            kvs = Context.Stat.get_day_data(gid, fmt)
            _kvs = {}
            total, task_total, fall_total = 0, 0, 0
            for k, v in kvs.iteritems():
                if k.startswith('in.diamond.'):
                    if k.startswith('in.diamond.task.reward.'):
                        task_total += int(v)
                    elif k.startswith('in.diamond.fish.fall.'):
                        fall_total += int(v)
                    else:
                        _kvs[k] = int(v)
                    total += int(v)
            _kvs['in.diamond.task.reward'] = task_total
            _kvs['in.diamond.fish.fall'] = fall_total
            _kvs['in.diamond.buy.product'] = int(kvs.get('in.diamond.buy.product', 0))
            _kvs['total'] = total
            mo.set_param(fmt, _kvs)
            start_day = Time.next_days(start_day)
        return mo

    def query_egg_fall(self, gid, mi, request):
        room_types = (201, 202, 203)
        props_ids = (211, 212, 213)
        fields = []
        for pid in props_ids:
            for room_type in room_types:
                fields.append('in.props.%d.fish.fall.%d' % (pid, room_type))

        cnt_fields = []
        for pid in props_ids:
            cnt_fields.append('user.count.get.props.%d' % pid)

        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            eggs = Context.Stat.get_day_data(gid, fmt, *fields)
            props_info = []
            for i in range(0, len(eggs), len(room_types)):
                fall = 0
                for j in range(len(room_types)):
                    if eggs[i+j]:
                        fall += int(eggs[i+j])
                props_info.append(fall)

            gets = Context.Stat.get_day_data(gid, fmt, *cnt_fields)
            get_total = 0
            for cnt in gets:
                if cnt:
                    get_total += int(cnt)
            mo.set_param(fmt, {'fall': props_info, 'get': get_total})
            start_day = Time.next_days(start_day)
        return mo

    def query_shot(self, gid, mi, request):
        room_types = (201, 202, 203)
        fields = []
        for room_type in room_types:
            fields.append('shot.times.%d' % room_type)
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            values = Context.Stat.get_day_data(gid, fmt, *fields)
            info = []
            for v in values:
                if v:
                    info.append(int(v))
                else:
                    info.append(0)
            mo.set_param(fmt, info)
            start_day = Time.next_days(start_day)
        return mo

    def query_raffle(self, gid, mi, request):
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        eggs = (211, 212, 213, 214)
        fileds = ['in.chip.bonus.raffle', 'in.diamond.bonus.raffle', 'in.coupon.bonus.raffle']
        for egg in eggs:
            fileds.append('in.props.%d.bonus.raffle' % egg)
        mo = MsgPack(0)
        while start_day <= end_day:
            kvs = {}
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            values = Context.Stat.get_day_data(gid, fmt, *fileds)
            kvs['chip'] = Tool.to_int(values[0], 0)
            kvs['diamond'] = Tool.to_int(values[1], 0)
            kvs['coupon'] = Tool.to_int(values[2], 0)
            egg_list = []
            for egg in values[3:]:
                egg_list.append(Tool.to_int(egg, 0))
            kvs['egg'] = egg_list
            mo.set_param(fmt, kvs)
            start_day = Time.next_days(start_day)
        return mo

    def query_carrying(self, gid, mi, request):
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            _login, _total = Context.Stat.get_day_data(gid, fmt, 'login.carrying.volume.chip', 'carrying.volume.chip')
            _login = Tool.to_int(_login, 0)
            _total = Tool.to_int(_total, 0)
            mo.set_param(fmt, {'carrying': _login, 'total': _total})
            start_day = Time.next_days(start_day)
        return mo

    def query_user_info(self, gid, mi, request):
        uid = mi.get_param('userId')
        user_attrs = ['createTime', 'deviceId', 'nick', 'idType', 'userName', 'channel', 'platform']
        kvs = Context.Data.get_attrs_dict(uid, user_attrs)
        game_attrs = ['pay_total', 'session_login', 'exp', 'barrel_level', 'chip', 'diamond', 'in_chip', 'out_chip']
        _kvs = Context.Data.get_game_attrs_dict(uid, gid, game_attrs)
        kvs.update(_kvs)

        kvs['chip'] = int(kvs.get('chip', 0))
        kvs['in_chip'] = int(kvs.get('in_chip', 0))
        kvs['out_chip'] = int(kvs.get('out_chip', 0))
        kvs['diamond'] = int(kvs.get('diamond', 0))

        dt = Time.str_to_datetime(kvs['createTime'], '%Y-%m-%d %X.%f')
        kvs['createTime'] = Time.datetime_to_str(dt, '%Y-%m-%d %X')

        dt = Time.str_to_datetime(kvs['session_login'], '%Y-%m-%d %X.%f')
        kvs['session_login'] = Time.datetime_to_str(dt, '%Y-%m-%d %X')

        if int(kvs['idType']) == 13:
            kvs['phone'] = kvs['userName']

        kvs['pay_total'] = int(kvs.get('pay_total', 0))
        kvs['vip_level'] = FishAccount.get_vip_level(uid, gid, pay_total=int(kvs['pay_total']))

        exp = int(kvs['exp'])
        kvs['level'], _ = FishAccount.get_exp_info(uid, gid, exp=exp)
        barrel_level = int(kvs['barrel_level'])
        kvs['barrel_multiple'] = FishAccount.trans_barrel_level(gid, barrel_level)

        l = (201, 202, 203, 204, 205, 211, 212, 213, 214, 215, 216, 217, 218, 219)
        _list = FishProps.get_props_list(uid, gid, l)
        props_map = dict(_list)
        props_list = []
        for i in l:
            count = props_map.get(i, 0)
            props_list.append(count)
        kvs['props'] = props_list
        mo = MsgPack(0)
        mo.update_param(kvs)
        return mo

    def query_pay_detail(self, gid, mi, request):
        conf = Context.Configure.get_game_item_json(gid, 'product.config')
        pids = []
        for pid in conf.iterkeys():
            pids.append('product_' + pid)
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            timess = Context.Stat.get_day_data(gid, fmt, *pids)
            kvs = {'product_100646': 0, 'product_100710': 0}
            for k, v in zip(pids, timess):
                pid = k.replace('product_', '')
                if pid in ('100646', '100647', '100648', '100649', '100650', '100651',
                           '100652', '100653', '100654', '100655'):
                    kvs['product_100646'] += Tool.to_int(v, 0)
                elif pid in ('100710', '100711', '100712', '100713', '100714', '100715', '100716'):
                    kvs['product_100710'] += Tool.to_int(v, 0)
                else:
                    kvs[k] = Tool.to_int(v, 0)
            mo.set_param(fmt, kvs)
            start_day = Time.next_days(start_day)
        return mo


FishShell = FishShell()
