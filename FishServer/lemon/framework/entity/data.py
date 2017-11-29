#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2014-10-14

from framework.util.tool import Tool
from framework.interface import IContext
from framework.interface import ICallable


class Data(IContext, ICallable):

    def __init__(self):
        pass

    # user attr
    def exists_attr(self, uid, attr):
        return self.ctx.RedisCluster.hash_exists(uid, 'user:%d' % uid, attr)

    def get_attr(self, uid, attr, default=None):
        return self.ctx.RedisCluster.hash_get(uid, 'user:%d' % uid, attr, default)

    def get_attr_int(self, uid, attr, default=None):
        return self.ctx.RedisCluster.hash_get_int(uid, 'user:%d' % uid, attr, default)

    def get_attr_json(self, uid, attr, default=None):
        return self.ctx.RedisCluster.hash_get_json(uid, 'user:%d' % uid, attr, default)

    def set_attr(self, uid, attr, value):
        return self.ctx.RedisCluster.hash_set(uid, 'user:%d' % uid, attr, value)

    def setnx_attr(self, uid, attr, value):
        return self.ctx.RedisCluster.hash_setnx(uid, 'user:%d' % uid, attr, value)

    def get_attrs(self, uid, attrs):
        return self.ctx.RedisCluster.hash_mget(uid, 'user:%d' % uid, *attrs)

    def get_attrs_dict(self, uid, attrs):
        return self.ctx.RedisCluster.hash_mget_as_dict(uid, 'user:%d' % uid, *attrs)

    def get_all(self, uid):
        return self.ctx.RedisCluster.hash_getall(uid, 'user:%d' % uid)

    def set_attrs(self, uid, attrs, values):
        l = Tool.make_list(attrs, values)
        return self.ctx.RedisCluster.hash_mset(uid, 'user:%d' % uid, *l)

    def set_attrs_dict(self, uid, kvs):
        return self.ctx.RedisCluster.hash_mset(uid, 'user:%d' % uid, **kvs)

    def del_attrs(self, uid, *attrs):
        return self.ctx.RedisCluster.hash_del(uid, 'user:%d' % uid, *attrs)

    # game attr
    def get_game_attr(self, uid, gid, attr, default=None):
        return self.ctx.RedisCluster.hash_get(uid, 'game:%d:%d' % (gid, uid), attr, default)

    def get_game_attr_int(self, uid, gid, attr, default=None):
        return self.ctx.RedisCluster.hash_get_int(uid, 'game:%d:%d' % (gid, uid), attr, default)

    def get_game_attr_json(self, uid, gid, attr, default=None):
        return self.ctx.RedisCluster.hash_get_json(uid, 'game:%d:%d' % (gid, uid), attr, default)

    def set_game_attr(self, uid, gid, attr, value):
        return self.ctx.RedisCluster.hash_set(uid, 'game:%d:%d' % (gid, uid), attr, value)

    def setnx_game_attr(self, uid, gid, attr, value):
        return self.ctx.RedisCluster.hash_setnx(uid, 'game:%d:%d' % (gid, uid), attr, value)

    def get_game_attrs(self, uid, gid, attrs):
        return self.ctx.RedisCluster.hash_mget(uid, 'game:%d:%d' % (gid, uid), *attrs)

    def get_game_attrs_dict(self, uid, gid, attrs):
        return self.ctx.RedisCluster.hash_mget_as_dict(uid, 'game:%d:%d' % (gid, uid), *attrs)

    def get_game_all(self, uid, gid):
        return self.ctx.RedisCluster.hash_getall(uid, 'game:%d:%d' % (gid, uid))

    def set_game_attrs(self, uid, gid, attrs, values):
        l = Tool.make_list(attrs, values)
        return self.ctx.RedisCluster.hash_mset(uid, 'game:%d:%d' % (gid, uid), *l)

    def set_game_attrs_dict(self, uid, gid, kvs):
        return self.ctx.RedisCluster.hash_mset(uid, 'game:%d:%d' % (gid, uid), **kvs)

    def hincr_game(self, uid, gid, attr, delta):
        return self.ctx.RedisCluster.hash_incrby(uid, 'game:%d:%d' % (gid, uid), attr, delta)

    def hmincr_game(self, uid, gid, *args, **kwargs):
        return self.ctx.RedisCluster.hash_mincrby(uid, 'game:%d:%d' % (gid, uid), *args, **kwargs)

    def del_game_attrs(self, uid, gid, *attrs):
        return self.ctx.RedisCluster.hash_del(uid, 'game:%d:%d' % (gid, uid), *attrs)


Data = Data()
