#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-10-15

import json
from http import BasicSession
from http import BasicRequest
from http import BasicResource
from http import BasicHttpFactory
from http import BasicHttpProtocol
from framework.entity.globals import Global


class ServerHttpFactory(BasicHttpFactory):
    protocol = BasicHttpProtocol
    sessionFactory = BasicSession
    requestFactory = BasicRequest

    def __init__(self, logPath=None, webroot=None):
        if not logPath:
            logPath = Global.log_path()
        if not webroot:
            webroot = Global.web_root()
        BasicHttpFactory.__init__(self, logPath, BasicResource(webroot))


class SdkRequest(BasicRequest):
    sessionCookieName = 'ddz_session'


class SdkSession(BasicSession):
    sessionTimeout = 86400

    def __init__(self, site, uid, reactor=None):
        self.userId = 0
        BasicSession.__init__(self, site, uid, reactor)

    def recover(self, data):
        data = json.loads(data)
        self.userId = data['userId']

    def touch(self):
        BasicSession.touch(self)
        if self.userId > 0:
            self.__cache_session()

    def isLogined(self):
        return self.userId > 0

    def setLogined(self, userId):
        if self.userId != userId:
            self.userId = userId
            if self.userId > 0:
                self.__cache_session()

    def __cache_session(self):
        from framework.context import Context
        data = json.dumps({'userId': self.userId}, separators=(',', ':'))
        Context.RedisCache.setex('token:%s' % self.uid, data, int(self.sessionTimeout))


class SdkHttpFactory(ServerHttpFactory):
    sessionFactory = SdkSession
    requestFactory = SdkRequest

    def getSession(self, uid):
        if uid not in self.sessions:
            from framework.context import Context
            data = Context.RedisCache.get('token:%s' % uid)
            if data:
                session = self.sessions[uid] = self.sessionFactory(self, uid)
                session.recover(data)
                session.startCheckingExpiration()

        return self.sessions[uid]

    def makeSession(self):
        uid = self._mkuid()
        session = self.sessions[uid] = self.sessionFactory(self, uid)
        session.startCheckingExpiration()
        return session


class GameHttpFactory(ServerHttpFactory):
    pass


class ShellHttpFactory(ServerHttpFactory):
    pass
