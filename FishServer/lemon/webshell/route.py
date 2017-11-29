#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-02-26

from framework.context import Context
from framework.entity.msgpack import MsgPack
from framework.util.exceptions import NotFoundException
from framework.util.exceptions import ForbiddenException
from framework.util.tool import Time
from framework.util.tool import Algorithm


class HttpShell(object):
    token = None

    def __init__(self):
        self.token = Context.Configure.get_global_item('shell.access_key')
        self.json_path = {
            '/v1/shell/gm/account/freeze': self.freeze_user,
            '/v1/shell/gm/account/disable': self.disable_user,
            '/v1/shell/gm/reward/chip': self.gm_reward_chip,
            '/v1/shell/gm/reward/diamond': self.gm_reward_diamond,
            '/v1/shell/gm/push/led': self.gm_push_led,
            '/v1/shell/query/summary': self.query_summary,
        }

    def check_token(self, gid, mi):
        sign = mi.get_param('sign')
        ts = mi.get_param('ts')
        gid = mi.get_param('gameId')
        line = 'gameId=%d&token=%s&ts=%d' % (gid, self.token, ts)
        _sign = Algorithm.md5_encode(line)
        if sign != _sign:
            Context.Log.error('verify token key failed', _sign, sign)
            return False
        return True

    def onMessage(self, request):
        if request.method.lower() == 'post':
            data = request.raw_data()
            mi = MsgPack.unpack(0, data)
            Context.Log.debug(mi)
            gid = mi.get_param('gameId')
            if not self.check_token(gid, mi):
                raise ForbiddenException('no permission access')
            if request.path in self.json_path:
                return self.json_path[request.path](gid, mi, request)
            from lemon import classMap
            if gid in classMap:
                http = classMap[gid].get('shell')
                if http and request.path in http.json_path:
                    return http.json_path[request.path](gid, mi, request)

        raise NotFoundException('Not Found')

    def freeze_user(self, gid, mi, request):
        uid = mi.get_param('userId')
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')
        days = mi.get_param('days')
        mo = MsgPack(0)
        if days is None:
            Context.RedisMix.hash_del('game.%d.freeze.user' % gid, uid)
        else:
            end_ts = Time.today_start_ts() + days * 3600 * 24
            Context.RedisMix.hash_set('game.%d.freeze.user' % gid, uid, end_ts)
            mo.set_param('end_ts', end_ts)
        return mo

    def disable_user(self, gid, mi, request):
        uid = mi.get_param('userId')
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')
        disable = mi.get_param('disable')
        if disable:
            Context.RedisMix.set_add('game.%d.disable.user' % gid, uid)
        else:
            Context.RedisMix.set_rem('game.%d.disable.user' % gid, uid)
        return MsgPack(0)

    def gm_reward_chip(self, gid, mi, request):
        uid = mi.get_param('userId')
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')
        chip = mi.get_param('chip')
        real, final = Context.UserAttr.incr_chip(uid, gid, chip, 'gm.reward')
        if real != chip:
            MsgPack.Error(0, 1, 'not enough')
        return MsgPack(0, {'chip': final, 'delta': real})

    def gm_reward_diamond(self, gid, mi, request):
        uid = mi.get_param('userId')
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')
        diamond = mi.get_param('diamond')
        real, final = Context.UserAttr.incr_diamond(uid, gid, diamond, 'gm.reward')
        if real != diamond:
            MsgPack.Error(0, 1, 'not enough')
        return MsgPack(0, {'diamond': final, 'delta': real})

    def gm_push_led(self, gid, mi, request):
        msg = mi.get_param('msg')
        if not msg:     # 清除led
            Context.RedisCache.delete('game.%d.led.list' % gid)
        else:
            led = Context.json_dumps({'led': msg, 'ts': Time.current_ts()})
            Context.RedisCache.list_lpush('game.%d.led.list' % gid, led)
        return MsgPack(0)

    def query_summary(self, gid, mi, request):
        # 新增设备, 新增用户, 活跃用户, (新)付费玩家, (新)用户付费, 充值次数
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            kvs = Context.Stat.get_day_data(gid, fmt)
            channel_info = {}
            for k, v in kvs.iteritems():
                if (k.endswith('.new.device.count') or k.endswith('.new.user.count') or
                        k.endswith('.login.user.count') or k.endswith('.new.pay.user.count') or
                        k.endswith('.new.pay.user.pay_total') or k.endswith('.pay.user.count') or
                        k.endswith('.pay.user.pay_total') or k.endswith('.user.pay.times')):
                    channel, key = k.split('.', 1)
                    if channel not in channel_info:
                        channel_info[channel] = {}
                    channel_info[channel][key] = int(v)

            mo.set_param(fmt, channel_info)
            start_day = Time.next_days(start_day)
        return mo


HttpShell = HttpShell()
