#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-05-06

import copy
import json
from framework.util.locker import LockAttr
from framework.util.log import Logger
from framework.util.strutil import Strutil
from framework.util.tool import Time
from framework.dao.db_cluster import RedisCluster
from framework.dao.db_single import RedisSingle
from framework.entity.configure import Configure
from framework.entity.const import Const
from framework.entity.const import Enum
from framework.entity.const import FlagType
from framework.entity.const import Message
from framework.entity.daily import Daily
from framework.entity.data import Data
from framework.entity.gdata import GData
from framework.entity.globals import Global
from framework.entity.online import Online
from framework.entity.stat import Stat
from framework.entity.userattr import UserAttr
from framework.entity.webpage import WebPage
from framework.entity.keyword_filter import KeywordFilter


class Context(object):
    def __init__(self):
        self.RedisConfig = RedisSingle()
        self.RedisCluster = RedisCluster()
        self.RedisMix = RedisSingle()
        self.RedisPay = RedisSingle()
        self.RedisCache = RedisSingle()
        self.RedisStat = RedisSingle()

        self.Log = Logger
        self.GData = GData
        self.Configure = Configure
        self.UserAttr = UserAttr
        self.Data = Data
        self.Daily = Daily
        self.Stat = Stat
        self.Strutil = Strutil
        self.Global = Global
        self.WebPage = WebPage
        self.Online = Online

        self.LockAttr = LockAttr
        self.Message = Message
        self.FlagType = FlagType
        self.Enum = Enum
        self.Const = Const
        self.Time = Time
        self.KeywordFilter = KeywordFilter

    @classmethod
    def json_loads(cls, s):
        return json.loads(s)

    @classmethod
    def json_dumps(cls, o, **kwargs):
        if 'separators' not in kwargs:
            kwargs['separators'] = (',', ':')
        return json.dumps(o, **kwargs)

    @classmethod
    def copy_json_obj(cls, j):
        t = json.dumps(j)
        return json.loads(t)

    @classmethod
    def copy_obj(cls, o):
        return copy.deepcopy(o)

    @classmethod
    def get_module(cls, gid, name, default=None):
        from lemon import classMap
        _cls = classMap.get(gid, {})
        return _cls.get(name, default)

    def tasklet(self):
        from framework.entity.manager import TaskManager
        return TaskManager.current()

    def init_ctx(self):
        for name in dir(self):
            if name.startswith('__'):
                continue
            obj = getattr(self, name)
            _init_ctx = getattr(obj, 'init_ctx', None)
            if callable(_init_ctx):
                _init_ctx()
        setattr(self, 'init_ctx', None)
        self.LockAttr.lock(self)

    def init_with_redis_json(self, redis_json, init_config=True):
        if init_config:
            self.RedisConfig.connect(redis_json['config'])
        self.RedisCluster.connect(redis_json['cluster'])
        self.RedisMix.connect(redis_json['mix'])
        self.RedisPay.connect(redis_json['pay'])
        self.RedisStat.connect(redis_json['stat'])
        self.RedisCache.connect(redis_json['cache'])
        setattr(self, 'init_with_redis_json', None)
        setattr(self, 'init_with_redis_key', None)

    def init_with_redis_key(self, redis_key):
        if isinstance(redis_key, str):
            host, port, db = redis_key.split(':')
        else:
            host, port, db = redis_key['host'], redis_key['port'], redis_key['db']
        self.RedisConfig.connect(host, port, db)
        redis_json = self.Configure.get_global_item_json('redis.config')
        self.init_with_redis_json(redis_json, False)

    def load_lua_script(self):
        if getattr(self, 'init_with_redis_json', None):
            raise Exception('not init ctx')
        alias_sha = self.Configure.get_global_item_json('redis.lua')
        if alias_sha:
            for alias, sha in alias_sha.iteritems():
                self.RedisCluster.add_lua_alias(alias, sha)
                self.RedisMix.add_lua_alias(alias, sha)
                self.RedisPay.add_lua_alias(alias, sha)
                self.RedisStat.add_lua_alias(alias, sha)
                self.RedisCache.add_lua_alias(alias, sha)


Context = Context()
Context.init_ctx()
