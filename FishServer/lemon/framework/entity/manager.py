#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-02-13

import stackless
from twisted.internet import reactor
from framework.entity.simple import SimpleTasklet
from framework.util.log import Logger


class TaskManager(object):
    @classmethod
    def current(cls):
        tasklet = stackless.getcurrent()
        return tasklet._class_instance

    @classmethod
    def add_task(cls, task, *args, **kwargs):
        curr = stackless.tasklet(task)(*args, **kwargs)
        reactor.callLater(0, stackless.schedule)
        return curr

    @classmethod
    def add_delay_task(cls, delay, task, *args, **kwargs):
        assert delay >= 0
        reactor.callLater(delay, cls.add_task, task, *args, **kwargs)

    @classmethod
    def add_simple_task(cls, start_routine, *args, **kwargs):
        tasklet = SimpleTasklet(start_routine)
        return cls.add_task(tasklet.run, *args, **kwargs)

    @classmethod
    def run_task(cls, task, *args, **kwargs):
        task.run(*args, **kwargs)

    @classmethod
    def call_later(cls, start_routine, delay=0, *args, **kwargs):
        return reactor.callLater(delay, start_routine, *args, **kwargs)

    @classmethod
    def set_timeout(cls, start_routine, delay=0, *args, **kwargs):
        return reactor.callLater(delay, start_routine, *args, **kwargs)

    @classmethod
    def set_interval(cls, start_routine, delay, interval, *args, **kwargs):
        def __dispatch(start_routine, *args, **kwargs):
            try:
                start_routine(*args, **kwargs)
            except Exception, e:
                Logger.exception(start_routine, args, kwargs)
            return reactor.callLater(interval, __dispatch, start_routine, *args, **kwargs)

        return reactor.callLater(delay, __dispatch, start_routine, *args, **kwargs)

    @classmethod
    def schedule(cls, retval=None):
        # return stackless.schedule(retval)
        return reactor.callLater(0, stackless.schedule, retval)

    @classmethod
    def start_loop(cls):
        delattr(cls, 'start_loop')
        stackless.tasklet(reactor.run)()
        reactor.callLater(0, stackless.schedule)
        stackless.run()

    @classmethod
    def end_loop(cls):
        reactor.stop()

    @classmethod
    def count(cls):
        return stackless.getruncount()
