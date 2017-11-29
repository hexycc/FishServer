#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-18

import random
import time
import md5
from sdk.const import Const
from sdk.lib.yuntongxun import CCPRestSDK
from sdk.modules.entity import Entity
from sdk.modules.account import Account
from framework.entity.msgpack import MsgPack
from framework.context import Context


class Mobile(object):
    verify_code_timeout = 30 * 60

    # def __request_verify_code(self, gid, mobile):
    #     config = Context.Configure.get_game_item_json(gid, 'sms.config')
    #     rest = CCPRestSDK.REST(config['serverIP'], config['serverPort'], config['softVersion'])
    #     rest.setAccount(config['accountSid'], config['accountToken'])
    #     rest.setAppId(config['appId'])
    #
    #     verifyCode = random.randint(100000, 999999)
    #     result = rest.sendTemplateSMS(mobile, [str(verifyCode), '30'], config['tempId'])
    #     if result['statusCode'] == '000000':
    #         key = 'sms:%d:%s' % (gid, mobile)
    #         Context.RedisCache.hash_set(key, 'verifyCode', verifyCode)
    #         Context.RedisCache.expire(key, self.verify_code_timeout)
    #         return True
    #     return False
    def __request_verify_code(self, gid, mobile):
        verifyCode = random.randint(100000, 999999)
        timestamp = (int(time.time()))
        message = '亲爱的玩家,' + str(verifyCode) + '是您本次手机注册的验证码。'
        token = md5.new(str(mobile) + message + str(timestamp)).hexdigest().lower()
        post_url = 'http://api.dizhubangapp.com/service/sendSPMessage.html '
        data = "mobile=" + str(mobile) + "&" + "message=" + message + "&" + "timestamp=" + str(
            timestamp) + "&" + "token=" + token + "&stype=buyu"
        result = Context.WebPage.wait_for_json(post_url, postdata=data)
        if result['ErrorCode'] == 0:
            key = 'sms:%d:%s' % (gid, mobile)
            Context.RedisCache.hash_set(key, 'verifyCode', verifyCode)
            Context.RedisCache.expire(key, self.verify_code_timeout)
            return True
        return False

    def checkVerifyCode(self, gameId, mobile, toVerifyCode):
        key = 'sms:%d:%s' % (gameId, mobile)
        verifyCode = Context.RedisCache.hash_get(key, 'verifyCode')
        if verifyCode:
            Context.RedisCache.delete(key)
            if str(toVerifyCode) == verifyCode:
                return True
        return False

    def getVerifyCode(self, mi, request):
        gid = mi.get_param('gameId')
        mobile = mi.get_param('mobile')
        isCheck = int(mi.get_param('isCheck', 0))
        if not Entity.checkMobile(mobile):
            return MsgPack.Error(0, 1, 'mobile invalid')

        if isCheck == 1:
            idType = Const.IDTYPE_MOBILE
            userId = Account.getUserIDByUserName(mobile, idType)
            if userId:
                return MsgPack.Error(0, 2, 'mobile exists')

        if not self.__request_verify_code(gid, mobile):
            return MsgPack.Error(0, 3, 'send failed')

        return MsgPack(0)

Mobile = Mobile()
