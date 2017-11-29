#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-20

from framework.core.tasklet import server
from framework.entity.msgpack import MsgPack
from framework.context import Context


class GameTasklet(server.BasicServerTasklet):
    def onInnerMessage(self, cmd, mi, *args, **kwargs):
        uid = mi.get_uid()
        gid = mi.get_gid()
        raw = mi.get_message()
        mi = MsgPack.unpack(cmd, raw)
        gid = mi.get_param('gameId', gid)
        game = Context.get_module(gid, 'game')
        with Context.GData.user_locker[uid]:
            if game:
                game.onMessage(cmd, uid, gid, mi)
            else:
                Context.Log.warn('no game found', mi)
