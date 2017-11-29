#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-04-11

from framework.context import Context
from framework.entity.msgpack import MsgPack
from framework.util.tool import Algorithm
from framework.util.exceptions import NotFoundException
from framework.util.exceptions import ForbiddenException


class HttpGame(object):
    def __init__(self):
        self.json_path = {
            '/v1/game/product/deliver': self.product_deliver,
        }

    def check_token(self, uid, gid, mi):
        session = mi.get_param('session')
        redis_session = Context.RedisCache.hash_get('token:%d' % uid, 'session')
        if redis_session != session:
            Context.Log.info('verify session key failed', session, redis_session)
            return False
        return True

    def onMessage(self, request):
        if request.method.lower() == 'post':
            data = request.raw_data()
            mi = MsgPack.unpack(0, data)
            Context.Log.debug('------', mi)
            gid = mi.get_param('gameId')
            if request.path in self.json_path:
                with Context.GData.server_locker:
                    return self.json_path[request.path](gid, mi, request)
            else:
                from lemon import classMap
                if gid in classMap:
                    http = classMap[gid].get('http')
                    if http:
                        if request.path in http.json_path:
                            uid = mi.get_param('userId')
                            if not self.check_token(uid, gid, mi):
                                raise ForbiddenException('no permission access')
                            with Context.GData.user_locker[uid]:
                                return http.json_path[request.path](uid, gid, mi, request)

        raise NotFoundException('Not Found')

    def product_deliver(self, gid, mi, request):
        userId = mi.get_param('userId')
        orderId = mi.get_param('orderId')
        productId = mi.get_param('productId')
        appKey = Context.Configure.get_game_item(gid, 'appKey', '')
        data = '%s-%s-%s' % (orderId, appKey, productId)
        sign = Algorithm.md5_encode(data)
        if sign != mi.get_param('sign'):
            return MsgPack.Error(0, 1, 'error sign')

        from lemon import classMap
        entity = classMap.get(gid, {}).get('entity')
        if not entity:
            Context.Log.error('game %d have no processor for order' % gid)
            return MsgPack.Error(0, 2, 'no processor')

        return entity.on_product_deliver(userId, gid, mi)


HttpGame = HttpGame()
