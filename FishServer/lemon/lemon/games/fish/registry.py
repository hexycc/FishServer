#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-26

from framework.context import Context


class FishRegistry(object):
    def get_table(self, tid):
        return Context.GData.online_table.get(tid)

    def create_table(self, gid, tid):
        if tid not in Context.GData.online_table:
            from table import FishTable as Table
            t = Table(gid, tid)
            if not t.on_init():
                return None
            Context.GData.online_table[tid] = t

        return Context.GData.online_table[tid]

    def get_player(self, uid):
        return Context.GData.online_user.get(uid)

    def create_player(self, uid):
        if uid not in Context.GData.online_user:
            from player import FishPlayer
            p = FishPlayer(uid)
            if not p.on_init():
                return None
            Context.GData.online_user[uid] = p

        return Context.GData.online_user[uid]


FishRegistry = FishRegistry()
