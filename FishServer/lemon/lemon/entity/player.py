#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-24

from framework.util.tool import Time
from framework.context import Context
from framework.entity.const import Enum
from framework.entity.const import Message
from framework.entity.msgpack import MsgPack


class Player(object):
    def __init__(self, uid):
        self.uid = uid
        self.owner = None
        self.tid = None
        self.user_info = None
        self.game_info = None
        self.gid = None
        self.sid = None
        self.online_ts = 0
        self.leave_ts = 0
        self.offline = False

    def _log(self, level, *args):
        import inspect
        frame = inspect.currentframe().f_back.f_back
        func_name = frame.f_code.co_name
        Context.Log.log(level, '%s(ID = %4d)::%s,' % (self.__class__.__name__, self.uid, func_name), *args)

    def _info(self, *args):
        self._log(Context.Log.INFO, *args)

    def _debug(self, *args):
        self._log(Context.Log.DEBUG, *args)

    def _warn(self, *args):
        self._log(Context.Log.WARN, *args)

    def _error(self, *args):
        self._log(Context.Log.ERROR, *args)

    def on_init(self):
        return True

    @property
    def table_id(self):
        return self.tid

    @property
    def table(self):
        return self.owner

    @table.setter
    def table(self, _table):
        self.owner = _table
        self.tid = _table.tid

    def leave_table(self):
        now_ts = Time.current_ts()
        if self.online_ts and self.uid > 0 and self.gid > 0:
            Context.Daily.incr_daily_data(self.uid, self.gid, 'online_sec', now_ts - self.online_ts)
            self.online_ts = 0
        self.user_info = None
        self.game_info = None
        self.gid = None
        self.sid = None
        self.tid = None
        self.owner = None
        self.leave_ts = now_ts
        self.offline = True

    def on_message(self, cmd, gid, msg):
        tid = msg.get_param('tableId', self.tid)
        with Context.GData.table_locker[tid]:
            if cmd == Message.MSG_SYS_JOIN_TABLE | Message.ID_REQ:
                result = self.on_join_table(gid, msg)
            elif cmd == Message.MSG_SYS_SIT_DOWN | Message.ID_REQ:
                result = self.on_sit_down(msg)
            elif cmd == Message.MSG_SYS_LEAVE_TABLE | Message.ID_REQ:
                result = self.on_leave_table(msg)
            elif cmd == Message.MSG_INNER_BROKEN | Message.ID_NTF:
                result = self.on_broken(msg)
            else:
                result = 0
                table = Context.GData.online_table.get(self.tid)
                if table:
                    result = table.on_client_message(self.uid, cmd, msg)

            if isinstance(result, MsgPack):
                Context.GData.send_to_connect(self.uid, result)

    def on_join_table(self, gid, msg):
        ack = MsgPack(Message.MSG_SYS_JOIN_TABLE | Message.ID_ACK)
        tid = msg.get_param('tableId')
        self._info('player req to join table', tid)
        self.offline = False
        if self.tid > 0 and self.tid != tid:
            self.offline = True
            return ack.set_error(Enum.join_table_failed_multi)

        registry = Context.get_module(gid, 'registry')
        table = registry.create_table(gid, tid)
        if not table:
            self.offline = True
            return ack.set_error(Enum.join_table_failed_id)

        result = table.join_table(self.uid)
        if result != 0:
            self.offline = True
            return ack.set_error(result)

        self.table = table
        self.online_ts = Time.current_ts()

        sid = msg.get_param('seatId')
        if sid is not None:
            return self.on_sit_down(msg)
        return result

    def on_sit_down(self, msg):
        sid = msg.get_param('seatId')
        self._info('player req to sit table %d at %d' % (self.tid, sid))
        ack = MsgPack(Message.MSG_SYS_SIT_DOWN | Message.ID_ACK)
        table = Context.GData.online_table.get(self.tid)
        if not table:
            self._error('not exists the table', self.tid)
            return ack.set_error(Enum.sit_down_failed_id)
        result = table.sit_down(self.uid, sid)
        if result != 0:
            return ack.set_error(result)

        return result

    def on_leave_table(self, msg):
        self._info('player req to leave table', self.tid)
        ack = MsgPack(Message.MSG_SYS_LEAVE_TABLE | Message.ID_ACK)
        table = Context.GData.online_table.get(self.tid)
        if not table:
            self._error('not exists the table', self.tid)
            return ack.set_error(Enum.leave_table_failed_id)

        result = table.leave_table(self.uid)
        if result != 0:
            return ack.set_error(result)

        return result

    def on_broken(self, msg):
        self._info('ntf offline in table', self.tid)
        if self.tid and self.tid > 0:
            table = Context.GData.online_table.get(self.tid)
            if table:
                result = table.offline(self.uid)
                if result != 0:
                    self._info('%d offline result %d' % (self.tid, result))

        return 0
