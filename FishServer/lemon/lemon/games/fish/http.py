#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-02-23

from rank import FishRank
from framework.context import Context
from framework.entity.const import Message
from framework.entity.msgpack import MsgPack


class FishHttp(object):
    def __init__(self):
        self.json_path = {
            '/v1/game/rank_list': self.get_rank_list,
            '/v1/game/history': self.get_history,
        }

    def get_rank_list(self, uid, gid, mi, request):
        return FishRank.get_ranks(uid, gid, mi)

    def get_history(self, uid, gid, mi, request):
        mo = MsgPack(0)
        _list = self.__get_history_exchange_list(uid, gid)
        mo.set_param('exchange', _list)
        return mo

    def __get_history_exchange_list(self, uid, gid):
        _list = []
        all_history = Context.RedisCluster.hash_getall(uid, 'history:%d:%d' % (gid, uid))
        if all_history:
            keys = all_history.keys()
            values = Context.RedisMix.hash_mget('game.%d.exchange.record' % gid, *keys)
            for k, v in zip(keys, values):
                v = Context.json_loads(v)
                if v and v['type'] == 'exchange':
                    _r = {
                        'ts': v['ts'],
                        'desc': v['desc'],
                        'cost': v['cost'],
                        'state': int(all_history[k])
                    }
                    if 'phone' in v:
                        _r['phone'] = v['phone']
                    _list.append(_r)
        return _list

FishHttp = FishHttp()
