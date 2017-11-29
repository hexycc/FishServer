#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-18

from random import Random

from framework.context import Context
from framework.entity.msgpack import MsgPack
from framework.util.tool import Algorithm
from framework.util.tool import Time
from sdk.const import Const
from sdk.modules.account import Account
from sdk.modules.entity import Entity
from sdk.modules.mobile import Mobile


class User(object):
    error_invalid_username = 1
    error_invalid_passwd = 2
    error_invalid_access_token = 3
    error_user_not_exist = 4
    error_pwd_not_right = 5
    error_version_too_low = 6
    desc_invalid_username = "param invalid"
    desc_invalid_passwd = "param invalid"
    desc_invalid_access_token = "param invalid"
    desc_user_not_exist = "user not exists"
    desc_pwd_not_right = "password not right"
    desc_version_too_low = "version too low"

    @classmethod
    def getParam(cls, mi, *args):
        param = {
            'cmd': mi.get_cmd(),
            'gameId': mi.get_param('gameId'),
            'deviceId': mi.get_param('deviceId', ''),
            'deviceId2': mi.get_param('deviceId2', ''),
            'mac': mi.get_param('mac', ''),
            'imei': mi.get_param('imei', ''),
            'imsi': mi.get_param('imsi', ''),
            'ip': mi.get_param('ip', ''),
            'model': mi.get_param('model', ''),
            'releaseVer': mi.get_param('releaseVer', ''),
            'location': mi.get_param('location', ''),
            'phoneType': mi.get_param('phoneType', ''),
            'resolution': mi.get_param('resolution', ''),
            'versionName': mi.get_param('versionName', ''),
            'umengToken': mi.get_param('umengToken', ''),
            'networkType': mi.get_param('networkType', ''),
            'channel': mi.get_param('channel', 'jiyu'),
            'platform': mi.get_param('platform', 'platform'),
            'clientId': mi.get_param('clientId', 'JYBY001'),
        }
        for arg in args:
            param[arg] = mi.get_param(arg, '')
        return param

    @classmethod
    def getLoginInfo(cls, request, cmd, uid, gid, param, userInfo, freshAccessToken, openid=None, open_token=None):
        session = Algorithm.md5_encode(Time.asctime() + request.getClientIP() + userInfo['userName'])
        Account.setUserToken(uid, gid, session)

        conn_server = Context.json_loads(Context.RedisCache.get('connect.server'))
        internet = conn_server[uid % len(conn_server)]

        dictInfo = {
            "session": session,
            "userId": uid,
            "sex": int(userInfo['sex']),
            "nick": userInfo['nick'],
            "avatar": userInfo['avatar'],
            "host": internet["domain"],
            "port": internet["port"],
        }

        if openid:
            dictInfo['openid'] = openid
        if open_token:
            dictInfo['open_token'] = open_token

        if freshAccessToken:
            data = '{"uid":%d,"ct":%d}' % (uid, Time.current_ts())
            accessToken = Entity.encrypt(data)
            Account.updateUserInfo(uid, accessToken=accessToken)
            dictInfo['accessToken'] = accessToken

        kvs = {
            'session_platform': param['platform'] or 'android',
            'session_channel': param['channel'] or 'jiyu',
            'session_ver': param['releaseVer'] or '1.0.1'
        }
        Context.Data.set_game_attrs_dict(uid, gid, kvs)

        Context.Log.report('user.login:', [uid, gid, kvs])

        # 登录成功设置session值
        session = request.getSession()
        session.setLogined(uid)

        return MsgPack(cmd, dictInfo)

    def loginByMobile(self, mi, request):
        param = self.getParam(mi, 'mobile', 'passwd')
        if not Entity.checkMobile(param['mobile']):
            return MsgPack.Error(0, self.error_invalid_username, self.desc_invalid_username)
        if not Entity.checkPassword(param['passwd']):
            return MsgPack.Error(0, self.error_invalid_passwd, self.desc_invalid_passwd)

        idType = Const.IDTYPE_MOBILE
        userId = Account.getUserIDByUserName(param['mobile'], idType)
        if not userId:
            return MsgPack.Error(0, self.error_user_not_exist, self.desc_user_not_exist)

        userInfo = Account.getUserInfo(userId)
        if not userInfo['userName']:
            return MsgPack.Error(0, self.error_user_not_exist, self.desc_user_not_exist)

        # 进行密码比较
        strMd5Pass = Entity.encodePassword(param['mobile'], param['passwd'])
        if strMd5Pass != userInfo['token']:
            return MsgPack.Error(0, self.error_pwd_not_right, self.desc_pwd_not_right)

        return self.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, True)

    def loginByUserName(self, mi, request):
        param = self.getParam(mi, 'userName', 'passwd')
        if not Entity.checkUserName(param['userName']):
            return MsgPack.Error(0, self.error_invalid_username, self.desc_invalid_username)
        if not Entity.checkPassword(param['passwd']):
            return MsgPack.Error(0, self.error_invalid_passwd, self.desc_invalid_passwd)

        idType = Const.IDTYPE_USERNAME
        userId = Account.getUserIDByUserName(param['userName'], idType)
        if not userId:
            return MsgPack.Error(0, self.error_user_not_exist, self.desc_user_not_exist)

        userInfo = Account.getUserInfo(userId)
        if not userInfo['userName']:
            return MsgPack.Error(0, self.error_user_not_exist, self.desc_user_not_exist)

        # 进行密码比较
        strMd5Pass = Entity.encodePassword(param['userName'], param['passwd'])
        if strMd5Pass != userInfo['token']:
            return MsgPack.Error(0, self.error_pwd_not_right, self.desc_pwd_not_right)

        return self.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, True)

    def loginByAccessToken(self, mi, request):
        param = self.getParam(mi, 'accessToken')

        if len(param['accessToken']) <= 1:
            return MsgPack.Error(0, self.error_invalid_access_token, self.desc_invalid_access_token)

        try:
            decrptData = Entity.decrypt(param['accessToken'])
            decoded = Context.json_loads(decrptData)
        except Exception, e:
            return MsgPack.Error(0, self.error_invalid_access_token, self.desc_invalid_access_token)

        if 'uid' not in decoded:
            return MsgPack.Error(0, self.error_invalid_access_token, self.desc_invalid_access_token)

        userId = decoded['uid']
        token = Context.Data.get_attr(userId, 'accessToken')
        if token != param['accessToken']:
            return MsgPack.Error(0, self.error_invalid_access_token, self.desc_invalid_access_token)

        userInfo = Account.getUserInfo(userId)
        if not userInfo['userName']:
            return MsgPack.Error(0, self.error_user_not_exist, self.desc_user_not_exist)
        if param['clientId']:
            clientId = param['clientId']
            c_key = 'client:%s' % (clientId)
            Context.RedisMix.set_add(c_key, userId)
        return self.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False)

    def loginByGuest(self, mi, request):
        param = self.getParam(mi, 'devName')
        l = []
        if param['deviceId']:
            l.append(param['deviceId'])
        if param['deviceId2']:
            l.append(param['deviceId2'])
        if param['mac']:
            l.append(param['mac'])
        if param['imei']:
            l.append(param['imei'])
        if param['imsi']:
            l.append(param['imsi'])

        gid = param['gameId']
        idType = Const.IDTYPE_GUEST
        for dev in l:
            uid = Account.getUserIDByUserName(dev, idType)
            if uid:
                break
        else:
            if l:
                deviceId = l[0]
            else:
                deviceId = 'DEVID' + str(Time.current_ms())

            platform = param['platform']
            channel = param['channel']
            clientId = param['clientId']
            dictInfo = {'idType': idType, 'deviceId': deviceId, 'userName': deviceId, 'nick': param['devName'],
                        'createIp': request.getClientIP(), 'token': '', 'platform': platform, 'channel': channel,
                        'clientId': clientId}
            Context.Log.info("dictInfo::", dictInfo)
            uid = Account.createUser(dictInfo)
            nick_name = "游客" + str(uid)
            Account.updateUserInfo(uid, nick = nick_name)
            if uid is None:
                return MsgPack.Error(0, Const.E_BAD_REDIS, Const.ES_BAD_REDIS)

            key = 'game.%d.info.hash' % gid
            pipe_args = []
            if l:
                field = '%s.new.device.count' % channel
                pipe_args.append(field)
                pipe_args.append(1)

            field = '%s.new.user.count' % channel
            pipe_args.append(field)
            pipe_args.append(1)
            Context.RedisMix.hash_mincrby(key, *pipe_args)
            Context.Stat.mincr_daily_data(gid, *pipe_args)

        c_key = 'client:%s' % (clientId)
        Context.RedisMix.set_add(c_key)
        userInfo = Account.getUserInfo(uid)
        return self.getLoginInfo(request, 0, uid, gid, param, userInfo, True)

    def random_str(self, randomNum):
        str = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(randomNum):
            str += chars[random.randint(0, length)]
        return str

    def updateUserInfo(self, mi, request):
        nick = mi.get_param('nick')
        avatar = mi.get_param('avatar')
        if not Entity.logined(request):
            return MsgPack.Error(0, Const.E_NOT_LOGIN, Const.ES_NOT_LOGIN)

        uid = request.getSession().userId
        kvs = {}
        if nick:
            if not Entity.checkNick(nick):
                return MsgPack.Error(0, 1, 'param nick invalid')
            if Context.KeywordFilter.isContains(nick):
                return MsgPack.Error(0, 2, 'key word filter')
            kvs['nick'] = nick

        if avatar:
            if avatar in Const.AVATAR_MAN:
                kvs['avatar'] = avatar
                kvs['sex'] = Const.SEX_MAN
            elif avatar in Const.AVATAR_WOMAN:
                kvs['avatar'] = avatar
                kvs['sex'] = Const.SEX_WOMAN
            else:
                return MsgPack.Error(0, 3, 'param avatar invalid')

        if kvs:
            Account.updateUserInfo(uid, **kvs)

        return MsgPack(0, kvs)

    def resetPasswd(self, mi, request):
        gid = mi.get_param('gameId')
        mobile = mi.get_param('mobile', '')
        verifyCode = mi.get_param('verifyCode', '')
        passwd = mi.get_param('passwd', '')
        if not Mobile.checkVerifyCode(gid, mobile, verifyCode):
            return MsgPack.Error(0, 1, 'verifycode not right')

        idType = Const.IDTYPE_MOBILE
        userId = Account.getUserIDByUserName(mobile, idType)
        if not userId:
            return MsgPack.Error(0, 2, 'user not exist')

        Account.updateUserInfo(userId, token=Entity.encodePassword(mobile, passwd))
        return MsgPack(0, {'newPwd': passwd})

    def upgradeByMobile(self, mi, request):
        gid = mi.get_param('gameId')
        nick = mi.get_param('nick', '')
        mobile = mi.get_param('mobile', '')
        passwd = mi.get_param('passwd', '')
        verifyCode = mi.get_param('verifyCode', '')

        if not Entity.logined(request):
            return MsgPack.Error(0, Const.E_NOT_LOGIN, Const.ES_NOT_LOGIN)

        if not Entity.checkMobile(mobile):
            return MsgPack.Error(0, 1, 'mobile invalid')

        if not Entity.checkPassword(passwd):
            return MsgPack.Error(0, 2, 'password invalid')

        if not Entity.checkNick(nick):
            return MsgPack.Error(0, 6, 'nick invalid')

        userId = request.getSession().userId
        # 先判断是不是游客
        userInfo = Account.getUserInfo(userId)
        if int(userInfo['idType']) != Const.IDTYPE_GUEST:
            return MsgPack.Error(0, 3, 'not guest')

        # 先查表，判断用户存不存在
        if Account.getUserIDByUserName(mobile, Const.IDTYPE_MOBILE):
            return MsgPack.Error(0, 4, 'mobile exist')

        if not Mobile.checkVerifyCode(gid, mobile, verifyCode):
            return MsgPack.Error(0, 5, 'verifycode not right')

        # nick 唯一
        if not Context.RedisMix.hash_setnx('game.%d.unique.nick' % gid, nick, 0):
            return MsgPack.Error(0, 7, 'nick not unique')

        if not Account.createUserName(Const.IDTYPE_MOBILE, mobile, userId):
            Context.RedisMix.hash_del('game.%d.unique.nick' % gid, nick)
            return MsgPack.Error(0, Const.E_BAD_REDIS, Const.ES_BAD_REDIS)

        if not Account.deleteUserName(userInfo['userName'], Const.IDTYPE_GUEST):
            Context.Log.error(userId, 'DeleteUserName failed,userName:', userInfo['userName'])

        Context.RedisMix.hash_set('game.%d.unique.nick' % gid, nick, userId)
        Account.updateUserInfo(userId, userName=mobile, nick=nick, idType=Const.IDTYPE_MOBILE,
                               token=Entity.encodePassword(mobile, passwd))
        return MsgPack(0)

    def registerByMobile(self, mi, request):
        gid = mi.get_param('gameId')
        mobile = mi.get_param('mobile', '')
        passwd = mi.get_param('passwd', '')
        deviceId = mi.get_param('deviceId', '')
        nick = mi.get_param('nick', '')
        verifyCode = mi.get_param('verifyCode', '')
        platform = mi.get_param('platform', 'android')
        channel = mi.get_param('channel', 'jiyu')
        if not Entity.checkMobile(mobile):
            return MsgPack.Error(0, 1, 'param mobile invalid')
        if not Entity.checkPassword(passwd):
            return MsgPack.Error(0, 2, 'param passwd invalid')
        if not Entity.checkNick(nick):
            return MsgPack.Error(0, 3, 'param nick invalid')

        # 先查表，判断用户存不存在
        idType = Const.IDTYPE_MOBILE
        userId = Account.getUserIDByUserName(mobile, idType)
        if userId:
            return MsgPack.Error(0, 4, 'mobile exist')

        if not Mobile.checkVerifyCode(gid, mobile, verifyCode):
            return MsgPack.Error(0, 5, 'verifycode not right')

        # nick 唯一
        nick_unique_key = 'game.%d.unique.nick' % gid
        if not Context.RedisMix.hash_setnx(nick_unique_key, nick, 0):
            return MsgPack.Error(0, 6, 'nick not unique')

        # 插入用户数据
        strMd5Pass = Entity.encodePassword(mobile, passwd)
        dictInfo = {'idType': idType, 'deviceId': deviceId, 'userName': mobile, 'nick': nick,
                    'createIp': request.getClientIP(), 'token': strMd5Pass, 'guest': 0,
                    'channel': channel, 'platform': platform}
        userId = Account.createUser(dictInfo)
        if not userId:
            Context.RedisMix.hash_del(nick_unique_key, nick)
            return MsgPack.Error(0, Const.E_BAD_REDIS, Const.ES_BAD_REDIS)

        Context.RedisMix.hash_set(nick_unique_key, nick, userId)
        key, field = 'game.%d.info.hash' % gid, '%s.new.user.count' % channel
        Context.RedisMix.hash_incrby(key, field, 1)
        Context.Stat.incr_daily_data(gid, field, 1)

        return MsgPack(0)

    def registerByUserName(self, mi, request):
        gid = mi.get_param('gameId')
        username = mi.get_param('userName', '')
        passwd = mi.get_param('passwd', '')
        deviceId = mi.get_param('deviceId', '')
        platform = mi.get_param('platform', 'android')
        channel = mi.get_param('channel', 'jiyu')
        if not Entity.checkUserName(username):
            return MsgPack.Error(0, 1, 'username invalid')
        if not Entity.checkPassword(passwd):
            return MsgPack.Error(0, 2, 'password invalid')

        nick = username
        if Context.KeywordFilter.isContains(nick):
            return MsgPack.Error(0, 3, 'keyword filter')

        # 先查表，判断用户存不存在
        idType = Const.IDTYPE_USERNAME
        userId = Account.getUserIDByUserName(username, idType)
        if userId:
            return MsgPack.Error(0, 5, 'username exist')

        # nick 唯一
        nick_unique_key = 'game.%d.unique.nick' % gid
        if not Context.RedisMix.hash_setnx(nick_unique_key, nick, 0):
            return MsgPack.Error(0, 6, 'nick not unique')

        # 插入用户数据
        strMd5Pass = Entity.encodePassword(username, passwd)
        dictInfo = {'idType': idType, 'deviceId': deviceId, 'userName': username, 'nick': nick,
                    'createIp': request.getClientIP(), 'token': strMd5Pass, 'guest': 0,
                    'channel': channel, 'platform': platform}
        userId = Account.createUser(dictInfo)
        if not userId:
            Context.RedisMix.hash_del(nick_unique_key, nick)
            return MsgPack.Error(0, Const.E_BAD_REDIS, Const.ES_BAD_REDIS)

        Context.RedisMix.hash_set(nick_unique_key, nick, userId)
        key, field = 'game.%d.info.hash' % gid, '%s.new.user.count' % channel
        Context.RedisMix.hash_incrby(key, field, 1)
        Context.Stat.incr_daily_data(gid, field, 1)

        return MsgPack(0)

    def upgradeByUserName(self, mi, request):
        gid = mi.get_param('gameId')
        username = mi.get_param('userName', '')
        passwd = mi.get_param('passwd', '')

        if not Entity.logined(request):
            return MsgPack.Error(0, Const.E_NOT_LOGIN, Const.ES_NOT_LOGIN)

        if not Entity.checkUserName(username):
            return MsgPack.Error(0, 1, 'username invalid')

        if not Entity.checkPassword(passwd):
            return MsgPack.Error(0, 2, 'password invalid')

        nick = username
        if Context.KeywordFilter.isContains(nick):
            return MsgPack.Error(0, 3, 'keyword filter')

        userId = request.getSession().userId
        # 先判断是不是游客
        userInfo = Account.getUserInfo(userId)
        if int(userInfo['idType']) != Const.IDTYPE_GUEST:
            return MsgPack.Error(0, 4, 'not guest')

        # 先查表，判断用户存不存在
        if Account.getUserIDByUserName(username, Const.IDTYPE_USERNAME):
            return MsgPack.Error(0, 5, 'username exist')

        # nick 唯一
        if not Context.RedisMix.hash_setnx('game.%d.unique.nick' % gid, username, 0):
            return MsgPack.Error(0, 6, 'nick not unique')

        if not Account.createUserName(Const.IDTYPE_USERNAME, username, userId):
            Context.RedisMix.hash_del('game.%d.unique.nick' % gid, username)
            return MsgPack.Error(0, Const.E_BAD_REDIS, Const.ES_BAD_REDIS)

        if not Account.deleteUserName(userInfo['userName'], Const.IDTYPE_GUEST):
            Context.Log.error(userId, 'DeleteUserName failed,userName:', userInfo['userName'])

        Context.RedisMix.hash_set('game.%d.unique.nick' % gid, username, userId)
        Account.updateUserInfo(userId, userName=username, nick=nick, idType=Const.IDTYPE_USERNAME,
                               token=Entity.encodePassword(username, passwd))
        return MsgPack(0)

    def register(self, param, request, openid, idType, channel):
        gid = param['gameId']
        l = []
        if param['deviceId']:
            l.append(param['deviceId'])
        if param['deviceId2']:
            l.append(param['deviceId2'])
        if param['mac']:
            l.append(param['mac'])
        if param['imei']:
            l.append(param['imei'])
        if param['imsi']:
            l.append(param['imsi'])

        if l:
            deviceId = l[0]
        else:
            deviceId = 'DEVID' + str(Time.current_ms())

        platform = param['platform']
        # channel = param['channel']
        nickName = param['devName']
        if param.get('nickName'):
            nickName = param.get('nickName')
        dictInfo = {'idType': idType, 'deviceId': deviceId, 'userName': openid, 'nick': nickName,
                    'createIp': request.getClientIP(), 'token': '', 'platform': platform, 'channel': channel,
                    'openid': openid}
        uid = Account.createUser(dictInfo)
        if uid is None:
            return None

        key = 'game.%d.info.hash' % gid
        pipe_args = []
        if l:
            field = '%s.new.device.count' % channel
            pipe_args.append(field)
            pipe_args.append(1)

        field = '%s.new.user.count' % channel
        pipe_args.append(field)
        pipe_args.append(1)
        Context.RedisMix.hash_mincrby(key, *pipe_args)
        Context.Stat.mincr_daily_data(gid, *pipe_args)
        return uid


User = User()
