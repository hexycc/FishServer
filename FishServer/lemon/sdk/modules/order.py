#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-16

from sdk.const import Const
from sdk.modules.entity import Entity
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm
from framework.entity.msgpack import MsgPack


class Order(object):
    invalid_product = 1
    invalid_channel = 2
    invalid_order = 3
    unknown_error = 4
    time_error = 5
    already_buy = 6
    appstore_limit = 7

    state_timeout = 0
    state_create = 1
    state_verify_success = 2
    state_verify_failed_id = 3
    state_verify_failed_sign = 4
    state_pre_deliver = 5
    state_deliver_success = 6
    state_deliver_failed = 7

    current_version = 1

    @classmethod
    def get_new_order_id(cls, appId, dt):
        """
        orderId采用62进制: <1位版本号><2位应用id><6位时间戳><3位序列号>
        """
        attr = 'max.order.id.%s' % cls.current_version
        seq_number = Context.RedisMix.hash_incrby('global.info.hash', attr, 1)
        api_ver = Context.Strutil.to_str62(cls.current_version, 1)
        app_id = Context.Strutil.to_str62(appId, 2)
        seq_number = Context.Strutil.to_str62(seq_number, 3)
        ts = Context.Strutil.to_str62(int(dt.strftime('%s')), 6)
        return api_ver + app_id + ts + seq_number

    @classmethod
    def parse_order(cls, orderId):
        if isinstance(orderId, (str, unicode)) and len(orderId) == 12:
            api_ver = Context.Strutil.to_int10(orderId[0:1])
            app_id = Context.Strutil.to_int10(orderId[1:3])
            ts = Context.Strutil.to_int10(orderId[3:9])
            seq_number = Context.Strutil.to_int10(orderId[9:12])
            return {'version': api_ver, 'appId': app_id, 'ts': ts, 'seq': seq_number}

    @classmethod
    def __create_order(cls, uid, gid, channel, productId, **kwargs):
        all_product = Context.Configure.get_game_item_json(gid, 'product.config')
        if productId not in all_product:
            return cls.invalid_product, 'invalid productId'

        product = all_product[productId]
        dt = Time.datetime()
        order_id = cls.get_new_order_id(gid, dt)
        kvs = {'userId': uid, 'gameId': gid, 'channel': channel, 'productId': productId, 'cost': product['price'],
               'state': cls.state_create, 'createTime': Time.datetime_to_str(dt, '%Y-%m-%d %X.%f')}
        kvs.update(kwargs)
        Context.Log.report('order.create: [%d, %d, %s, %s]' % (uid, gid, order_id, kvs))
        Context.RedisPay.hash_mset('order:' + order_id, **kvs)
        Context.RedisStat.list_rpush('order:%d:%d:user' % (gid, uid), order_id)
        Context.RedisStat.list_rpush('order:%d:%s:daily' % (gid, dt.strftime('%Y-%m-%d')), order_id)

        info = {
            'orderId': order_id,
            'productId': productId,
            'title': product['name'],
            'desc': '',
            'cost': product['price'],
            'price': product['price'],
        }

        return 0, info

    @classmethod
    def getOrderInfo(cls, orderId, *args):
        if not args:
            return Context.RedisPay.hash_getall('order:' + orderId)
        if len(args) == 1:
            return Context.RedisPay.hash_get('order:' + orderId, args[0])
        else:
            return Context.RedisPay.hash_mget('order:' + orderId, *args)

    def deliver_product(self, userId, gameId, orderId, orderInfo, productId, payType):
        deliver_url = Context.Global.http_game() + '/v1/game/product/deliver'
        param = {
            'userId': userId,
            'gameId': gameId,
            'orderId': orderId,
            'productId': productId,
            'cost': int(orderInfo['cost']),
            'payType': payType,
            'channel': orderInfo['channel']
        }
        appKey = Context.Configure.get_game_item(gameId, 'appKey', '')
        data = '%s-%s-%s' % (orderId, appKey, productId)
        sign = Algorithm.md5_encode(data)
        param['sign'] = sign
        Context.Log.report('product.deliver: [%d, %d, %s, %s]' % (userId, gameId, orderId, param))
        mo = MsgPack(0, param)
        result = Context.WebPage.wait_for_json(deliver_url, postdata=mo.pack())
        return 'error' not in result

    @classmethod
    def updateOrder(cls, orderId, **kwargs):
        return Context.RedisPay.hash_mset('order:' + orderId, **kwargs)

    def createOrder(self, mi, request):
        gameId = mi.get_param('gameId')
        channel = mi.get_param('channel', 'jiyu')
        platform = mi.get_param('platform', 'android')
        productId = mi.get_param('productId')

        if not Entity.logined(request):
            return MsgPack.Error(0, Const.E_NOT_LOGIN, Const.ES_NOT_LOGIN)

        userId = request.getSession().userId
        code, desc = self.__create_order(userId, gameId, channel, productId, platform=platform)
        if code != 0:
            return MsgPack.Error(0, code, desc)
        return MsgPack(0, desc)

    def deliverOrder(self, mi, request):
        gid = mi.get_param('gameId')
        order_list = mi.get_param('orders')
        if not Entity.logined(request):
            return MsgPack.Error(0, Const.E_NOT_LOGIN, Const.ES_NOT_LOGIN)

        uid = request.getSession().userId
        orders = []
        for orderId in order_list:
            orderInfo = self.getOrderInfo(orderId)
            if not orderInfo:
                continue

            userId = int(orderInfo['userId'])
            gameId = int(orderInfo['gameId'])
            state = int(orderInfo['state'])
            if userId != uid:
                Context.Log.warn('userId not match', userId, uid, orderId)
                continue

            if gameId != gid:
                Context.Log.warn('gameId not match', gameId, gid, orderId)
                continue

            if state == self.state_create:
                create_ts = Time.str_to_timestamp(orderInfo['createTime'], '%Y-%m-%d %X.%f')
                now_ts = Time.current_ts()
                if now_ts - create_ts > 3600:
                    state = self.state_timeout
            orders.append({'id': orderId, 'state': state})
        return MsgPack(0, {'orders': orders})


Order = Order()
