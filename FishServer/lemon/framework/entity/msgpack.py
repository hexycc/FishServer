#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-03

import json


class MsgPack(object):
    def __init__(self, cmd=None, param=None):
        self._ht = {}
        if cmd is not None:
            self.set_cmd(cmd)
        if param is not None:
            self.update_param(param)

    def __str__(self):
        if 'error' in self._ht:
            return '%s' % self._ht['error']
        if 'param' in self._ht:
            return '%s' % self._ht['param']
        return '{}'

    def __repr__(self):
        return 'json ' + self.__str__()

    def set_cmd(self, cmd):
        self._ht['cmd'] = cmd
        return self

    def get_cmd(self):
        return self._ht['cmd']

    def update_param(self, kvs):
        if 'param' not in self._ht:
            self._ht['param'] = {}
        for k, v in kvs.iteritems():
            self._ht['param'][k] = v
        return self

    def set_param(self, key, value):
        if 'param' not in self._ht:
            self._ht['param'] = {}
        self._ht['param'][key] = value
        return self

    def get_param(self, key, default=None):
        if 'param' in self._ht:
            if key in self._ht['param']:
                return self._ht['param'][key]
        return default

    def remove_param(self, *keys):
        if 'param' in self._ht:
            ht = self._ht['param']
            for key in keys:
                if key in ht:
                    del ht[key]
        return self

    def is_error(self):
        return 'error' in self._ht

    def set_error(self, code, desc=None, **kwargs):
        self._ht['error'] = {'error': code}
        if desc:
            self._ht['error']['desc'] = desc
        if kwargs:
            self._ht['error'].update(kwargs)
        return self

    def get_error(self):
        return self._ht['error']

    def clone(self):
        cmd = self._ht['cmd']
        error = self._ht.get('error')
        if error:
            desc = error.get('desc')
            return self.Error(cmd, error['error'], desc)
        param = self._ht.get('param', {})
        return MsgPack(cmd, param)

    @classmethod
    def unpack(cls, cmd, data):
        param = json.loads(data)
        if 'error' in param:
            m = MsgPack(cmd)
            m._ht['error'] = param
            return m
        else:
            return MsgPack(cmd, param)

    @classmethod
    def Error(cls, cmd, code, desc=None, **kwargs):
        m = MsgPack(cmd)
        m.set_error(code, desc, **kwargs)
        return m

    def pack(self):
        if 'error' in self._ht:
            return json.dumps(self._ht['error'], separators=(',', ':'))
        if 'param' in self._ht:
            return json.dumps(self._ht['param'], separators=(',', ':'))
        return '{}'
