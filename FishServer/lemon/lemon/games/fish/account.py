#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-12-28

from const import Message
from props import FishProps
from framework.util.tool import Time
from framework.util.tool import Tool
from framework.context import Context
from lemon.entity.account import Account
from framework.entity.msgpack import MsgPack


class FishAccount(Account):
    game_attrs = {
        'exp': 0,
        'barrel_level': 1,
        'barrel_skin': 1
    }
    auto_issue_benefit = False

    @classmethod
    def get_game_info(cls, uid, gid):
        is_new, kvs = cls.get_common_game_info(uid, gid)

        conf = Context.Configure.get_game_item_json(gid, 'barrel.unlock.config')
        kvs['barrel_multiple'] = conf[kvs['barrel_level'] - 1]['multiple']

        vip = cls.get_vip_info(uid, gid)
        if vip:
            kvs['vip'] = vip
        now_day, last_login, ns_login = cls.get_login_info(uid, gid)
        login = {'done': 0}
        if now_day == last_login:  # 已经签到
            login['done'] = 1
        elif now_day == last_login + 1:  # 连续登陆
            ns_login += 1
        else:
            ns_login = 0

        # login
        conf = Context.Configure.get_game_item_json(gid, 'login.reward')
        if vip['level'] > 0:
            conf = conf['vip']
        else:
            conf = conf['common']
        login['conf'] = conf
        login['which'] = ns_login % len(conf)
        kvs['login'] = login

        # exp
        level, diff = cls.get_exp_info(uid, gid, kvs['exp'])
        kvs['exp_level'] = level
        if diff:
            kvs['exp_diff'] = diff

        # month card
        state, left_days = FishProps.get_vip(uid, gid)
        if left_days >= 0:
            kvs['card'] = {'state': state, 'left': left_days}

        # skill test
        vt, sw = Context.Data.get_game_attrs(uid, gid, ['try_violent', 'try_super_weapon'])
        can_try = []
        if vt is None:
            can_try.append(203)
        if sw is None:
            can_try.append(204)
        if can_try:
            kvs['try'] = can_try

        return is_new, kvs

    @classmethod
    def get_vip_level(cls, uid, gid, pay_total=None):
        if pay_total is None:
            pay_total = Context.Data.get_game_attr_int(uid, gid, 'pay_total', 0)
        conf = Context.Configure.get_game_item_json(gid, 'vip.level')
        if conf:
            start = 0
            for i, v in enumerate(conf):
                if start <= pay_total < v:
                    level = i
                    break
                start = v
            else:
                level = len(conf)
        else:
            level = 0
        return level

    @classmethod
    def get_vip_info(cls, uid, gid):
        pay_total = Context.Data.get_game_attr_int(uid, gid, 'pay_total', 0)
        conf = Context.Configure.get_game_item_json(gid, 'vip.level')
        vip = {}
        if conf:
            start = 0
            for i, v in enumerate(conf):
                if start <= pay_total < v:
                    vip['level'] = i
                    vip['next'] = v
                    break
                start = v
            else:
                vip['level'] = len(conf)
        else:
            vip['level'] = 0
            vip['next'] = conf[0]

        vip['pay_total'] = pay_total
        return vip

    @classmethod
    def get_exp_info(cls, uid, gid, exp=None):
        if exp is None:
            exp = Context.Data.get_game_attr_int(uid, gid, 'exp', 0)
        conf = Context.Configure.get_game_item_json(gid, 'exp.level')
        if conf:
            start = 0
            for i, v in enumerate(conf):
                if start <= exp < v:
                    level, diff = i, [start, v]
                    break
                start = v
            else:
                level, diff = len(conf), None
        else:
            level, diff = 1, [0, conf[1]]
        return level, diff

    @classmethod
    def trans_barrel_level(cls, gid, level):
        conf = Context.Configure.get_game_item_json(gid, 'barrel.unlock.config')
        return conf[level - 1]['multiple']

    @classmethod
    def check_benefit(cls, uid, gid):
        conf = Context.Configure.get_game_item_json(gid, 'benefit.config')
        total_times = len(conf['reward'])
        benefit_times, bankrupt_ts = Context.Daily.get_daily_data(uid, gid, 'benefit_times', 'bankrupt_ts')
        benefit_times = Tool.to_int(benefit_times, 0)
        if benefit_times >= total_times:
            return total_times, total_times, 0, conf
        now_ts = Time.current_ts()
        if bankrupt_ts and bankrupt_ts >= now_ts:
            return total_times, benefit_times, 0, conf
        else:
            return total_times, benefit_times, now_ts - bankrupt_ts, conf

    @classmethod
    def on_create_user(cls, uid, gid):
        super(FishAccount, cls).on_create_user(uid, gid)
        # 发放一级礼包
        conf = Context.Configure.get_game_item_json(gid, 'exp.level.reward')
        rewards_info = FishProps.issue_rewards(uid, gid, conf[0], 'exp.upgrade')
        rewards_info = FishProps.convert_reward(rewards_info)
        mo = MsgPack(Message.FISH_MSG_EXP_UPGRADE | Message.ID_NTF)
        mo.set_param('exp', 0)
        mo.set_param('lv', 1)
        mo.set_param('df', [1, [0, conf[1]]])
        mo.update_param(rewards_info)
        Context.GData.send_to_connect(uid, mo)

        # new user carrying
        pipe_args = []
        for k in ('chip', 'diamond', 'coupon'):
            if k in rewards_info:
                pipe_args.append('login.carrying.volume.%s' % k)
                pipe_args.append(rewards_info[k])
        if 'chip' in rewards_info:
            pipe_args.append('carrying.volume.chip')
            pipe_args.append(rewards_info['chip'])
        if pipe_args:
            Context.Stat.mincr_daily_data(gid, *pipe_args)

    @classmethod
    def on_user_login(cls, uid, gid):
        login = super(FishAccount, cls).on_user_login(uid, gid)
        if login == 1:  # 今天第一次登陆
            max_barrel = Context.Data.get_game_attr_int(uid, gid, 'barrel_level', 1)
            cache_barrel_multi = cls.trans_barrel_level(gid, max_barrel)
            Context.Daily.set_daily_data(uid, gid, 'cache_barrel_multi', cache_barrel_multi)
            # 登陆用户携带量统计
            kvs = Context.Data.get_game_attrs_dict(uid, gid, ['chip', 'diamond', 'coupon'])
            pipe_args = []
            for k, v in kvs.iteritems():
                pipe_args.append('login.carrying.volume.%s' % k)
                pipe_args.append(v)
            if pipe_args:
                Context.Stat.mincr_daily_data(gid, *pipe_args)

    @classmethod
    def check_bankrupt(cls, uid, gid):
        benefit_times, bankrupt_ts = Context.Daily.get_daily_data(uid, gid, 'benefit_times', 'bankrupt_ts')
        benefit_times = Tool.to_int(benefit_times, 0)
        wait, which = None, None
        if bankrupt_ts:  # 已经在破产状态, 未领取
            which = benefit_times + 1
            wait = int(bankrupt_ts) - Time.current_ts()
            if wait < 0:
                wait = 0
        else:
            conf = Context.Configure.get_game_item_json(gid, 'benefit.config')
            if benefit_times < len(conf['reward']):
                reward = conf['reward'][benefit_times]
                bankrupt_ts = Time.current_ts() + reward['wait']
                Context.Daily.set_daily_data(uid, gid, 'bankrupt_ts', bankrupt_ts)
                wait = reward['wait']
                which = benefit_times + 1

        mo = MsgPack(Message.FISH_MSG_BANKRUPT | Message.ID_NTF)
        mo.set_param('userId', uid)
        if wait is not None:
            mo.set_param('wait', wait)
        if which is not None:
            mo.set_param('which', which)  # 可以领取哪一次
        return mo
