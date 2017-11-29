#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-18

from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm
import md5
class JiYu(object):
    app_key = ''

    def parse(self, dt):
        Context.Log.info("data:::",dt)
        param = {
            "amount": int(dt.get('amount', 0)),
            "app_id": str(dt.get('app_id', '')),
            "app_info": str(dt.get('app_info', '')),
            "client_id": dt.get('client_id', ''),
            "order_id": dt.get('order_id', ''),
            "out_order_id": dt.get('out_order_id', ''),
            "pay_status": dt.get('pay_status', ''),
            "timestamp": dt.get('timestamp', 0),
            "signType": dt.get('signType', ''),
            "sign": dt.get('sign', ''),
        }
        return param

    def check_app_info(self, self_info, param):
        # todo: sign check
        third_sign = param['sign']
        third_appKey = "mgPC0SmWqYVRUY1a"
        param.pop('sign')
        param.pop('signType')
        sign_str = ''
        for key in param:
            sign_str = sign_str + key + '=' + str(param[key]) + '&'
        final_sign_str = sign_str[:-1] + '&' + md5.new(third_appKey).hexdigest().lower()
        check_sign = md5.new(final_sign_str).hexdigest().lower()
        if third_sign == check_sign:
            return Order.state_verify_success
        else:
            return Order.state_verify_failed_sign
    def pay_callback(self, request):
        data = request.get_args()
        param = self.parse(data)
        if param['pay_status'] != 'success':
            return 'failed'

        orderId = param['out_order_id']
        thirdClientId = param['client_id']
        price = param['amount'] / 100
        parseInfo = Order.parse_order(orderId)
        if not parseInfo:
            Context.Log.info('order not exist')
            return 'failed'

        orderInfo = Order.getOrderInfo(orderId)
        Context.Log.debug('orderInfo-----', orderInfo)
        if not orderInfo:
            return 'failed'

        state = int(orderInfo['state'])
        if state >= Order.state_pre_deliver:        # 可能并没有成功, 需要检查对单
            return 'success'

        cost = int(orderInfo['cost'])
        # if price != cost:
        #     Context.Log.info('price not equal', orderId, orderInfo, parseInfo)
        #     # Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        #     return 'failed'

        userId = int(orderInfo['userId'])
        gameId = int(orderInfo['gameId'])
        channel = orderInfo['channel']
        productId = orderInfo['productId']

        all_product = Context.Configure.get_game_item_json(gameId, 'product.config')
        if productId not in all_product:
            Context.Log.info('productId not exist', orderId, productId, all_product)
            # Context.Log.error('productId not exist', orderId, productId, all_product)
            return 'failed'

        jiyu_app_info = Context.Configure.get_game_item_json(gameId, 'jiyu.app.info')
        if not jiyu_app_info:
            Context.Log.warn('jiyu.app.info miss', orderId, orderInfo, parseInfo)
            return 'failed'

        result = self.check_app_info(jiyu_app_info, param)
        Order.updateOrder(orderId, state=result)
        if result != Order.state_verify_success:
            return 'failed'

        payType = 'jiyu'
        Order.updateOrder(orderId, state=Order.state_pre_deliver, payType=payType)
        kvs = {
            'payTime': param['timestamp'],
            'deliverTime': Time.current_time(),
            'thirdOrderId': param['out_order_id']
        }
        if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, payType):
            kvs['state'] = Order.state_deliver_success
        else:
            kvs['state'] = Order.state_deliver_failed

        Order.updateOrder(orderId, **kvs)
        return 'success'


JiYu = JiYu()
