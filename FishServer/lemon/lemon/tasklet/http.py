#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-20

from framework.core.tasklet import server


class SdkTasklet(server.BasicHttpTasklet):
    def onMessage(self, *args, **kwargs):
        from sdk.route import HttpSdk
        return HttpSdk.onMessage(self.request)


class ShellTasklet(server.BasicHttpTasklet):
    def onMessage(self, *args, **kwargs):
        from webshell.route import HttpShell
        return HttpShell.onMessage(self.request)


class HttpTasklet(server.BasicHttpTasklet):
    def onMessage(self, *args, **kwargs):
        from lemon.entity.http import HttpGame
        return HttpGame.onMessage(self.request)
