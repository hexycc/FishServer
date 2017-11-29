#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-12-21

from framework.context import Context


class Props(object):
    PROP_CHIP = 1           # 金币
    PROP_DIAMOND = 2        # 钻石
    PROP_COUPON = 3         # 奖券
    PROP_RMB = 4            # 人民币

    PROP_VIP = 10           # 月卡

    def incr_vip(self, uid, gid, delta, event, **kwargs):
        assert int(delta) != 0
        today = Context.Time.up_days()
        state, days = Context.RedisCluster.execute_lua_alias(uid, 'vip_op', 'incr', uid, gid, today, delta)
        Context.Log.report('incr.vip:', [uid, gid, delta, days, event, kwargs])
        return state, days

    def get_vip(self, uid, gid):
        today = Context.Time.up_days()
        return Context.RedisCluster.execute_lua_alias(uid, 'vip_op', 'get', uid, gid, today)

    def use_vip(self, uid, gid):
        today = Context.Time.up_days()
        success, left_days = Context.RedisCluster.execute_lua_alias(uid, 'vip_op', 'use', uid, gid, today)
        if success:
            Context.Log.report('use.vip:', [uid, gid, -1, left_days])
        return success, left_days

    def incr_pay(self, uid, gid, delta, event, **kwargs):
        assert int(delta) != 0
        final = Context.Data.hincr_game(uid, gid, 'pay_total', delta)
        Context.Log.report('pay.update:', [uid, gid, delta, final, event, kwargs])
        return final

    def incr_props(self, uid, gid, pid, count, event, **kwargs):
        assert self.check_props(pid)
        assert int(count) != 0

        real, final, fixed = Context.RedisCluster.execute_lua_alias(uid, 'props_op', 'incr', uid, gid, pid, count)
        if fixed:
            Context.Log.report('props.%s.fixed:' % pid, [uid, gid, int(fixed), 0, event, kwargs])
            Context.Stat.incr_daily_data(gid, 'in.props.%d.fixed' % pid, fixed)
            Context.RedisMix.hash_incrby('game.%d.info.hash' % gid, 'in.props.%d.fixed' % pid, fixed)

        if real or count == 0:
            Context.Log.report('props.%s.update:' % pid, [uid, gid, int(real), int(final), event, kwargs])
            if real != 0:
                if real > 0:
                    in_or_out = 'in'
                else:
                    in_or_out = 'out'
                if 'roomtype' in kwargs:
                    _field = '%s.props.%d.%s.%d' % (in_or_out, pid, event, kwargs['roomtype'])
                else:
                    _field = '%s.props.%d.%s' % (in_or_out, pid, event)
                Context.Stat.incr_daily_data(gid, _field, real)
                Context.RedisMix.hash_incrby('game.%d.info.hash' % gid, '%s.props.%d' % (in_or_out, pid), real)

        return real, final

    def get_props(self, uid, gid, pid):
        return Context.RedisCluster.execute_lua_alias(uid, 'props_op', 'get', uid, gid, pid)

    def __check_incr_args(self, *args):
        l = list(args)
        if len(l) < 2 or len(l) % 2 != 0:
            raise Exception('error count')

        for i in xrange(0, len(l), 2):
            assert self.check_props(l[i])
            assert int(l[i + 1]) != 0
        return l

    def mincr_props(self, uid, gid, event, *args, **kwargs):
        self.__check_incr_args(*args)

        failed, finals = Context.RedisCluster.execute_lua_alias(uid, 'props_op', 'mincr', uid, gid, *args)
        if failed:
            return False

        for i, final in enumerate(finals):
            pid, real = args[2 * i], args[2 * i + 1]
            Context.Log.report('props.%s.update:' % pid, [uid, gid, int(real), int(final), event, kwargs])
            if real != 0:
                if real > 0:
                    in_or_out = 'in'
                else:
                    in_or_out = 'out'
                if 'roomtype' in kwargs:
                    _field = '%s.props.%d.%s.%d' % (in_or_out, pid, event, kwargs['roomtype'])
                else:
                    _field = '%s.props.%d.%s' % (in_or_out, pid, event)
                Context.Stat.incr_daily_data(gid, _field, real)
                Context.RedisMix.hash_incrby('game.%d.info.hash' % gid, '%s.props.%d' % (in_or_out, pid), real)
        return finals

    def check_props(self, pid):
        raise NotImplementedError

    def issue_rewards(self, uid, gid, rewards, event, **kwargs):
        rewards_info = {}
        if rewards:
            chip = rewards.get('chip', 0)
            if chip > 0:
                _, final = Context.UserAttr.incr_chip(uid, gid, chip, event, **kwargs)
                rewards_info['chip'] = final
            diamond = rewards.get('diamond', 0)
            if diamond:
                _, final = Context.UserAttr.incr_diamond(uid, gid, diamond, event, **kwargs)
                rewards_info['diamond'] = final

            coupon = rewards.get('coupon', 0)
            if coupon:
                _, final = Context.UserAttr.incr_coupon(uid, gid, coupon, event, **kwargs)
                rewards_info['coupon'] = final

            props = rewards.get('props')
            if props:
                _props = []
                for prop in props:
                    if self.check_props(prop['id']):
                        _, final = self.incr_props(uid, gid, prop['id'], prop['count'], event, **kwargs)
                        _props.append({'id': prop['id'], 'count': final})
                if _props:
                    rewards_info['props'] = _props

            rewards_info['reward'] = rewards
        return rewards_info

    def merge_reward(self, *args):
        if not args:
            return {}
        if len(args) == 1:
            return args[0]
        rewards = {}
        for arg in args:
            rewards = self.__merge_reward(rewards, arg)
        return rewards

    def __merge_reward(self, prev, later):
        if not prev:
            return Context.copy_json_obj(later)
        if not later:
            return Context.copy_json_obj(prev)

        rewards = {}
        # merge金币
        if 'chip' in prev or 'chip' in later:
            rewards['chip'] = prev.get('chip', 0) + later.get('chip', 0)
        # merge钻石
        if 'diamond' in prev or 'diamond' in later:
            rewards['diamond'] = prev.get('diamond', 0) + later.get('diamond', 0)
        # merge兑换券
        if 'coupon' in prev or 'coupon' in later:
            rewards['coupon'] = prev.get('coupon', 0) + later.get('coupon', 0)
        # merge道具
        props = {}
        for tmp in [prev, later]:
            if 'props' in tmp:
                for prop in tmp['props']:
                    if prop['id'] not in props:
                        props[prop['id']] = prop
                    else:
                        props[prop['id']]['count'] += prop['count']

        if props:
            rewards['props'] = props.values()

        return rewards

    def merge_reward_result(self, detail, *args):
        if not args:
            return {}
        if len(args) == 1:
            return args[0]
        rewards = {}
        for arg in args:
            rewards = self.__merge_reward_result(detail, rewards, arg)
        return rewards

    def __merge_reward_result(self, detail, prev, later):
        if not prev:
            return Context.copy_json_obj(later)
        if not later:
            return Context.copy_json_obj(prev)

        ret = {}

        # 合并最终的字段
        if 'chip' in later:
            ret['chip'] = later['chip']
        elif 'chip' in prev:
            ret['chip'] = prev['chip']

        if 'diamond' in later:
            ret['diamond'] = later['diamond']
        elif 'diamond' in prev:
            ret['diamond'] = prev['diamond']

        _props = {}
        for tmp in [prev, later]:
            if 'props' in tmp:
                for prop in tmp['props']:
                    _props[prop['id']] = prop
        if _props:
            ret['props'] = _props.values()

        if detail:
            # 合并奖励字段
            prev_reward, later_reward = prev['reward'], later['reward']
            rewards = {}
            # merge金币
            if 'chip' in prev_reward or 'chip' in later_reward:
                rewards['chip'] = prev_reward.get('chip', 0) + later_reward.get('chip', 0)
            # merge fake 金币
            if 'fake_chip' in prev_reward or 'fake_chip' in later_reward:
                rewards['fake_chip'] = prev_reward.get('fake_chip', 0) + later_reward.get('fake_chip', 0)
            # merge钻石
            if 'diamond' in prev_reward or 'diamond' in later_reward:
                rewards['diamond'] = prev_reward.get('diamond', 0) + later_reward.get('diamond', 0)
            # merge兑换券
            if 'coupon' in prev_reward or 'coupon' in later_reward:
                rewards['coupon'] = prev_reward.get('coupon', 0) + later_reward.get('coupon', 0)
            # merge道具
            props = {}
            for tmp in [prev_reward, later_reward]:
                if 'props' in tmp:
                    for prop in tmp['props']:
                        if prop['id'] not in props:
                            props[prop['id']] = prop
                        else:
                            props[prop['id']]['count'] += prop['count']

            if props:
                rewards['props'] = props.values()

            if rewards:
                ret['reward'] = rewards

        return ret
