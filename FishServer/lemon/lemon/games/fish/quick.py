#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-23

from const import Enum
from const import Message
from framework.context import Context
from framework.util.tool import Time
from lemon.entity.quick import Quick
from framework.entity.msgpack import MsgPack


class FishQuick(Quick):
    def onMessage(self, cmd, uid, gid, mi):
        mo = None
        if cmd == Message.MSG_SYS_QUICK_START | Message.ID_REQ:
            mo = self.__on_quick_start(uid, gid, mi)
        if isinstance(mo, MsgPack):
            Context.GData.send_to_connect(uid, mo)

    def __on_quick_start(self, uid, gid, mi):
        Context.Log.info(uid, 'req quick start with', mi)
        mo = MsgPack(Message.MSG_SYS_QUICK_START | Message.ID_ACK)

        result, location = Context.Online.get_location(uid, gid)
        if not result:
            return mo.set_error(Enum.quick_start_failed_unknown, 'info illegal')

        now_ts = Time.current_ts()
        if location:
            mo.set_param('serverId', location['serverId'])
            mo.set_param('roomType', location['room_type'])
            mo.set_param('tableId', location['table_id'])
            mo.set_param('seatId', location['seat_id'])
            return mo

        room_type = mi.get_param('roomType', 0)
        chip = Context.UserAttr.get_chip(uid, gid, 0)
        room_type, desc = self.__find_available_room(uid, gid, chip, room_type)
        if room_type not in (201, 202, 203):
            return mo.set_error(room_type, desc)

        play_mode = mi.get_param('playMode', Enum.play_mode_common)
        if play_mode != Enum.play_mode_common:
            return mo.set_error(110, 'error play mode')

        # 分配玩家
        for num in (3, 2, 1):
            table_list = self.__get_table_list(gid, room_type, play_mode, num)
            for table_id in table_list:
                key = 'table:%d:%d' % (gid, table_id)
                attrs = ['status', 'fresh_ts', 'serverId']
                kvs = Context.RedisCache.hash_mget_as_dict(key, *attrs)
                if len(attrs) != len(kvs):
                    Context.Log.error('get table info failed', uid, gid, room_type, table_id, num, kvs)
                    continue

                server_id = int(kvs['serverId'])
                if server_id < 0:
                    Context.Log.info('table server_id error', uid, gid, room_type, table_id, num, server_id)
                    continue

                seat_id = self.__join_table(uid, gid, room_type, play_mode, table_id)
                if seat_id < 0:
                    Context.Log.error('join_table failed!', uid, gid, room_type, table_id)
                    continue
                Context.Online.set_location(uid, gid, server_id, room_type, table_id, seat_id, 0, now_ts, play_mode=play_mode)
                mo.set_param('serverId', server_id)
                mo.set_param('roomType', room_type)
                mo.set_param('tableId', table_id)
                mo.set_param('seatId', seat_id)
                Context.Log.info('join table', uid, gid, server_id, room_type, table_id, server_id, play_mode)
                return mo

        # new table
        table_id = self.get_free_table(gid)
        server_id = self.__select_server(uid, gid, table_id, room_type)
        if not server_id:
            Context.Log.error('select server failed', uid, gid, room_type)
            return mo.set_error(Enum.quick_start_failed_unknown, 'no server found')

        self.__create_table(gid, room_type, play_mode, table_id, server_id, now_ts)
        seat_id = self.__join_table(uid, gid, room_type, play_mode, table_id)
        if seat_id < 0:
            Context.Log.error('join_table failed!', uid, gid, room_type, table_id)
            return mo.set_error(Enum.quick_start_failed_unknown, 'json table failed')

        Context.Online.set_location(uid, gid, server_id, room_type, table_id, seat_id, 0, now_ts, play_mode=play_mode)

        mo.set_param('serverId', server_id)
        mo.set_param('roomType', room_type)
        mo.set_param('tableId', table_id)
        mo.set_param('seatId', seat_id)
        Context.Log.info('create location info', uid, gid, server_id, room_type, table_id, seat_id, play_mode)
        return mo

    def __find_available_room(self, uid, gid, chip, room_type):
        room_config = Context.Configure.get_room_config(gid)
        barrel_level = Context.Data.get_game_attr_int(uid, gid, 'barrel_level', 1)
        if room_type:
            # room
            for conf in room_config:
                if room_type == conf['room_type']:
                    chip_min = conf.get('chip_min', -1)
                    if chip_min > 0 and chip < chip_min:
                        return Enum.quick_start_failed_chip_small, u'金币不足'
                    chip_max = conf.get('chip_max', -1)
                    if chip > chip_max > 0:
                        return Enum.quick_start_failed_chip_big, u'金币限制'

                    level_min = conf.get('level_min', -1)
                    if level_min > 0 and barrel_level < level_min:
                        return Enum.quick_start_failed_barrel_small, u'炮倍不足，1000炮倍才可以进入竞技场'
                    level_max = conf.get('level_max', -1)
                    if barrel_level > level_max > 0:
                        return Enum.quick_start_failed_barrel_big, u'炮倍限制'
                    return room_type, ''

        # 自动匹配房间
        rcs = set()
        for conf in room_config:
            chip_min = conf.get('chip_min', -1)
            if chip_min > 0 and chip < chip_min:
                continue
            chip_max = conf.get('chip_max', -1)
            if chip > chip_max > 0:
                continue
            level_min = conf.get('level_min', -1)
            if level_min > 0 and barrel_level < level_min:
                continue
            level_max = conf.get('level_max', -1)
            if barrel_level > level_max > 0:
                continue
            rcs.add(conf['room_type'])
        if not rcs:
            return Enum.quick_start_failed_unknown, u'未知错误'
        else:
            rcs = sorted(rcs)
            return rcs[-1], ''

    def __get_table_list(self, gid, room_type, play_mode, num):
        if num == 0:
            key = 'quick:%d:%d:%d' % (gid, num, play_mode)
        else:
            key = 'quick:%d:%d:%d:%d' % (gid, room_type, num, play_mode)
        table_list = Context.RedisCache.list_range(key, 0, -1)
        return (int(tid) for tid in table_list)

    def __kick_off(self, uid, gid, tid):
        if tid > 0:
            res = Context.RedisCache.execute_lua_alias('kick_off', uid, gid, 4, tid)
        else:
            res = Context.RedisCache.execute_lua_alias('kick_off', uid, gid, 4, 0)
        return res

    def __join_table(self, uid, gid, room_type, play_mode, table_id):
        attrs = [uid, gid, room_type, table_id, 4, play_mode]
        res = Context.RedisCache.execute_lua_alias('join_table', *attrs)
        Context.Log.info('user join table', uid, gid, room_type, table_id, res)
        return res[0]

    def __select_server(self, uid, gid, table_id, room_type):
        if gid not in Context.GData.map_room_type:
            Context.Log.error('no game_server found', uid, gid)
            return False
        if room_type not in Context.GData.map_room_type[gid]:
            Context.Log.error('no room_type found', uid, gid, room_type)
            return False
        ss = Context.GData.map_room_type[gid][room_type]
        server_id = ss[table_id % len(ss)]
        if server_id not in Context.GData.map_server_info:
            Context.Log.error('not found the server', uid, gid, room_type, server_id)
            return False
        return server_id

    def __create_table(self, gid, room_type, play_mode, table_id, server_id, now_ts):
        key = 'table:%d:%d' % (gid, table_id)
        kvs = {
            'serverId': server_id,
            'room_type': room_type,
            'play_mode': play_mode,
            'status': 0,
            'seat0': 0,
            'seat1': 0,
            'seat2': 0,
            'seat3': 0,
            'fresh_ts': now_ts,
        }
        Context.RedisCache.hash_mset(key, **kvs)
        return True


FishQuick = FishQuick()
