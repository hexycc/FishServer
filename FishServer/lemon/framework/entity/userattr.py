#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-29

from framework.interface import IContext
from framework.interface import ICallable
from framework.entity.const import Const


class UserAttr(IContext, ICallable):
    def incr_attr(self, uid, gid, field, delta, event, low=-1, high=-1, mode=Const.chip_operate_noop, **kwargs):
        """
        对用户的%(attr)进行操作
        @param uid: userId
        @param gid: 游戏ID
        @param field: 属性字段
        @param delta: 变化的值可以是负数
        @param low: 用户最低%(attr)数，-1表示没有最低限制
        @param high: 用户最高%(attr)数，-1表示没有最高限制
        @param mode: 当INCR动作会变成负数时的处理模式, 0表示不进行操作; 1会给%(attr)清零
        @param event: 触发INCR的事件ID
        @param kwargs: 需要根据事件传入附加参数
        @return (real, final) real表示实际变化的值, final表示变化后的最终数量
        """
        assert isinstance(uid, int)
        assert isinstance(gid, int)
        assert isinstance(field, (str, unicode))
        assert isinstance(delta, int)
        assert isinstance(low, int)
        assert isinstance(high, int)
        assert mode in (Const.chip_operate_noop, Const.chip_operate_zero)
        assert isinstance(event, (str, unicode))
        alias = 'incr_attr'
        key = 'game:%d:%d' % (gid, uid)
        real, final, fixed = self.ctx.RedisCluster.execute_lua_alias(uid, alias, delta, low, high, mode, key, field)
        if fixed:
            self.ctx.Log.report('%s.fixed:' % field, [uid, gid, int(fixed), 0, event, kwargs])
            self.ctx.Stat.incr_daily_data(gid, 'in.%s.fixed' % field, fixed)
            self.ctx.RedisMix.hash_incrby('game.%d.info.hash' % gid, 'in.%s.fixed' % field, fixed)

        if real or delta == 0:
            self.ctx.Log.report('%s.update:' % field, [uid, gid, int(real), int(final), event, kwargs])
            if real != 0:
                if real > 0:
                    in_or_out = 'in'
                else:
                    in_or_out = 'out'

                if 'roomtype' in kwargs:
                    _field = '%s.%s.%s.%d' % (in_or_out, field, event, kwargs['roomtype'])
                else:
                    _field = '%s.%s.%s' % (in_or_out, field, event)

                if real > 0:
                    self.ctx.Stat.incr_daily_data(gid, _field, real)
                    self.ctx.RedisMix.hash_incrby('game.%d.info.hash' % gid, '%s.%s' % (in_or_out, field), real)
                else:
                    self.ctx.Stat.incr_daily_data(gid, _field, -real)
                    self.ctx.RedisMix.hash_incrby('game.%d.info.hash' % gid, '%s.%s' % (in_or_out, field), -real)

        return real, final

    def incr_chip(self, uid, gid, delta, event, low=-1, high=-1, mode=Const.chip_operate_noop, **kwargs):
        return self.incr_attr(uid, gid, 'chip', delta, event, low, high, mode, **kwargs)

    def get_chip(self, uid, gid, default=None):
        return self.ctx.Data.get_game_attr_int(uid, gid, 'chip', default)

    def incr_diamond(self, uid, gid, delta, event, low=-1, high=-1, mode=Const.chip_operate_noop, **kwargs):
        return self.incr_attr(uid, gid, 'diamond', delta, event, low, high, mode, **kwargs)

    def get_diamond(self, uid, gid, default=None):
        return self.ctx.Data.get_game_attr_int(uid, gid, 'diamond', default)

    def incr_coupon(self, uid, gid, delta, event, low=-1, high=-1, mode=Const.chip_operate_noop, **kwargs):
        return self.incr_attr(uid, gid, 'coupon', delta, event, low, high, mode, **kwargs)

    def get_coupon(self, uid, gid, default=None):
        return self.ctx.Data.get_game_attr_int(uid, gid, 'coupon', default)

    def check_exist(self, uid, gid):
        chip = self.ctx.Data.get_game_attr(uid, gid, 'chip')
        return chip is not None

UserAttr = UserAttr()
