#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-03-09

import stackless
from framework.interface import ICallable


def __lock_obj_attr__(*args, **kwargs):
    raise Exception('Can Not Modify Lock Object !!')


class LockAttr(ICallable):
    def __init__(self):
        self.lock(self)

    @classmethod
    def lock(cls, obj):
        object.__setattr__(obj, '__setattr__', __lock_obj_attr__)

    @classmethod
    def unlock(cls, obj):
        if isinstance(obj, object):
            fun = obj.__getattribute__('__setattr__')
            if fun == __lock_obj_attr__:
                obj.__delattr__('__setattr__')


LockAttr = LockAttr()


class Locker(stackless.channel):
    def __init__(self, label=''):
        super(Locker, self).__init__(label)
        self.owner = None
        self.locked = False

    def lock(self):
        if not self.locked:
            self.locked = True
            self.owner = stackless.getcurrent()
            return True

        if self.owner == stackless.getcurrent():
            return False

        self.receive()
        self.locked = True
        self.owner = stackless.getcurrent()
        return True

    def unlock(self):
        if not self.locked:
            return True

        if self.owner != stackless.getcurrent():
            return False

        self.locked = False
        self.owner = None
        if self.balance < 0:
            self.send(True)

        return True

    def grab(self):
        self.locked = True
        self.owner = stackless.getcurrent()
        return True

    def __enter__(self):
        self.lock()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unlock()


class LockerMap(object):
    def __init__(self):
        self.map = {}

    def lock(self, key):
        if key not in self.map:
            self.map[key] = Locker(key)
        locker = self.map[key]
        return locker.lock()

    def unlock(self, key, rm=False):
        if key not in self.map:
            return True
        locker = self.map[key]
        ret = locker.unlock()
        if rm:
            del self.map[key]
        return ret

    def remove(self, key):
        if key in self.map:
            del self.map[key]
        return True

    def __len__(self):
        return len(self.map)

    def __iter__(self):
        return iter(self.map)

    def popitem(self):
        return self.map.popitem()

    def __getitem__(self, item):
        if item not in self.map:
            self.map[item] = Locker(item)
        return self.map[item]
