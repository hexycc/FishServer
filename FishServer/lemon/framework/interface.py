#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-03-01

from framework.util.exceptions import NotInitException


class IContext(object):
    def __getattr__(self, item):
        if item == 'ctx':
            raise NotInitException('not init, please call init_ctx first')

    @classmethod
    def init_ctx(cls):
        from framework.context import Context
        cls.ctx = Context
        setattr(cls, 'init_ctx', None)


class ICallable(object):
    def __call__(self, *args, **kwargs):
        return self
