#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-06-01

from framework.context import Context
from framework.entity.const import Message


class Game(object):
    def onMessage(self, cmd, uid, gid, mi):
        if cmd == Message.MSG_INNER_TIMER:
            tid = mi.get_param('tableId')
            if tid:
                registry = Context.get_module(gid, 'registry')
                table = registry.get_table(tid)
                if table:
                    with Context.GData.table_locker[tid]:
                        table.onTimer(cmd, gid, mi)
                else:
                    Context.Log.info(tid, 'table not exist', mi)
            else:
                Context.Log.info('miss table id', mi)
        else:
            registry = Context.get_module(gid, 'registry')
            player = registry.create_player(uid)
            if player:
                player.on_message(cmd, gid, mi)
            else:
                Context.Log.debug('no player found', mi)
