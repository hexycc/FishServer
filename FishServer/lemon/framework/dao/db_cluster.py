#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2014-10-02

from db_single import RedisSingle
from framework.util.log import Logger


class RedisCluster(object):

    def __init__(self):
        self.__dbs__ = None

    def connect(self, param_list):
        if not isinstance(param_list, list):
            raise Exception('param_list error' + str(param_list))

        Logger.info('RedisCluster.__init__ ->', param_list)
        self.__dbs__ = []
        for param in param_list:
            single = RedisSingle()
            single.connect(param)
            self.__dbs__.append(single)

    def __get_db__(self, user_id):
        user_id = int(user_id)
        if user_id <= 0:
            raise Exception('user_id value error !! ' + str(user_id))

        rdb = self.__dbs__[user_id % len(self.__dbs__)]
        return rdb

    def execute(self, uid, *args, **kwargs):
        rdb = self.__get_db__(uid)
        return rdb.execute(*args, **kwargs)

    def load_lua_script(self, lua_alias, lua_script):
        sha = ''
        for rdb in self.__dbs__:
            sha = rdb.load_lua_script(lua_alias, lua_script)
        return sha

    def add_lua_alias(self, lua_alias, lua_sha, user_id=None):
        if user_id:
            rdb = self.__get_db__(user_id)
            rdb.add_lua_alias(lua_alias, lua_sha)
        else:
            for rdb in self.__dbs__:
                rdb.add_lua_alias(lua_alias, lua_sha)

    def execute_lua_alias(self, uid, lua_alias, *args, **kwargs):
        rdb = self.__get_db__(uid)
        return rdb.execute_lua_alias(lua_alias, *args, **kwargs)

    def delete(self, uid, key):
        rdb = self.__get_db__(uid)
        return rdb.delete(key)

    def expire(self, uid, key, expire_sec):
        rdb = self.__get_db__(uid)
        return rdb.expire(key, expire_sec)

    def expire_at(self, uid, key, expire_at):
        rdb = self.__get_db__(uid)
        return rdb.expire_at(key, expire_at)

    def hash_set(self, uid, key, field, value):
        rdb = self.__get_db__(uid)
        return rdb.hash_set(key, field, value)

    def hash_setnx(self, uid, key, field, value):
        rdb = self.__get_db__(uid)
        return rdb.hash_setnx(key, field, value)

    def hash_mget(self, uid, key, *args):
        rdb = self.__get_db__(uid)
        return rdb.hash_mget(key, *args)

    def hash_mset(self, uid, key, *args, **kwargs):
        rdb = self.__get_db__(uid)
        return rdb.hash_mset(key, *args, **kwargs)

    def hash_getall(self, uid, key):
        rdb = self.__get_db__(uid)
        return rdb.hash_getall(key)

    def hash_exists(self, uid, key, field):
        rdb = self.__get_db__(uid)
        return rdb.hash_exists(key, field)

    def hash_del(self, uid, key, *args):
        rdb = self.__get_db__(uid)
        return rdb.hash_del(key, *args)

    def hash_incrby(self, uid, key, field, delta=1):
        rdb = self.__get_db__(uid)
        return rdb.hash_incrby(key, field, delta)

    def hash_get(self, uid, key, field, default=None):
        rdb = self.__get_db__(uid)
        return rdb.hash_get(key, field, default)

    def hash_get_int(self, uid, key, field, default=None):
        rdb = self.__get_db__(uid)
        return rdb.hash_get_int(key, field, default)

    def hash_get_json(self, uid, key, field, default=None):
        rdb = self.__get_db__(uid)
        return rdb.hash_get_json(key, field, default)

    def hash_mget_as_dict(self, uid, key, *args):
        rdb = self.__get_db__(uid)
        return rdb.hash_mget_as_dict(key, *args)

    def list_lpop(self, uid, key, default=None):
        rdb = self.__get_db__(uid)
        return rdb.list_lpop(key, default)

    def list_lpop_int(self, uid, key, default=None):
        rdb = self.__get_db__(uid)
        return rdb.list_lpop_int(key, default)

    def list_lpop_json(self, uid, key, default=None):
        rdb = self.__get_db__(uid)
        return rdb.list_lpop_json(key, default)

    def list_lpush(self, uid, key, *args):
        rdb = self.__get_db__(uid)
        return rdb.list_lpush(key, *args)

    def list_rpop(self, uid, key, default=None):
        rdb = self.__get_db__(uid)
        return rdb.list_rpop(key, default)

    def list_rpop_int(self, uid, key, default=None):
        rdb = self.__get_db__(uid)
        return rdb.list_rpop_int(key, default)

    def list_rpop_json(self, uid, key, default=None):
        rdb = self.__get_db__(uid)
        return rdb.list_rpop_json(key, default)

    def list_rpush(self, uid, key, *args):
        rdb = self.__get_db__(uid)
        return rdb.list_rpush(key, *args)

    def list_range(self, uid, key, begin=0, end=-1):
        rdb = self.__get_db__(uid)
        return rdb.list_range(key, begin, end)

    def mincrby(self, uid, *args, **kwargs):
        rdb = self.__get_db__(uid)
        return rdb.mincrby(*args, **kwargs)

    def hash_mincrby(self, uid, key, *args, **kwargs):
        rdb = self.__get_db__(uid)
        return rdb.hash_mincrby(key, *args, **kwargs)
