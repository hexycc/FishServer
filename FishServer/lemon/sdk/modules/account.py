#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-18

import random
from sdk.const import Const
from framework.context import Context
from framework.util.tool import Time


class Account(object):
    CACHE_DATA_TIMEOUT = 24 * 60 * 60  # 24小时

    def setUserToken(self, uid, gid, session):
        strKey = 'token:%d' % uid
        Context.RedisCache.hash_set(strKey, 'session', session)
        Context.RedisCache.expire(strKey, self.CACHE_DATA_TIMEOUT)

    def getUserIDByUserName(self, userName, idType):
        key = 'username:%d:%s' % (idType, userName)
        return Context.RedisMix.hash_get_int(key, 'userId')

    def getUserInfo(self, userId):
        attrs = ['userName', 'idType', 'token', 'nick', 'sex', 'avatar', 'deviceId', 'createIp', 'createTime']
        kvs = dict.fromkeys(attrs, None)
        Context.Log.info("kvs-----:", kvs)
        kvs.update(Context.Data.get_attrs_dict(userId, attrs))
        return kvs

    def createUserInfo(self, userId, dictInfo):
        sex = random.choice([Const.SEX_MAN, Const.SEX_WOMAN])
        if sex == Const.SEX_WOMAN:
            avatar = random.choice(Const.DEFAULT_AVATAR_WOMAN)
        else:
            avatar = random.choice(Const.DEFAULT_AVATAR_MAN)
        value = {'userName': dictInfo['userName'], 'idType': dictInfo['idType'], 'token': dictInfo['token'],
                 'nick': dictInfo['nick'], 'sex': sex, 'avatar': avatar, 'status': 0, 'deviceId': dictInfo['deviceId'],
                 'createIp': dictInfo['createIp'], 'createTime': Time.datetime_now(), 'accessToken': '',
                 'channel': dictInfo['channel'], 'platform': dictInfo['platform']}
        if 'openid' in dictInfo:
            value['openid'] = dictInfo['openid']
        return Context.Data.set_attrs_dict(userId, value)

    def createUserName(self, idType, userName, userId):
        key = 'username:%d:%s' % (idType, userName)
        return Context.RedisMix.hash_setnx(key, 'userId', userId)

    def deleteUserName(self, userName, idType):
        key = 'username:%d:%s' % (idType, userName)
        return Context.RedisMix.delete(key)

    def createUser(self, info):
        uid = Context.GData.get_new_user_id()
        Context.Log.info("uid ::: is ::", uid)
        if not self.createUserName(info['idType'], info['userName'], uid):
            return None
        if not self.createUserInfo(uid, info):
            self.deleteUserName(info['userName'], info['idType'])
            return None
        Context.Log.report('user.init:', [uid, info])
        return uid

    def updateUserInfo(self, userId, **kvs):
        return Context.Data.set_attrs_dict(userId, kvs)


Account = Account()
