#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-03-09

import stackless


class Channel(stackless.channel):
    def send_nowait(self, v):
        if self.balance == 0:
            self.value = v
        else:
            self.send(v)

    def send_exception_nowait(self, exp_type, exp_value):
        if self.balance == 0:
            self.exc = (exp_type, exp_value)
        else:
            if isinstance(exp_value, exp_type):
                self.send(stackless.bomb(exp_type, exp_value))
            else:
                self.send_exception(exp_type, exp_value)

    def receive(self):
        if hasattr(self, 'value'):
            v = self.value
            del self.value
            return v
        if hasattr(self, 'exc'):
            exp_type, exp_value = self.exc
            del self.exc
            raise Exception(exp_type, exp_value)
        return stackless.channel.receive(self)
