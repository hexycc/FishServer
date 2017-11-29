#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-24

from framework.util.tool import Time
from framework.context import Context
from framework.entity.const import Enum
from framework.entity.const import Message
from framework.entity.msgpack import MsgPack


class Table(object):
    MAX_PLAYER_CNT = 4

    def __init__(self, gid, tid):
        self.gid = gid
        self.tid = tid
        self.playing = False
        self.recycle_ts = 0
        self.all_user = {}          # 所有玩家
        self.table_info = {}        # 配桌信息
        self.room_config = {}       # 房间配置
        self._info('game %d create table' % gid)

    def _log(self, level, *args):
        import inspect
        frame = inspect.currentframe().f_back.f_back
        func_name = frame.f_code.co_name
        Context.Log.log(level, '%s(ID = %4d)::%s,' % (self.__class__.__name__, self.tid, func_name), *args)

    def _info(self, *args):
        self._log(Context.Log.INFO, *args)

    def _debug(self, *args):
        self._log(Context.Log.DEBUG, *args)

    def _warn(self, *args):
        self._log(Context.Log.WARN, *args)

    def _error(self, *args):
        self._log(Context.Log.ERROR, *args)

    def on_init(self):
        self.playing = False
        self.recycle_ts = 0
        return True

    def __notify_join_table(self, uid, reconnect=False, viewer=False):
        # 通知其他人(包括自己)该用户进入房间及相关信息
        if reconnect:
            evt = [{
                'type': Enum.table_event_reconnect,
                'userId': uid,
            }]
        elif viewer:
            evt = [{
                'type': Enum.table_event_viewer_join_table,
                'userId': uid,
            }]
        else:
            evt = [{
                'type': Enum.table_event_join_table,
                'userId': uid,
            }]

        user_info = self.get_user_info(uid)
        if user_info:
            evt.append({
                'type': Enum.table_event_user_info,
                'userId': uid,
                'userInfo': user_info,
            })

        game_info = self.get_game_info(uid)
        if game_info:
            evt.append({
                'type': Enum.table_event_game_info,
                'userId': uid,
                'gameInfo': game_info,
            })
        all_user = self.get_all_user()
        self.notify_event(evt, all_user=all_user)

        # 通知回归玩家,其他人的gameinfo及userinfo
        evt = []
        table_info = self.get_table_info()
        if table_info:
            evt.append({
                'type': Enum.table_event_table_info,
                'tableInfo': table_info
            })

        for user_id, identity in all_user.iteritems():
            if user_id != uid:
                user_info = self.get_user_info(user_id)
                if user_info:
                    evt.append({
                        'type': Enum.table_event_user_info,
                        'userId': user_id,
                        'userInfo': user_info,
                    })

                game_info = self.get_game_info(user_id)
                if game_info:
                    evt.append({
                        'type': Enum.table_event_game_info,
                        'userId': user_id,
                        'gameInfo': game_info,
                    })
        if evt:
            self.notify_event(evt, all_user=uid)

        self.recycle_ts = 0

    def update_table_status(self, status):
        key = 'table:%d:%d' % (self.gid, self.tid)
        Context.RedisCache.hash_mset(key, 'status', status, 'fresh_ts', Time.current_ts())

    def is_join_legal(self, uid):
        status = Context.Online.get_location_status(uid, self.gid)
        if status is None:
            self._warn('get location status failed')
            return False
        elif status != 0:
            Context.Online.del_location(uid, self.gid)
            return False

        return uid in self.table_info

    def remove_player(self, uid):
        result = Context.RedisCache.execute_lua_alias('kick_off', uid, self.gid, self.MAX_PLAYER_CNT, self.tid)
        self._info('kick off', uid, result)

    def get_by_identity_type(self, identity_type):
        count = 0
        for _, player in self.all_user.iteritems():
            if player.identity == identity_type:
                count += 1
        return count

    def get_by_state(self, state):
        count = 0
        for _, player in self.all_user.iteritems():
            if player.state == state:
                count += 1
        return count

    @property
    def room_type(self):
        return self.room_config['room_type']

    @property
    def room_name(self):
        return self.room_config['room_name']

    def join_table(self, uid):
        if self.recycle_ts:
            if not self.on_init():
                self._warn('init logic failed')
                return Enum.join_table_failed_unknown

        result = self.on_join(uid)
        self._info('join result', result)
        if result == 0:
            # 返回加入成功
            ack = MsgPack(Message.MSG_SYS_JOIN_TABLE | Message.ID_ACK)
            Context.GData.send_to_connect(uid, ack)
            self.__notify_join_table(uid)
        else:
            state = self.get_user_state(uid)
            if state == Enum.user_state_playing:
                result = self.on_offline(uid)
                state = Enum.user_state_offline
                self._info('user playing simulate user state as', state)
            self._info('test reconnect with user state', state)
            if state == Enum.user_state_offline or state == Enum.user_state_getout:
                result = self.__reconnect(uid)
        self._info('join result', result)
        return result

    def sit_down(self, uid, sid):
        result = self.on_sit_down(uid, sid)
        if result == 0:
            ack = MsgPack(Message.MSG_SYS_SIT_DOWN | Message.ID_ACK)
            Context.GData.send_to_connect(uid, ack)

            evt = [{
                'type': Enum.table_event_sit_down,
                'userId': uid,
                'seatId': sid,
            }]
            self._info('user %d sit down %d' % (uid, sid))
            self.notify_event(evt)
        else:
            state = self.get_user_state(uid)
            if state == Enum.user_state_playing:
                result = self.on_offline(uid)
                state = Enum.user_state_offline
                self._info('user playing simulate user state as', state)
                self._info('test reconnect with user state', state)
                result = self.__reconnect(uid)
        return result

    def leave_table(self, uid):
        if self.playing:
            return Enum.leave_table_failed_playing

        result = self.on_leave(uid)
        if result == 0:
            ack = MsgPack(Message.MSG_SYS_LEAVE_TABLE | Message.ID_ACK)
            Context.GData.send_to_connect(uid, ack)

            evt = [{
                'type': Enum.table_event_leave_table,
                'userId': uid,
            }]
            self.notify_event(evt, exclude=uid)
        return result

    def offline(self, uid):
        result = self.on_offline(uid)
        if result == 0:
            evt = [{
                'type': Enum.table_event_offline,
                'userId': uid,
            }]
            self.notify_event(evt)

        return result

    def __reconnect(self, uid):
        self.__notify_join_table(uid, reconnect=True)
        self.on_reconnect(uid)
        return 0

    def notify_event(self, event, exclude=None, all_user=None):
        ntf = MsgPack(Message.MSG_SYS_TABLE_EVENT | Message.ID_NTF)
        ntf.set_param('event', event)
        self.table_broadcast(ntf, exclude, all_user)

    def table_broadcast(self, mo, exclude=None, all_user=None):
        if isinstance(all_user, int):
            all_user = [all_user]
        elif not all_user:
            all_user = self.get_all_user()
        if isinstance(exclude, int):
            exclude = [exclude]

        for uid in all_user:
            if not exclude or uid not in exclude:
                Context.GData.send_to_connect(uid, mo)

    @property
    def table_id(self):
        return self.tid

    @property
    def is_playing(self):
        return self.playing

    def set_game_start(self):
        self.playing = True
        evt = [{'type': Enum.table_event_game_start}]
        self.notify_event(evt)

    def set_game_end(self):
        self.playing = False
        evt = [{'type': Enum.table_event_game_end}]
        self.notify_event(evt)

    def kick_off_user(self, reason, kicked_uid, kicker_uid=None):
        evt = [{
            'type': Enum.table_event_kick_off,
            'userId': kicked_uid,
            'reason': reason,
        }]

        if kicker_uid and kicker_uid > 0:
            evt[0]['kicker'] = kicker_uid

        self.notify_event(evt)

        registry = Context.get_module(self.gid, 'registry')
        player = registry.get_player(kicked_uid)
        if player:
            player.leave_table()

        return 0

    kick_off_viewer = kick_off_user

    def kick_off_robot(self, kicked_uid):
        evt = [{
            'type': Enum.table_event_kick_off,
            'userId': kicked_uid,
        }]

        self.notify_event(evt)
        return 0

    def set_recycle_flag(self):
        self.recycle_ts = Time.current_ts()
        return 0

    def flush_game_info(self, uid):
        game_info = self.get_game_info(uid)
        if game_info:
            evt = [{
                'type': Enum.table_event_game_info,
                'userId': uid,
                'gameInfo': game_info,
            }]
            self.notify_event(evt)
        return 0

    def notify_trustee(self, uid, cancel):
        t = Enum.table_event_cancel_trustee if cancel else Enum.table_event_trustee
        evt = [{
            'type': t,
            'userId': uid,
        }]
        self.notify_event(evt)
        return 0

    def get_all_user(self):
        kvs = {}
        for k, v in self.all_user.iteritems():
            if v.state != Enum.user_state_offline:
                kvs[k] = v.identity
        return kvs

    def get_game_info(self, uid):
        game_info = None
        if uid in self.all_user:
            game_info = self.all_user[uid].game_info
        return game_info

    def get_user_info(self, uid):
        user_info = None
        if uid in self.all_user:
            user_info = self.all_user[uid].user_info
        return user_info

    def get_table_info(self):
        info = []
        for uid, player in self.all_user.iteritems():
            if player.state != Enum.user_state_offline:
                item = {
                    'userId': uid,
                    'identity': Enum.identity_type_player,
                    'state': player.state,
                }
                if player.sid is not None:
                    item['seatId'] = player.sid
                info.append(item)
        return {'info': info}

    def get_user_state(self, uid):
        if uid in self.all_user:
            return self.all_user[uid].state
        else:
            return Enum.user_state_free
