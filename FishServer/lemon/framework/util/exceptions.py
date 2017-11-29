#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2014-10-14


class BasicException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

    def __repr__(self):
        return repr(self.value)


class TimeoutException(BasicException):
    pass


class NotFoundException(BasicException):
    pass


class ForbiddenException(BasicException):
    pass


class SystemException(BasicException):
    pass


class NotInitException(BasicException):
    pass


class NotImplementedException(BaseException):
    pass
