#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-02-01

from framework.context import Context


class Rank(object):
    """
    每个排行榜使用两个数据结构
    1. rank:{gid}:{rank_name} ==> ordered_set结构, 存储uid和score, 可以获取top N
    2. rank:{gid}:{rank_name}:cache ==> hash结构, 缓存用户对应的其他属性
    """

    @classmethod
    def add(cls, uid, gid, rank_name, score, cache_string, capacity=100):
        key = 'rank:%d:%s' % (gid, rank_name)
        cls.check_rank_expire(gid, key)
        min_info = Context.RedisMix.zset_revrange(key, capacity, capacity, True)
        if min_info and int(min_info[1]) >= score:
            return
        Context.RedisMix.zset_add(key, score, uid)
        Context.RedisMix.hash_set(key + ':cache', uid, cache_string)

    @classmethod
    def incrby(cls, uid, gid, rank_name, score, cache=None, field='score'):
        key = 'rank:%d:%s' % (gid, rank_name)
        score = Context.RedisMix.zset_incrby(key, uid, score)
        if cache:
            cache[field] = score
            Context.RedisMix.hash_set(key + ':cache', uid, Context.json_dumps(cache))
        return int(score)

    @classmethod
    def check_rank_expire(cls, gid, full_rank_name):
        pass

    @classmethod
    def issue_rank_reward(cls, gid, rank_name):
        pass

    @classmethod
    def get_rank_list(cls, gid, rank_name, start=0, end=20):
        key = 'rank:%d:%s' % (gid, rank_name)
        id_scores = Context.RedisMix.zset_revrange(key, start, max(0, end), True)
        ids = id_scores[::2]
        scores = id_scores[1::2]
        ret = []
        if ids:
            infos = Context.RedisMix.hash_mget(key + ':cache', *ids)
            for _id, _score, _info in zip(ids, scores, infos):
                if _info:
                    ret.append([_id, _score, _info])

        return ret

    @classmethod
    def get_rank(cls, uid, gid, rank_name):
        key = 'rank:%d:%s' % (gid, rank_name)
        return Context.RedisMix.zset_revrank(key, uid)

    @classmethod
    def get_score(cls, uid, gid, rank_name):
        key = 'rank:%d:%s' % (gid, rank_name)
        return Context.RedisMix.zset_score(key, uid)

    @classmethod
    def get_cache_info(cls, gid, rank_name, *args):
        key = 'rank:%d:%s:cache' % (gid, rank_name)
        if len(args) == 1:
            return Context.RedisMix.hash_get(key, *args)
        else:
            return Context.RedisMix.hash_mget(key, *args)

    @classmethod
    def set_cache_info(cls, gid, rank_name, *args, **kwargs):
        key = 'rank:%d:%s:cache' % (gid, rank_name)
        return Context.RedisMix.hash_mset(key, *args, **kwargs)
