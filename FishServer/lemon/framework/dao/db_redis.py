#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2014-10-01

from twisted.internet import reactor
from txredis import RedisClientFactory
from framework.util.log import Logger
from framework.util.tool import Tool
from framework.entity.manager import TaskManager


class DbRedis(object):
    __CONNECT_REDIS__ = {}
    __LUA_ALIAS__ = {}

    def connect(self, *args):
        if len(args) == 1:
            host = str(args[0]['host'])
            port = int(args[0]['port'])
            db = int(args[0]['db'])
        elif len(args) == 3:
            host = str(args[0])
            port = int(args[1])
            db = int(args[2])
        else:
            raise Exception("error args, connect(ip, port, db) or connect({'host': host, 'port': port, 'db': db}")

        self.__redis_key__ = 'redis:%s:%s:%s' % (host, port, db)
        if self.__redis_key__ in self.__CONNECT_REDIS__:
            self.__redisPool__ = self.__CONNECT_REDIS__[self.__redis_key__].__redisPool__
            self.__sha_map__ = self.__CONNECT_REDIS__[self.__redis_key__].__sha_map__
            return self.__CONNECT_REDIS__[self.__redis_key__]
        else:
            tasklet = TaskManager.current()
            factory = RedisClientFactory(db=db)
            reactor.connectTCP(host, port, factory)
            tasklet.wait_for_deferred(factory.deferred)
            self.__redisPool__ = factory
            self.__CONNECT_REDIS__[self.__redis_key__] = self
            return self.__CONNECT_REDIS__[self.__redis_key__]

    def __init__(self):
        self.__redisPool__ = None
        self.__sha_map__ = {}
        self.__redis_key__ = None

    def execute(self, *args, **kwargs):
        tasklet = TaskManager.current()
        # d = self.__redisPool__.execute_command(*args, **kwargs)
        d = self.__redisPool__.client.send(*args)
        result = tasklet.wait_for_deferred(d)
        Logger.debug_redis(self.__redis_key__, args, kwargs, '=>', result)
        return result

    def load_lua_script(self, lua_alias, lua_script):
        sha = self.execute('script', 'load', lua_script)
        self.__sha_map__[lua_alias] = sha
        DbRedis.__LUA_ALIAS__[lua_alias] = lua_script
        Logger.info(self.__redis_key__, 'load_lua_script', lua_alias, sha, lua_script)
        return sha

    def add_lua_alias(self, lua_alias, lua_sha):
        self.__sha_map__[lua_alias] = lua_sha
        Logger.info(self.__redis_key__, 'add_lua_alias', lua_alias, lua_sha)

    def execute_lua_alias(self, lua_alias, *args, **kwargs):
        if lua_alias not in self.__sha_map__:
            lua_script = DbRedis.__LUA_ALIAS__[lua_alias]
            self.load_lua_script(lua_alias, lua_script)
        sha = self.__sha_map__[lua_alias]
        result = self.execute('evalsha', sha, len(args), *args, **kwargs)
        return result

    # functional method
    def delete(self, *key):
        return self.execute('del', *key)

    def rename(self, key, new_key):
        return self.execute('rename', key, new_key)

    def expire(self, key, expire_sec):
        return self.execute('expire', key, expire_sec)

    def expire_at(self, key, expire_at):
        return self.execute('expireat', key, expire_at)

    def get(self, key):
        return self.execute('get', key)

    def set(self, key, value):
        return self.execute('set', key, value)

    def setex(self, key, value, second):
        return self.execute('setex', key, second, value)

    def incrby(self, key, delta=1):
        return self.execute('incrby', key, delta)

    def list_rpush(self, key, *args):
        return self.execute('rpush', key, *args)

    def list_lpush(self, key, *args):
        return self.execute('lpush', key, *args)

    def list_range(self, key, begin=0, end=-1):
        return self.execute('lrange', key, begin, end)

    def list_lpop(self, key):
        return self.execute('lpop', key)

    def list_rem(self, key, value):
        return self.execute('lrem', key, 0, value)

    def set_add(self, key, *args):
        return self.execute('sadd', key, *args)

    def set_ismember(self, key, value):
        return self.execute('sismember', key, value)

    def set_rem(self, key, value):
        return self.execute('srem', key, value)

    def set_members(self, key):
        return self.execute('smembers', key)

    def hash_get(self, key, field):
        return self.execute('hget', key, field)

    def hash_set(self, key, field, value):
        return self.execute('hset', key, field, value)

    def hash_setnx(self, key, field, value):
        return self.execute('hsetnx', key, field, value)

    def hash_mget(self, key, *args):
        return self.execute('hmget', key, *args)

    def hash_mset(self, key, *args, **kwargs):
        l = []
        l.extend(args)
        for k, v in kwargs.iteritems():
            l.append(k)
            l.append(v)
        return self.execute('hmset', key, *l)

    def hash_getall(self, key):
        l = self.execute('hgetall', key)
        return Tool.list2dict(l)

    def hash_exists(self, key, field):
        return self.execute('hexists', key, field)

    def hash_del(self, key, *args):
        return self.execute('hdel', key, *args)

    def hash_incrby(self, key, field, delta=1):
        return self.execute('hincrby', key, field, delta)

    def zset_score(self, key, member):
        return self.execute('zscore', key, member)

    def zset_add(self, key, *args, **kwargs):
        l = []
        l.extend(args)
        for k, v in kwargs.iteritems():
            l.append(v)
            l.append(k)
        return self.execute('zadd', key, *l)

    def zset_card(self, key):
        return self.execute('zcard', key)

    def zset_range(self, key, begin, end, withscores=True):
        if withscores:
            return self.execute('zrange', key, begin, end, 'withscores')
        else:
            return self.execute('zrange', key, begin, end)

    def zset_rem(self, key, member):
        return self.execute('zrem', key, member)

    def zset_incrby(self, key, member, delta):
        return self.execute('zincrby', key, delta, member)

    def zset_revrange(self, key, begin, end, withscores=True):
        if withscores:
            return self.execute('zrevrange', key, begin, end, 'withscores')
        else:
            return self.execute('zrevrange', key, begin, end)

    def zset_count(self, key, begin, end):
        return self.execute('zcount', key, begin, end)

    def zset_revrank(self, key, member):
        return self.execute('zrevrank', key, member)

    def mincrby(self, *args, **kwargs):
        l = self.__make_arg_list(*args, **kwargs)
        return self.execute_lua_alias('multi_incr', 1, *l)

    def hash_mincrby(self, key, *args, **kwargs):
        l = self.__make_arg_list(*args, **kwargs)
        return self.execute_lua_alias('multi_incr', 2, key, *l)

    def __make_arg_list(self, *args, **kwargs):
        l = list(args)
        if kwargs:
            _ = Tool.dict2list(kwargs)
            l.extend(_)
        if len(l) < 2 or len(l) % 2 != 0:
            raise Exception('error count')

        for i in xrange(0, len(l), 2):
            try:
                int(l[i + 1])
            except Exception, e:
                raise Exception('error param %s' % l)
        return l
