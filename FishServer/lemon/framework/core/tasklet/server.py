#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-02-15

# from twisted.web import resource
from framework.util.log import Logger
from framework.entity.const import Message
from framework.entity.msgpack import MsgPack
from framework.entity.msgline import MsgLine
from framework.entity.response import http_response
from framework.entity.response import http_response_500
from framework.entity.response import http_response_404
from framework.entity.response import http_response_403
from framework.core.tasklet.tasklet import BasicTasklet
from framework.util.exceptions import SystemException
from framework.util.exceptions import NotFoundException
from framework.util.exceptions import ForbiddenException


class BasicServerTasklet(BasicTasklet):
    def __init__(self, cmd, raw, connection):
        self.cmd = cmd
        self.raw = raw
        self.connection = connection

    def handle(self, *args, **kwargs):
        if Logger.is_debug_network():
            peer = kwargs.get('peer', 'INNER')
            mode = kwargs.get('proto', 'TCP')
            Logger.debug('==== RECV %s FROM %s: %08X %s' % (mode, peer, self.cmd, repr(self.raw)))
        if Message.is_inner(self.cmd):
            cmd = Message.to_outer(self.cmd)
            mi = MsgLine.unpack(self.raw)
            self.onInnerMessage(cmd, mi, *args, **kwargs)
        else:
            self.onOuterMessage(self.cmd, self.raw, *args, **kwargs)

    def onInnerMessage(self, cmd, mi, *args, **kwargs):
        Logger.debug('HANDLE INNER MESSAGE', self.raw, args, kwargs)

    def onOuterMessage(self, cmd, raw, *args, **kwargs):
        Logger.debug('HANDLE OUTER MESSAGE', raw, args, kwargs)


class BasicHttpTasklet(BasicTasklet):
    def __init__(self, request):
        self.request = request

    def handle(self, *args, **kwargs):
        Logger.debug('====>', self.request.path)
        try:
            mo = self.onMessage(*args, **kwargs)
            if self.request._disconnected:
                Logger.info('<====', self.request.path, 'connection lost')
                return
            if isinstance(mo, MsgPack):
                body, content_type = http_response(self.request, mo.pack(), content_type='application/json')
            else:
                body, content_type = http_response(self.request, mo)
        except SystemException, e:
            body, content_type = http_response_500(self.request)
        except NotFoundException, e:
            # body = resource.NoResource('Not Found').render(self.request)
            body, content_type = http_response_404(self.request)
        except ForbiddenException, e:
            # body = resource.ForbiddenResource('Forbidden Access').render(self.request)
            body, content_type = http_response_403(self.request)
        except Exception, e:
            Logger.exception(kwargs)
            body, content_type = http_response_500(self.request)
        Logger.debug('<====', self.request.path, content_type, repr(body))

    def onMessage(self, *args, **kwargs):
        raise NotImplementedError
