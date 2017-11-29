#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-10-15

from sdk.third.jiyu import JiYu
from sdk.modules.user import User
from sdk.modules.mobile import Mobile
from sdk.modules.order import Order
from framework.context import Context
from framework.entity.msgpack import MsgPack
from framework.util.exceptions import NotFoundException


class HttpSdk(object):
    def __init__(self):
        self.json_path = {
            '/v1/user/getVerifyCode': Mobile.getVerifyCode,  # fix client bug
            '/v1/mobile/getVerifyCode': Mobile.getVerifyCode,
            '/v1/user/registerByMobile': User.registerByMobile,
            '/v1/user/upgradeByMobile': User.upgradeByMobile,
            '/v1/user/registerByUserName': User.registerByUserName,
            '/v1/user/upgradeByUserName': User.upgradeByUserName,
            '/v1/user/loginByMobile': User.loginByMobile,
            '/v1/user/loginByUserName': User.loginByUserName,
            '/v1/user/loginByGuest': User.loginByGuest,
            '/v1/user/loginByAccessToken': User.loginByAccessToken,
            '/v1/user/resetPassword': User.resetPasswd,
            '/v1/user/modifyUserInfo': User.updateUserInfo,
            '/v1/order/create': Order.createOrder,
            '/v1/order/deliver': Order.deliverOrder,
            # 第三方登录
        }

        # 第三方回调
        self.callback_path = {
            '/v1/third/callback/jiyu/pay': JiYu.pay_callback,
        }

    def onMessage(self, request):
        if request.method.lower() == 'post':
            if request.path in self.json_path:
                data = request.raw_data()
                mi = MsgPack.unpack(0, data)
                Context.Log.debug(mi)
                # with Context.GData.server_locker:
                return self.json_path[request.path](mi, request)

        if request.path in self.callback_path:
            with Context.GData.server_locker:
                return self.callback_path[request.path](request)

        raise NotFoundException('Not Found')


HttpSdk = HttpSdk()
