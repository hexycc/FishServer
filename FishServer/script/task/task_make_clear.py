#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-27

import commands
from framework.helper import Log


def game_make_clear(params):
    """清理缓存"""
    Log.log('clear redis cache ...')
    cmd = 'sh ' + params['clear_script']
    Log.log(cmd)
    status, output = commands.getstatusoutput(cmd)
    if status:
        Log.log(output)
        return status
