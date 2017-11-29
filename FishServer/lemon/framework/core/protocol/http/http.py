#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-10-09

import os
import time
from twisted.web import http
from twisted.web import server
from twisted.web import static
from twisted.web import resource
from twisted.python import logfile
from framework.util.log import Logger
from framework.util.tool import Time
from framework.entity.manager import TaskManager
from framework.entity.response import http_response_500


class BasicResource(static.File):
    pass


class BasicSession(server.Session):
    pass


class BasicDailyLogFile(logfile.DailyLogFile):
    def suffix(self, tupledate):
        try:
            t = map(str, tupledate)
        except:
            t = map(str, self.toDate(tupledate))
        return '%04d-%02d-%02d' % (int(t[0]), int(t[1]), int(t[2]))


class BasicRequest(server.Request):
    sessionCookieName = None

    def __init__(self, *args, **kw):
        server.Request.__init__(self, *args, **kw)
        self.started = time.time()

    def render(self, resrc):
        if isinstance(resrc, (resource.NoResource, static.DirectoryLister)):
            self.channel.receiveDone(self)
        else:
            server.Request.render(self, resrc)

    def getClientIP(self):
        return self.getHeader('X-Real-IP') or server.Request.getClientIP(self)

    def getSession(self, sessionInterface=None):
        # Session management
        if not self.session:
            cookiename = self.sessionCookieName or b"_".join([b'TWISTED_SESSION'] + self.sitepath)
            sessionCookie = self.getCookie(cookiename)
            if sessionCookie:
                try:
                    self.session = self.site.getSession(sessionCookie)
                except KeyError:
                    pass
            # if it still hasn't been set, fix it up.
            if not self.session:
                self.session = self.site.makeSession()
                self.addCookie(cookiename, self.session.uid, path=b'/')
        self.session.touch()
        if sessionInterface:
            return self.session.getComponent(sessionInterface)
        return self.session

    def get_args(self):
        args = {}
        for k, v in self.args.iteritems():
            if len(v) > 1:
                args[k] = v
            else:
                args[k] = v[0]
        return args

    def raw_data(self):
        return self.content.read()

    def get_origin(self):
        return self.getHeader('origin') or '*'


class BasicHttpProtocol(http.HTTPChannel):
    def makeTasklet(self, request):
        raise NotImplementedError

    def receiveDone(self, request):
        try:
            tasklet = self.makeTasklet(request)
            TaskManager.add_task(tasklet.run)
            TaskManager.schedule()
        except Exception, e:
            Logger.exception()
            body, content_type = http_response_500(self.request)
            Logger.debug('<====', self.request.path, content_type, repr(body))


class BasicHttpFactory(server.Site):
    protocol = BasicHttpProtocol

    def __init__(self, logPath, resource, **kwargs):
        logPath += '.access'
        if 'logFormatter' not in kwargs:
            kwargs['logFormatter'] = self.timedLogFormatter
        server.Site.__init__(self, resource, logPath=logPath, **kwargs)

    def _openLogFile(self, path):
        return BasicDailyLogFile(os.path.basename(path), os.path.dirname(path))

    @classmethod
    def timedLogFormatter(cls, timestamp, request):
        from twisted.web.http import _escape

        referrer = _escape(request.getHeader("referer") or "-")
        agent = _escape(request.getHeader("user-agent") or "-")
        tc = round(time.time() - request.started, 4)
        line = u'%(fmt)s | "%(ip)s" %(tc)ss %(code)d %(length)s "%(method)s %(uri)s %(proto)s" "%(agent)s" "%(ref)s"' % {
            'fmt': Time.current_time('%m-%d %H:%M:%S.%f'),
            'ip': _escape(request.getClientIP() or "-"),
            'tc': tc,
            'method': _escape(request.method),
            'uri': _escape(request.uri),
            'proto': _escape(request.clientproto),
            'code': request.code,
            'length': request.sentLength or "-",
            'agent': agent,
            'ref': referrer,
        }
        return line
