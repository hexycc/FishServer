#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-06-25

import os
import commands
from framework.helper import File
from framework.helper import Log


def action_copy_file(params, *dirs):
    cmds = []
    for d in dirs:
        from_dir = os.path.join(params['src_dir'], d)
        up_dir = os.path.dirname(from_dir)
        File.make_dirs(up_dir)
        cmd = 'cd %s; tar -cf - %s --exclude=*.pyc --exclude=*.c | tar -xf - -C %s' % (up_dir, d, params['bin_dir'])
        cmds.append(cmd)

    File.make_dirs(params['bin_dir'])
    for cmd in cmds:
        Log.log(cmd)
        status, output = commands.getstatusoutput(cmd)
        if status:
            Log.log(output)
            return status


def game_copy_file(params):
    return action_copy_file(params, 'lemon', 'script')


def sdk_copy_file(params):
    return action_copy_file(params, 'lemon', 'script', 'webroot')


shell_copy_file = game_copy_file
