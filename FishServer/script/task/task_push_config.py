#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-05-11

from framework.context import Context
from framework.helper import File


def action_push_config(params):
    """推送配置"""
    data = File.read_file(params['redis.output'])
    j = Context.json_loads(data)
    for item in j:
        Context.RedisConfig.execute(*item)


def game_push_config(params):
    action_push_config(params)
    Context.RedisCache.set('connect.server', Context.json_dumps(params['connect.server']))


sdk_push_config = action_push_config
shell_push_config = action_push_config
