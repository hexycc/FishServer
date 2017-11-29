#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-05-06

import os


def action_load_config(params):
    """加载配置"""
    conf_file = params['server']['config.file']
    conf_file = conf_file.replace('/', '.')
    conf_file = conf_file.replace('.py', '')
    exec "import %s" % conf_file
    params['redis.output'] = os.path.join(params['output_dir'], 'redis.output')


game_load_config = action_load_config
sdk_load_config = action_load_config
shell_load_config = action_load_config
