#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-03-17


class MsgLine(object):
    FIELD_SEPARATOR = '\20'
    MSG_SEPARATOR = '\21'

    def __init__(self, raw, gid=None, room=None, target=None):
        self.target = target
        self.gid = gid
        self.room = room
        self.raw = raw

    def pack(self):
        fileds = []
        if self.gid:
            fileds.append(str(self.gid))
        else:
            fileds.append('')
        if self.room:
            fileds.append(str(self.room))
        else:
            fileds.append('')
        if isinstance(self.target, int):
            fileds.append(str(self.target))
        elif isinstance(self.target, list):
            _target = []
            for t in self.target:
                _target.append(str(t))
            fileds.append(','.join(_target))
        else:
            fileds.append('')
        fileds.append(self.raw)

        return self.FIELD_SEPARATOR.join(fileds)

    @classmethod
    def unpack(cls, line):
        _gid, _room, _target, _msg = line.split(cls.FIELD_SEPARATOR, 4)
        if _gid:
            _gid = int(_gid)
        if _room:
            _room = int(_room)
        target = None
        if _target:
            try:
                target = int(_target)
            except:
                _target = _target.split(',')
                target = [int(t) for t in _target]
        return MsgLine(_msg, _gid, _room, target)

    def fast_param_str(self, key, default=None):
        key = '"' + key + '":'
        i = self.raw.find(key)
        if i > 0:
            x = self.raw.find('"', i + len(key))
            y = self.raw.find('"', x + 1)
            return self.raw[x + 1:y]
        else:
            return default

    def fast_param_int(self, key, default=None):
        pos = self.raw.find('"' + key + '":')
        if pos == -1:
            return default
        data = self.raw[pos + len(key) + 3:].strip()
        end = 0
        for x in data:
            if '0' <= x <= '9':
                end += 1
            else:
                break
        if end:
            return int(data[:end])
        return default

    def get_uid(self):
        return self.target

    def get_gid(self):
        return self.gid

    def get_room(self):
        return self.room

    def get_message(self):
        return self.raw

    def to_msgpack(self, cmd):
        from msgpack import MsgPack
        return MsgPack.unpack(cmd, self.raw)
