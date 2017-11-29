#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-04

import random
from framework.core.tasklet import server
from framework.util.tool import Time
from framework.util.tool import Tool
from framework.entity.online import Online
from framework.entity.msgpack import MsgPack
from framework.entity.const import Message
from framework.context import Context
from lemon.entity.account import Account


class EntityTasklet(server.BasicServerTasklet):
    def onInnerMessage(self, cmd, mi, *args, **kwargs):
        uid = mi.get_uid()
        gid = mi.get_gid()
        raw = mi.get_message()
        mi = MsgPack.unpack(cmd, raw)
        gid = mi.get_param('gameId', gid)
        with Context.GData.user_locker[uid]:
            if cmd == Message.MSG_SYS_USER_INFO | Message.ID_REQ:
                self.onUserInfo(uid, gid, mi)
            elif cmd == Message.MSG_SYS_GAME_INFO | Message.ID_REQ:
                self.onGameInfo(uid, gid, mi)
            elif cmd == Message.MSG_SYS_SERVER_INFO | Message.ID_REQ:
                self.onServerInfo(uid, gid, mi)
            elif cmd == Message.MSG_SYS_LED | Message.ID_REQ:
                self.onLed(uid, gid, mi)
            else:
                entity = Context.get_module(gid, 'entity')
                if entity:
                    entity.onMessage(cmd, uid, gid, mi)
                else:
                    Context.Log.warn('error msg', cmd, mi)

    def onUserInfo(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_USER_INFO | Message.ID_ACK)
        account = Context.get_module(gid, 'account', Account)
        data = account.get_user_info(uid, gid)
        if not data:
            mo.set_error(-1, 'no user info')
        else:
            mo.update_param(data)

        login = mi.get_param('login')
        if login:
            account.on_user_login(uid, gid)
            result, loc = Online.get_location(uid, gid)
            if result and loc:
                loc = {
                    'roomType': loc['room_type'],
                    'tableId': loc['table_id'],
                    'seatId': loc['seat_id']
                }
                mo.set_param('loc', loc)
        return Context.GData.send_to_connect(uid, mo)

    def onGameInfo(self, uid, gid, mi):
        gid = mi.get_param('gameId')
        mo = MsgPack(Message.MSG_SYS_GAME_INFO | Message.ID_ACK)
        account = Context.get_module(gid, 'account', Account)
        is_new, data = account.get_game_info(uid, gid)
        if not data:
            mo.set_error(-1, 'no game info')
        else:
            mo.update_param(data)
            if is_new:
                mo.set_param('new', 1)

        info = Context.RedisCache.hash_mget('global.notice', 'led',
                                            'start', 'end')
        led = info[0]
        if led:
            now_ts = Time.current_ts()
            start = int(info[1])
            end = int(info[2])
            if start < now_ts < end:
                mo.set_param('global_notice', {'list': [led], 'end': end,
                                               'now_ts': now_ts})

        Context.GData.send_to_connect(uid, mo)

        if is_new:
            account.on_create_user(uid, gid)

        if account.auto_issue_benefit:
            benefit_config = Context.Configure.get_game_item_json(gid, 'benefit.config')
            if benefit_config and benefit_config['limit'] > data['chip']:
                benefit = Context.Daily.issue_benefit(uid, gid)
                mo = MsgPack(Message.MSG_SYS_BENEFIT | Message.ID_NTF)
                if not benefit:
                    benefit = {
                        'which': 0,
                        'total': 0,
                        'reward': 0,
                        'chip': data['chip'],
                    }
                mo.update_param(benefit)
                Context.GData.send_to_connect(uid, mo)

    def onServerInfo(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_SERVER_INFO | Message.ID_ACK)
        game_room = Context.GData.map_room_type.get(gid)
        if game_room is None:
            mo.set_error(1, 'not found game')
        else:
            total, online_list = 0, []
            room_types = sorted(game_room.keys())
            onlines = Context.Online.get_online(gid, *room_types)
            for _type, _online in zip(room_types, onlines):
                _online = Tool.to_int(_online, 0)
                if _online < 1000:
                    _online = 1000 + random.randint(0, 10)
                total += _online
                online_list.append([_type, _online])
            mo.set_param('gameId', gid)
            mo.set_param('list', online_list)
            mo.set_param('online', total)
        return Context.GData.send_to_connect(uid, mo)

    def onLed(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_LED | Message.ID_ACK)
        action = mi.get_param('action', 'get')
        if action == 'get':
            last_ts = mi.get_param('last_ts', 0)
            led_list = Context.RedisCache.list_range('global.led.list', 0, 9)
            _list, ts = [], 0
            for led in led_list:
                led = Context.json_loads(led)
                if led['ts'] > last_ts:
                    _list.append(led['led'])
                    ts = led['ts']
            if _list:
                mo.set_param('global', {'ts': ts, 'list': _list})

            led_list = Context.RedisCache.list_range('game.%d.led.list' % gid, 0, 9)
            _list, ts = [], 0
            for led in led_list:
                led = Context.json_loads(led)
                if led['ts'] > last_ts:
                    _list.append(led['led'])
                    ts = led['ts']

            if _list:
                mo.set_param('game', {'ts': ts, 'list': _list})
        elif action == 'put':
            conf = Context.Configure.get_game_item_json(gid, 'led.config')
            if not conf or not conf.get('enable'):
                mo.set_error(101, 'led not available')
            else:
                msg = mi.get_param('msg')
                cost = conf['cost']
                real, final = Context.UserAttr.incr_diamond(uid, gid, -cost, 'led.put')
                if real != -cost:
                    mo.set_error(102, 'no enough diamond')
                else:
                    led = Context.json_dumps({'led': msg, 'ts': Time.current_ts()})
                    Context.RedisCache.list_lpush('game.%d.led.list' % gid, led)

        return Context.GData.send_to_connect(uid, mo)

    def on_server_heart_beat(self):
        pass
