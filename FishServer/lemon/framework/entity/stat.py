#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-05

from framework.util.tool import Tool
from framework.util.tool import Time
from framework.interface import IContext


class Stat(IContext):
    prefix = 'stat'
    format = '%Y-%m-%d'

    def get_daily_data(self, gid, *field):
        return self.get_day_data(gid, Time.current_time(self.format), *field)

    def get_day_data(self, gid, fmt, *field):
        key = '%s:%s:%s' % (self.prefix, gid, fmt)
        if not field:
            return self.ctx.RedisStat.hash_getall(key)
        elif len(field) == 1:
            return self.ctx.RedisStat.hash_get(key, *field)
        else:
            return self.ctx.RedisStat.hash_mget(key, *field)

    def set_daily_data(self, gid, *args, **kwargs):
        l = Tool.dict2list(kwargs)
        l.extend(args)
        if len(l) % 2 != 0:
            raise Exception('error param')
        key = '%s:%s:%s' % (self.prefix, gid, Time.current_time(self.format))
        return self.ctx.RedisStat.hash_mset(key, *l)

    def setnx_daily_data(self, gid, field, value):
        key = '%s:%s:%s' % (self.prefix, gid, Time.current_time(self.format))
        return self.ctx.RedisStat.hash_setnx(key, field, value)

    def incr_daily_data(self, gid, field, delta=1):
        key = '%s:%s:%s' % (self.prefix, gid, Time.current_time(self.format))
        return self.ctx.RedisStat.hash_incrby(key, field, delta)

    def mincr_daily_data(self, gid, *args, **kwargs):
        key = '%s:%s:%s' % (self.prefix, gid, Time.current_time(self.format))
        return self.ctx.RedisStat.hash_mincrby(key, *args, **kwargs)

Stat = Stat()
