#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-12-17

from framework.context import Context


class Quick(object):
    @classmethod
    def get_free_table(cls, gid):
        table_id = Context.RedisCache.list_lpop_int('quick:%d:0' % gid)
        if table_id is None:
            key = 'cache.%d.info.hash' % gid
            Context.RedisCache.hash_setnx(key, 'max.table.id', 1000)
            table_id = Context.RedisCache.hash_incrby(key, 'max.table.id', 1)
        return table_id
