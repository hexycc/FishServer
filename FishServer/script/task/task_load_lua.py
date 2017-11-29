#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-05-06

import os
from framework.context import Context


def action_load_lua(params):
    # 加载所有lua脚本
    lua_map = {}
    for fname in os.listdir(params['lua_dir']):
        fpath = os.path.join(params['lua_dir'], fname)
        if os.path.isfile(fpath):
            with open(fpath) as f:
                content = f.read()
                f.close()
                lua_name = fname[:-4]
                Context.RedisMix.load_lua_script(lua_name, content)
                Context.RedisPay.load_lua_script(lua_name, content)
                Context.RedisStat.load_lua_script(lua_name, content)
                Context.RedisCache.load_lua_script(lua_name, content)
                sha1 = Context.RedisCluster.load_lua_script(lua_name, content)
                lua_map[lua_name] = sha1

    from framework.helper import add_global_config
    add_global_config('redis.lua', lua_map)


game_load_lua = action_load_lua
sdk_load_lua = game_load_lua
shell_load_lua = game_load_lua
