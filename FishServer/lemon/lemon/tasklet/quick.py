#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-06

from framework.core.tasklet import server
from framework.entity.msgpack import MsgPack
from framework.context import Context


class QuickTasklet(server.BasicServerTasklet):
    def onInnerMessage(self, cmd, mi, *args, **kwargs):
        uid = mi.get_uid()
        gid = mi.get_gid()
        raw = mi.get_message()
        mi = MsgPack.unpack(cmd, raw)
        gid = mi.get_param('gameId', gid)
        quick = Context.get_module(gid, 'quick')
        with Context.GData.server_locker:
            if quick:
                quick.onMessage(cmd, uid, gid, mi)
            else:
                Context.Log.warn('error msg', cmd, mi)
