#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-02-13

from framework.interface import IContext
from framework.interface import ICallable
from framework.entity.const import FlagType
from framework.entity.msgline import MsgLine
from framework.entity.const import Message
from framework.util.locker import Locker
from framework.util.locker import LockerMap


class GData(IContext, ICallable):
    def __init__(self):
        self.server = None
        self.server_id = 0
        self.server_type = 0
        self.game_list = []
        self.game_desc = {}
        self.server_info = {}           # {server info}
        self.map_room_config = {}       # {gameId: {room config}}
        self.map_room_type = {}         # {roomtype: [serverId, ...]}
        self.map_server_type = {}       # {server_type: [serverId, ...]}
        self.map_server_info = {}       # {server_id: {server process info}}
        self.map_server_connect = {}    # {server_id: connect}
        self.map_game_server = {}       # {gameId: [serverId, ...]}

        self.server_locker = Locker('server_lock')
        self.user_locker = LockerMap()
        self.table_locker = LockerMap()

        self.map_client_connect = {}    # {user_id: connect | player}
        self.map_three_server = {}      # {game_id: connect}
        self.online_user = {}
        self.online_table = {}

    def init_data(self):
        game_list = self.ctx.Configure.get_global_item_json('game.list')
        if not game_list:
            raise Exception('get game_list failed!')

        self.game_list = game_list

        desc = self.ctx.Configure.get_global_item_json('game.desc')
        game_desc = {}
        for game in desc:
            game_desc[game['id']] = game
        self.game_desc = game_desc

        self.__load_server_info()
        if self.server_type != FlagType.flag_type_sdk:
            self.__load_room_config()
            self.__load_room_map()

    def send_to_client(self, uid, msg, connection=None, cmd=None):
        if cmd is None:
            if isinstance(msg, str):
                return False
            cmd = msg.get_cmd()

        if not isinstance(msg, str):
            msg = msg.pack()

        if connection:
            return connection.sendMsg(cmd, msg)

        connection = self.map_client_connect.get(uid)
        if connection:
            return connection.sendMsg(cmd, msg)
        return False

    def __send_to_server(self, uid, msg, dst, sid, cmd, gid):
        if sid is None:
            ids = self.map_server_type.get(dst, [])
            if not ids:
                return False
            sid = ids[uid % len(ids)]
        conn = self.map_server_connect.get(sid, None)
        if not conn:
            return False

        if cmd is None:
            if isinstance(msg, str):
                return False
            cmd = msg.get_cmd()

        cmd = Message.to_inner(cmd)
        if not isinstance(msg, str):
            msg = msg.pack()

        mo = MsgLine(msg, gid, target=uid)
        return conn.sendMsg(cmd, mo.pack())

    def send_to_connect(self, uid, msg, sid=None, cmd=None, gid=None):
        return self.__send_to_server(uid, msg, FlagType.flag_type_connect, sid, cmd, gid)

    def send_to_entity(self, uid, msg, sid=None, cmd=None, gid=None):
        return self.__send_to_server(uid, msg, FlagType.flag_type_entity, sid, cmd, gid)

    def send_to_quick(self, uid, msg, sid=None, cmd=None, gid=None):
        return self.__send_to_server(uid, msg, FlagType.flag_type_quick, sid, cmd, gid)

    def send_to_game(self, uid, msg, sid, cmd=None, gid=None):
        if sid < 0:
            return False
        return self.__send_to_server(uid, msg, FlagType.flag_type_game, sid, cmd, gid)

    def send_to_three(self, msg, cmd=None, gid=None, uid=None, connection=None):
        if connection is None:
            if gid is None:
                return False
            connection = self.map_three_server.get(gid)
        if connection is None:
            return False
        if cmd is None:
            cmd = msg.get_cmd()
        if not isinstance(msg, str):
            msg = msg.pack()
        mo = MsgLine(msg, gid, target=uid)
        return connection.sendMsg(cmd, mo.pack())

    def broadcast_to_system(self, msg, gid=None, room=None, target=None):
        ids = self.map_server_type.get(FlagType.flag_type_connect, [])
        inner_cmd = Message.to_inner(msg.get_cmd())
        data = MsgLine(msg.pack(), gid, room, target).pack()

        for _id in ids:
            conn = self.map_server_connect.get(_id, None)
            if conn:
                conn.sendMsg(inner_cmd, data)

    def forward_to_system(self, cmd, msg):
        if not isinstance(msg, str):
            msg = msg.pack()
        ids = self.map_server_type.get(FlagType.flag_type_connect, [])
        inner_cmd = Message.to_inner(cmd)
        for _id in ids:
            conn = self.map_server_connect.get(_id, None)
            if conn:
                conn.sendMsg(inner_cmd, msg)

    def __load_room_config(self):
        self.ctx.Log.info('load room config')
        for gid in self.game_list:
            room_config = self.ctx.Configure.get_room_config(gid)
            self.map_room_config[gid] = room_config
        self.ctx.Log.info('map_room_config:', self.map_room_config)

    def __load_room_map(self):
        self.ctx.Log.info('load room map')
        for gid in self.game_list:
            self.map_room_type[gid] = {}
            game_server_ids = set()
            room_map = self.ctx.Configure.get_game_item_json(gid, 'room.map')
            for k, v in room_map.iteritems():
                self.map_room_type[gid][int(k)] = v
                game_server_ids.update(v)
            self.map_game_server[gid] = sorted(game_server_ids)
        self.ctx.Log.info('map_room_type:', self.map_room_type)
        self.ctx.Log.info('map_game_server:', self.map_game_server)

    def __load_server_info(self):
        self.ctx.Log.info('load server info')
        server_map = self.ctx.Configure.get_global_item_json('server.map')
        for server_type, processes in server_map.iteritems():
            s = [process['serverId'] for process in processes]
            self.map_server_type[server_type] = s
            server_type = FlagType.trans_server_type(server_type)
            self.map_server_type[server_type] = s
            for process in processes:
                process['type'] = server_type
                self.map_server_info[process['serverId']] = process
                if process['serverId'] == self.server_id:
                    self.server_info = process
                    self.server_type = process['type']
        self.ctx.Log.info('map_server_type:', self.map_server_type)
        self.ctx.Log.info('map_server_info:', self.map_server_info)
        self.ctx.Log.info('server_info:', self.server_info)

    def get_new_user_id(self):
        self.ctx.RedisMix.hash_setnx('global.info.hash', 'max.user.id', 20000)
        max_user_id = self.ctx.RedisMix.hash_incrby('global.info.hash', 'max.user.id', 1)
        self.ctx.Log.report('max.user.id:', max_user_id)
        return max_user_id


GData = GData()
