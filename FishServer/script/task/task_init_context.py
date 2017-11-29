#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-05-06

from framework.context import Context


def action_init_context(params):
    """初始化上下文"""
    redis = params['server']['redis']
    Context.init_with_redis_json(redis)


game_init_context = action_init_context
sdk_init_context = action_init_context
shell_init_context = action_init_context
