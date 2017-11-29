#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-05-11

import commands
from framework.helper import Log


def action_stop(params):
    """停止进程"""
    Log.log('stop ...')
    if 'kill_script' in params:
        cmd = 'sh ' + params['kill_script']
        Log.log(cmd)
        status, output = commands.getstatusoutput(cmd)
        if status:
            Log.log(output)
            return status


game_stop = action_stop
sdk_stop = action_stop
shell_stop = action_stop
