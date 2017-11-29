#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-02-15

import stackless
from channel import Channel
from framework.util.log import Logger


class BasicTasklet(object):
    def run(self, *args, **kwargs):
        self._return_channel = Channel()
        current = stackless.getcurrent()
        current._class_instance = self
        self._tasklet_instance = current
        try:
            self.handle(*args, **kwargs)
        except:
            Logger.exception()

    def handle(self, *args, **kwargs):
        raise NotImplementedError

    def wait_for_deferred(self, d, tip=None):
        try:
            d.addCallbacks(self.__callback, self.__errorback)
            return self._return_channel.receive()
        except Exception, e:
            Logger.exception(tip)
            raise e

    def __callback(self, msg):
        try:
            self._return_channel.send_nowait(msg)
        except Exception, e:
            Logger.exception(msg)
            self._return_channel.send_exception_nowait(Exception, e)

        if stackless.getcurrent() != self._tasklet_instance:
            stackless.schedule()

    def __errorback(self, fault):
        try:
            self._return_channel.send_exception_nowait(fault.type, fault.value)
        except Exception, e:
            Logger.exception(fault)
            self._return_channel.send_exception_nowait(Exception, e)

        if stackless.getcurrent() != self._tasklet_instance:
            stackless.schedule()
