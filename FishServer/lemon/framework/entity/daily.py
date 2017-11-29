#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-03

from framework.interface import ICallable
from framework.interface import IContext
from framework.util.tool import Tool
from framework.util.tool import Time


class Daily(ICallable, IContext):
    def get_daily_data(self, uid, gid, *field):
        key = 'daily:%d:%d' % (gid, uid)
        if not field:
            return self.ctx.RedisCluster.hash_getall(uid, key)
        elif len(field) == 1:
            return self.ctx.RedisCluster.hash_get(uid, key, *field)
        else:
            return self.ctx.RedisCluster.hash_mget(uid, key, *field)

    def set_daily_data(self, uid, gid, *args, **kwargs):
        l = Tool.dict2list(kwargs)
        l.extend(args)
        if len(l) % 2 != 0:
            raise Exception('error param')
        key = 'daily:%d:%d' % (gid, uid)
        tomorrow_ts = Time.tomorrow_start_ts()
        isNew = self.ctx.RedisCluster.hash_setnx(uid, key, 'expire_ts', tomorrow_ts)
        if isNew:
            self.ctx.RedisCluster.hash_mset(uid, key, *l)
            self.ctx.RedisCluster.expire_at(uid, key, tomorrow_ts)
        else:
            self.ctx.RedisCluster.hash_mset(uid, key, *l)

    def incr_daily_data(self, uid, gid, field, delta=1):
        key = 'daily:%d:%d' % (gid, uid)
        tomorrow_ts = Time.tomorrow_start_ts()
        isNew = self.ctx.RedisCluster.hash_setnx(uid, key, 'expire_ts', tomorrow_ts)
        if isNew:
            self.ctx.RedisCluster.hash_incrby(uid, key, field, delta)
            self.ctx.RedisCluster.expire_at(uid, key, tomorrow_ts)
            return delta
        else:
            return self.ctx.RedisCluster.hash_incrby(uid, key, field, delta)

    def mincr_daily_data(self, uid, gid, *args, **kwargs):
        key = 'daily:%d:%d' % (gid, uid)
        tomorrow_ts = Time.tomorrow_start_ts()
        isNew = self.ctx.RedisCluster.hash_setnx(uid, key, 'expire_ts', tomorrow_ts)
        if isNew:
            result = self.ctx.RedisCluster.hash_mincrby(uid, key, *args, **kwargs)
            self.ctx.RedisCluster.expire_at(uid, key, tomorrow_ts)
            return result
        else:
            return self.ctx.RedisCluster.hash_mincrby(uid, key, *args, **kwargs)

    def del_daily_data(self, uid, gid, *fields):
        key = 'daily:%d:%d' % (gid, uid)
        return self.ctx.RedisCluster.hash_del(uid, key, *fields)

    def issue_benefit(self, uid, gid, limit=None):
        benefit_config = self.ctx.Configure.get_game_item_json(gid, 'benefit.config')
        if not benefit_config:
            return False
        chip = self.ctx.UserAttr.get_chip(uid, gid, 0)
        if limit is None:
            limit = benefit_config.get('limit', None)
        if limit is not None and chip >= limit:
            return False
        rewards = benefit_config['reward']
        keys = [uid, gid, Time.tomorrow_start_ts(), len(rewards)]
        keys.extend([item['chip'] for item in rewards])
        result = self.ctx.RedisCluster.execute_lua_alias(uid, 'issue_benefit', *keys)
        if result[0] <= 0:
            return False
        self.ctx.Log.report('chip.update: [%s, %s, %s, %s, issue.benefit, {}]' % (uid, gid, result[1], result[2]))
        return {
            'which': result[0],         # 领取第几次
            'total': len(rewards),
            'reward': result[1],
            'chip': result[2],
        }


Daily = Daily()
