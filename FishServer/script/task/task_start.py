#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-05-11

from framework.helper import Log


def action_start(params):
    """游戏开始"""
    Log.log('start ...')
    if 'start_script' in params:
        cmd = 'sh ' + params['start_script']
        Log.log(cmd)
        import subprocess
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        for line in p.stdout.read().splitlines():
            Log.log(line)


game_start = action_start
sdk_start = action_start
shell_start = action_start
