#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-02-18

from framework.interface import IContext
from framework.interface import ICallable
from framework.entity.const import Const
from framework.entity.globals import Global


class Configure(IContext, ICallable):
    def __init__(self):
        self._cache = {}
        self._update_time = 0

    def on_startup(self):
        self._update_time = str(Global.config_time())

    def reload(self):
        # reload configitem
        val = self.ctx.RedisConfig.hash_get('configitem', 'update.time')
        if val != self._update_time:
            self.ctx.Log.info('Configure->reload configitem data', val, self._update_time)
            self._cache = {}
            self._update_time = val
        # else:
        #     self.ctx.Log.info('no need to reload config', self._update_time)

    def __get_item__(self, keys, default=None, datatype=0, unescap=False, catalog='configitem'):
        rkey = ':'.join(keys)
        ckey = catalog + '::::' + rkey
        if ckey in self._cache:
            val = self._cache[ckey]
        else:
            val = self.ctx.RedisConfig.hash_get(catalog, rkey)
            # self.ctx.Log.debug('__get_item__', ckey, catalog, rkey, 'val=', val)
            if val is not None:
                if unescap and isinstance(val, (str, unicode)):
                    val = val.replace('\\n', '\n')
                    val = val.replace('\\\\d', '\\d')

                if datatype == Const.data_type_json:
                    val = self.ctx.json_loads(val)
                elif datatype == Const.data_type_int:
                    val = int(val)
                elif datatype == Const.data_type_float:
                    val = float(val)

            self._cache[ckey] = val
        if val is None:
            return default
        else:
            return val

    def get_global_item(self, key, default=None, datatype=Const.data_type_str, unescap=False):
        return self.__get_item__(['global', str(key)], default, datatype, unescap)

    def get_global_item_int(self, key, default=0):
        return self.__get_item__(['global', str(key)], default, Const.data_type_int, False)

    def get_global_item_float(self, key, default=0.0):
        return self.__get_item__(['global', str(key)], default, Const.data_type_float, False)

    def get_global_item_json(self, key, default=None):
        return self.__get_item__(['global', str(key)], default, Const.data_type_json, False)

    def get_game_item(self, gid, key, default=None, datatype=Const.data_type_str, unescap=False):
        return self.__get_item__(['game', str(gid), str(key)], default, datatype, unescap)

    def get_game_item_int(self, gid, key, default=0):
        return self.__get_item__(['game', str(gid), str(key)], default, Const.data_type_int, False)

    def get_game_item_float(self, gid, key, default=0.0):
        return self.__get_item__(['game', str(gid), str(key)], default, Const.data_type_float, False)

    def get_game_item_json(self, gid, key, default=None):
        return self.__get_item__(['game', str(gid), str(key)], default, Const.data_type_json, False)

    def get_room_config(self, gid, roomtype=None, default=None):
        config = self.get_game_item_json(gid, 'room.config')
        if not config:
            return default

        if roomtype is None:
            return config

        for item in config:
            if item.get('room_type') == roomtype:
                return item

        return default


Configure = Configure()
