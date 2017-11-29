#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-09

from framework.core.tasklet import server
from framework.context import Context
from framework.util.tool import Time
from lemon.entity.account import Account
from framework.entity.const import Message
from framework.entity.msgpack import MsgPack


class ConnectTasklet(server.BasicServerTasklet):
    def onInnerMessage(self, cmd, mi, *args, **kwargs):
        gid = mi.get_gid()
        uid = mi.get_uid()
        raw = mi.get_message()

        # 指定用户
        if uid:
            if isinstance(uid, int):
                uid = [uid]

            for u in uid:
                connection = Context.GData.map_client_connect.get(u)
                if connection:
                    if gid and gid != connection.gameId:
                        continue
                    Context.GData.send_to_client(u, raw, connection, cmd)
                else:
                    Context.Log.debug('send msg 0x%08X to offline player(%s):' % (cmd, u), raw)
            return True

        # 指定房间
        room = mi.get_room()
        if room:
            for u in Context.GData.map_client_connect:
                connection = Context.GData.map_client_connect[u]
                if gid and gid != connection.gameId:
                    continue
                if connection.room != room:
                    continue
                Context.GData.send_to_client(u, raw, connection, cmd)
            return True

        for u in Context.GData.map_client_connect:
            connection = Context.GData.map_client_connect[u]
            if gid and gid != connection.gameId:
                continue
            Context.GData.send_to_client(u, raw, connection, cmd)

        return False

    def onOuterMessage(self, cmd, raw, *args, **kwargs):
        if not self.connection.has_login():
            with self.connection.locker:
                if cmd == Message.MSG_SYS_USER_INFO | Message.ID_REQ:
                    mi = MsgPack.unpack(cmd, raw)
                    self.process_login(mi)
                    if self.connection.has_login():
                        self.send_to_entity(cmd, self.connection.userId, raw)
                    return True

        if self.connection.has_login():
            uid = self.connection.userId
            if Message.is_game_server(cmd):
                return self.send_to_game(cmd, uid, raw)
            elif cmd == Message.MSG_SYS_HOLD | Message.ID_REQ:
                return self.on_hold()
            elif cmd == Message.MSG_SYS_QUICK_START | Message.ID_REQ:
                return self.send_to_quick(cmd, uid, raw)
            elif cmd == Message.MSG_SYS_BIND_GAME | Message.ID_REQ:
                return self.on_bind_game(cmd, raw)
            elif cmd == Message.MSG_INNER_BROKEN:
                return self.process_broken(raw)
            else:
                return self.send_to_entity(cmd, uid, raw)

        return False

    def process_login(self, mi):
        uid = mi.get_param('userId')
        gid = mi.get_param('gameId')
        session = mi.get_param('session')
        result, desc = Account.check_forbidden(uid, gid, session)
        if result:
            mo = MsgPack(Message.MSG_SYS_USER_INFO | Message.ID_ACK)
            mo.set_error(result, desc)
            return Context.GData.send_to_client(uid, mo, self.connection)

        if uid in Context.GData.map_client_connect:  # 多点登陆
            # 清除原来的client
            connection = Context.GData.map_client_connect[uid]
            mo = MsgPack(Message.MSG_SYS_MULTIPLE_LOGIN | Message.ID_NTF)
            Context.Log.info('multi login', uid)
            Context.GData.send_to_client(connection.userId, mo, connection)
            connection.terminate_connection()

        Context.GData.map_client_connect[uid] = self.connection
        self.connection.login(uid, gid)
        return True

    def process_broken(self, mi):
        uid = mi.get_param('userId')
        gid = mi.get_param('gameId')
        mo = MsgPack(Message.MSG_INNER_BROKEN | Message.ID_NTF)
        gids = set(Context.GData.game_list)
        if gid:
            gids.add(gid)

        for gid in gids:
            key = 'location:%d:%d' % (gid, uid)
            sid = Context.RedisCache.hash_get_int(key, 'serverId', 0)
            if sid > 0:
                mo.set_param('gameId', gid)
                Context.GData.send_to_game(uid, mo, sid, gid=gid)
        return True

    def on_hold(self):
        mo = MsgPack(Message.MSG_SYS_HOLD | Message.ID_ACK)
        Context.GData.send_to_client(self.connection.userId, mo, self.connection)
        return True

    def on_bind_game(self, cmd, raw):
        mi = MsgPack.unpack(cmd, raw)
        gid = mi.get_param('gameId')
        if gid > 0:
            room = mi.get_param('room')
            self.connection.bind_game(gid, room)
            mo = MsgPack(Message.MSG_SYS_BIND_GAME | Message.ID_ACK)
            mo.set_param('gameId', gid)
            Context.GData.send_to_client(self.connection.userId, mo, self.connection)
        return True

    def send_to_entity(self, cmd, uid, raw):
        return Context.GData.send_to_entity(uid, raw, cmd=cmd, gid=self.connection.gameId)

    def send_to_quick(self, cmd, uid, raw):
        return Context.GData.send_to_quick(uid, raw, cmd=cmd, gid=self.connection.gameId)

    def send_to_game(self, cmd, uid, raw):
        gid = self.connection.gameId
        key = 'location:%d:%d' % (gid, uid)
        with self.connection.locker:
            sid = Context.RedisCache.hash_get_int(key, 'serverId', 0)

        if sid <= 0:
            ss = Context.GData.map_game_server.get(gid, [])
            if not ss:
                Context.Log.error('no server_id found', uid, gid, Context.GData.map_game_server)
                return False
            sid = ss[uid % len(ss)]

        Context.GData.send_to_game(uid, raw, sid, cmd, gid)

    def on_server_heart_beat(self):
        now_ts = Time.current_ts()
        rc_del = []
        for uid in Context.GData.map_client_connect:
            connection = Context.GData.map_client_connect[uid]
            if now_ts - connection.access_ts >= 60:
                rc_del.append(connection)
        for connection in rc_del:
            Context.Log.info('too long time no msg, terminate', connection.userId, connection.access_ts)
            connection.terminate_connection()
