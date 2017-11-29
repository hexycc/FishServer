#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-05-06

import os
from framework.helper import File


def action_log_conf(params):
    """生成process对应log配置文件"""
    File.make_dirs(params['log_dir'])
    server = params['server']
    for process in server['process']:
        log_key = process['log_key']
        bi_log = os.path.join(params['log_dir'], 'bi-%s.log' % log_key)
        common_log = os.path.join(params['log_dir'], '%s.log' % log_key)
        process['bi_log_file'] = bi_log
        process['log_file'] = common_log


game_log_conf = action_log_conf
sdk_log_conf = action_log_conf
shell_log_conf = action_log_conf
