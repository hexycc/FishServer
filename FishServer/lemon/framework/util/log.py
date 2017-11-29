#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2014-09-25

"""
[debug: cyan, info: white, warn: blue, error: yellow, fatal: red, bi: white]
"""

import time
import sys
import traceback
import logging
import logging.handlers

_NOTSET = ''
_DEBUG = ''
_INFO = ''
_WARN = ''
_ERROR = ''
_FATAL = ''
_RECOVERY = ''

logging.addLevelName(logging.NOTSET, ' | N | ' + _NOTSET)
logging.addLevelName(logging.DEBUG, ' | D | ' + _DEBUG)
logging.addLevelName(logging.INFO, ' | I | ' + _INFO)
logging.addLevelName(logging.WARN, ' | W | ' + _WARN)
logging.addLevelName(logging.ERROR, ' | E | ' + _ERROR)
logging.addLevelName(logging.FATAL, ' | B | ' + _FATAL)


class LogFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        s = time.strftime("%m-%d %H:%M:%S", ct)
        s = "%s.%06d" % (s, record.msecs * 1000)
        return s


class Logger(object):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    BI = logging.FATAL

    _show_task_id = True
    _show_prefix = False
    _show_network = True
    _show_redis = True
    _open_std_log = False
    _open_log = False
    _open_bi_log = False
    __logger = logging.getLogger()

    @classmethod
    def open_log(cls, fpath):
        if cls._open_log:
            cls.warn('open log have called')
            return
        formatter = LogFormatter('%(asctime)s%(levelname)s%(message)s')
        handler = logging.handlers.TimedRotatingFileHandler(fpath, when='MIDNIGHT')
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        cls.__logger.addHandler(handler)
        cls.__logger.setLevel(logging.DEBUG)
        cls._open_log = True
        if hasattr(cls, 'std_handler'):
            cls.__logger.removeHandler(getattr(cls, 'std_handler'))

    @classmethod
    def open_std_log(cls):
        if cls._open_std_log:
            cls.warn('open std log have called')
            return

        std_handler = logging.StreamHandler(sys.stdout)
        std_formatter = LogFormatter('%(asctime)s%(levelname)s%(message)s')
        std_handler.setFormatter(std_formatter)
        std_handler.setLevel(logging.DEBUG)
        std_logger = logging.getLogger()
        std_logger.addHandler(std_handler)
        std_logger.setLevel(logging.DEBUG)
        cls._open_std_log = True
        cls.std_handler = std_handler

    @classmethod
    def is_debug_network(cls):
        return cls._show_network

    @classmethod
    def is_debug_redis(cls):
        return cls._show_redis

    @classmethod
    def open_bi_log(cls, fpath):
        if cls._open_bi_log:
            cls.warn('open bi log have called')
            return

        formatter = LogFormatter('%(asctime)s | %(message)s')
        handler = logging.handlers.TimedRotatingFileHandler(fpath, when='MIDNIGHT')
        handler.setFormatter(formatter)
        handler.setLevel(logging.FATAL)
        cls.__logger.addHandler(handler)
        cls.__logger.setLevel(logging.DEBUG)
        cls._open_bi_log = True
        if hasattr(cls, 'std_handler'):
            cls.__logger.removeHandler(getattr(cls, 'std_handler'))

    @classmethod
    def show_task_id(cls, enable=True):
        cls._show_task_id = enable

    @classmethod
    def show_location_prefix(cls, enable=True):
        cls._show_prefix = enable

    @classmethod
    def show_debug_network(cls, enable=True):
        cls._show_network = enable

    @classmethod
    def show_debug_redis(cls, enable=True):
        cls._show_redis = enable

    @classmethod
    def set_level(cls, level=logging.DEBUG):
        cls.__logger.setLevel(level)

    @classmethod
    def debug_network(cls, *args):
        if cls._show_network:
            cls.__log(logging.DEBUG, *args)

    @classmethod
    def debug_redis(cls, *args):
        if cls._show_redis:
            cls.__log(logging.DEBUG, *args)

    @classmethod
    def debug(cls, *args):
        cls.__log(logging.DEBUG, *args)

    @classmethod
    def info(cls, *args):
        cls.__log(logging.INFO, *args)

    @classmethod
    def warn(cls, *args):
        cls.__log(logging.WARN, *args)

    @classmethod
    def error(cls, *args):
        cls.__log(logging.ERROR, *args)

    @classmethod
    def exception(cls, *args):
        cls.__log(logging.ERROR, '-' * 100)
        if args and (len(args) > 1 or args[0]):
            cls.__log(logging.ERROR, cls.__serialize_args(*args))
        lines = traceback.format_exc().splitlines()
        for line in lines:
            cls.__log(logging.ERROR, cls.__serialize_args(line))
        cls.__log(logging.ERROR, '-' * 100)

    @classmethod
    def report(cls, *args):
        cls.__log(logging.FATAL, *args)

    @classmethod
    def log(cls, level, *args):
        cls.__log(level, *args)

    @classmethod
    def __log(cls, level, *args):
        if cls.__logger.isEnabledFor(level):
            msg = cls.__serialize_args(*args)
            if cls._show_prefix:
                import inspect
                frame = inspect.currentframe().f_back.f_back
                segs = frame.f_code.co_filename.split('/')
                # filename = frame.f_code.co_filename
                filename = segs[-1]
                log_message = '%s:%s | %s' % (filename, frame.f_lineno, msg)
            else:
                log_message = msg
            if level not in (cls.INFO, cls.BI):
                log_message += _RECOVERY
            if cls._show_task_id:
                import stackless
                log_message = '%016x | %s' % (id(stackless.getcurrent()), log_message)

            logging.log(level, log_message)

    @classmethod
    def __serialize_args(cls, *args):
        log_message = []
        if args:
            for arg in args:
                log_message.append(cls.__to_string(arg))

        return ' '.join(log_message)

    @classmethod
    def __to_string(cls, arg_object):
        return str(arg_object)


Logger = Logger()
