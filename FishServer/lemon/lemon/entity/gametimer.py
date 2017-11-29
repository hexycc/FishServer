#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-21

from framework.util.log import Logger
from framework.entity.const import Message
from framework.entity.manager import TaskManager
from framework.entity.msgpack import MsgPack
from framework.entity.msgline import MsgLine


class GameTimer(object):
    TIMER_ONCE = 1
    TIMER_LOOP = 2

    def __init__(self, tasklet=None):
        self.type = None
        self.second = None
        self.timer = None
        if tasklet is None:
            from lemon.tasklet.game import GameTasklet
            self.tasklet = GameTasklet
        else:
            self.tasklet = tasklet

    def setTimeout(self, second, param, *args, **kwargs):
        self.type = self.TIMER_ONCE
        self.second = second
        msg = MsgPack(Message.MSG_INNER_TIMER, param)
        uid = msg.get_param('userId')
        gid = msg.get_param('gameId')
        msg = MsgLine(msg.pack(), gid, target=uid).pack()
        task = self.tasklet(Message.to_inner(Message.MSG_INNER_TIMER), msg, None).run
        self.timer = TaskManager.call_later(self.__timeout, second, msg, task, *args, **kwargs)
        return True

    def setInterval(self, interval, param, delay=None, *args, **kwargs):
        self.type = self.TIMER_LOOP
        self.second = interval
        msg = MsgPack(Message.MSG_INNER_TIMER, param)
        uid = msg.get_param('userId')
        gid = msg.get_param('gameId')
        msg = MsgLine(msg.pack(), gid, target=uid).pack()
        task = self.tasklet(Message.to_inner(Message.MSG_INNER_TIMER), msg, None).run
        if delay is None:
            self.timer = TaskManager.call_later(self.__timeout, self.second, msg, task, *args, **kwargs)
        else:
            self.timer = TaskManager.call_later(self.__timeout, delay, msg, task, *args, **kwargs)
        return True

    def getTimerType(self):
        return self.type

    def getLeftTime(self):
        if self.type is None:
            return None
        else:
            return self.timer.getTime()

    def getInterval(self):
        if self.type is None:
            return None
        return self.second

    def delay(self, second):
        try:
            return self.timer.delay(second)
        except:
            return None

    def reset(self, second):
        try:
            self.timer.reset(second)
            self.second = second
            return True
        except:
            return False

    def cancel(self):
        try:
            if self.timer:
                self.timer.cancel()
            self.type = None
            return True
        except:
            return False

    def IsActive(self):
        try:
            return self.timer.active()
        except:
            return False

    def __timeout(self, msg, task, *args, **kwargs):
        try:
            TaskManager.add_task(task)
        except Exception, e:
            Logger.exception(args)

        if self.type == self.TIMER_LOOP:
            self.timer = TaskManager.call_later(self.__timeout, self.second, msg, task, *args, **kwargs)
