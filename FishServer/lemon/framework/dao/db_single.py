#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-11

import json
from db_redis import DbRedis
from framework.util.log import Logger


class RedisSingle(DbRedis):
    def connect(self, *params):
        Logger.info('RedisSingle.__init__ ->', *params)
        DbRedis.connect(self, *params)

    def get(self, key, default=None):
        _ret = DbRedis.get(self, key)
        if _ret is None:
            _ret = default
        return _ret

    def get_int(self, key, default=None):
        _ret = DbRedis.get(self, key)
        if _ret is None:
            _ret = default
        else:
            _ret = int(_ret)
        return _ret

    def get_json(self, key, default=None):
        _ret = DbRedis.get(self, key)
        if _ret is None:
            _ret = default
        else:
            _ret = json.loads(_ret)
        return _ret

    def list_lpop(self, key, default=None):
        _ret = DbRedis.list_lpop(self, key)
        if _ret is None:
            _ret = default
        return _ret

    def list_lpop_int(self, key, default=None):
        _ret = DbRedis.list_lpop(self, key)
        if _ret is None:
            _ret = default
        else:
            _ret = int(_ret)
        return _ret

    def list_lpop_json(self, key, default=None):
        _ret = DbRedis.list_lpop(self, key)
        if _ret is None:
            _ret = default
        else:
            _ret = json.loads(_ret)
        return _ret

    def hash_get(self, key, field, default=None):
        _ret = DbRedis.hash_get(self, key, field)
        if _ret is None:
            _ret = default
        return _ret

    def hash_get_int(self, key, field, default=None):
        _ret = DbRedis.hash_get(self, key, field)
        if _ret is None:
            _ret = default
        else:
            _ret = int(_ret)
        return _ret

    def hash_get_json(self, key, field, default=None):
        _ret = DbRedis.hash_get(self, key, field)
        if _ret is None:
            _ret = default
        else:
            _ret = json.loads(_ret)
        return _ret

    def hash_mget_as_dict(self, key, *args):
        values = DbRedis.hash_mget(self, key, *args)
        kvs = {}
        for k, v in zip(args, values):
            if v is not None:
                kvs[k] = v
        return kvs
