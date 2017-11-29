#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-27

from framework.interface import IContext
from framework.interface import ICallable
from framework.util.tool import Time


class Online(IContext, ICallable):
    def get_location(self, uid, gid):
        key = 'location:%d:%d' % (gid, uid)
        attrs = ['room_type', 'table_id', 'seat_id', 'status', 'fresh_ts', 'serverId']
        kvs = self.ctx.RedisCache.hash_mget_as_dict(key, *attrs)
        if not kvs:
            return True, None

        if len(kvs) != len(attrs):
            self.ctx.Log.info(uid, 'info illegal', kvs)
            table_id = int(kvs.get('table_id', -1))
            res = self.__kick_off(uid, gid, table_id)
            self.ctx.Log.debug('kick off', uid, gid, res)
            return False, None
        else:
            for k in kvs:
                kvs[k] = int(kvs[k])
            return True, kvs

    def get_location_status(self, uid, gid):
        key = 'location:%d:%d' % (gid, uid)
        return self.ctx.RedisCache.hash_get_int(key, 'status')

    def set_location(self, uid, gid, server_id, room_type, table_id, seat_id, status, fresh_time, **kwargs):
        key = 'location:%d:%d' % (gid, uid)
        kvs = {
            'serverId': server_id,
            'room_type': room_type,
            'table_id': table_id,
            'seat_id': seat_id,
            'status': status,
            'fresh_ts': fresh_time,
        }
        kvs.update(kwargs)
        self.ctx.RedisCache.hash_mset(key, **kvs)
        return True

    def set_location_status(self, uid, gid, status, fresh_time=None):
        key = 'location:%d:%d' % (gid, uid)
        if not fresh_time:
            fresh_time = Time.current_ts()
        self.ctx.RedisCache.hash_mset(key, 'status', status, 'fresh_ts', fresh_time)
        return True

    def del_location(self, uid, gid):
        key = 'location:%d:%d' % (gid, uid)
        self.ctx.RedisCache.delete(key)
        return True

    def incr_online(self, gid, rid, online=True):
        if online:
            return self.ctx.RedisCache.hash_incrby('online.info.%d' % gid, rid, 1)
        else:
            return self.ctx.RedisCache.hash_incrby('online.info.%d' % gid, rid, -1)

    def get_online(self, gid, *rid):
        return self.ctx.RedisCache.hash_mget('online.info.%d' % gid, *rid)


Online = Online()
