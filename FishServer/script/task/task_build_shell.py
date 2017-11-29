#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-20

import os
import time
from framework.helper import File


def action_build_shell(params, service_type):
    """生成process相关脚本"""
    # 生成启动脚本
    params['shell'] = []
    server = params['server']
    date_time = time.strftime("%Y-%m-%d")
    redis_key = params['redis_key']
    bin_dir = params['bin_dir']

    # 生成启动process脚本
    __make_process_start_script(params, server, date_time, redis_key, bin_dir)

    # 生成启动全部脚本
    __make_start_all(params, date_time, service_type)

    # 生成停止process脚本
    __make_process_stop_script(params, server, date_time)

    # 生成停止全部脚本
    __make_stop_all(params, date_time, redis_key, service_type)

    if service_type == 'game':
        # 生成清理缓存脚本
        __make_redis_clear(params, server, date_time)

    del params['shell']


def __make_process_start_script(params, server, date_time, redis_key, bin_dir):
    # 生成启动脚本
    fpath_py = os.path.join(params['template_dir'], 'start.sh')
    shell_start_template_py = File.read_file(fpath_py)
    for process in server['process']:
        if process['type'] in server['startup']:
            listen_port = process['port']
            process['proc_key'] = "%s:%s:%s" % (redis_key, listen_port, process['id'])
            svrd = 'lemon/framework/service.py'
            s = shell_start_template_py % (date_time, params['service_file'], bin_dir, svrd,
                                           process['proc_key'], process['log_file'])
            fname = "start-" + process['shell_key']
            File.write_file(params['shell_dir'], fname, s)
            params['shell'].append(os.path.join(params['shell_dir'], fname))


def __make_process_stop_script(params, server, date_time):
    # 生成停止脚本
    fpath = os.path.join(params['template_dir'], 'stop.sh')
    shell_stop_template = File.read_file(fpath)
    for process in server['process']:
        if process['type'] in server['startup']:
            s = shell_stop_template % (date_time, params['service_file'], process['proc_key'], params['bin_dir'])
            fname = "kill-" + process['shell_key']
            File.write_file(params['shell_dir'], fname, s)
            params['shell'].append(os.path.join(params['shell_dir'], fname))


def __make_redis_clear(params, server, date_time):
    fpath = os.path.join(params['template_dir'], 'redis-cache-clear.sh')
    shell_clear_cache = File.read_file(fpath)
    cache_redis = server['redis']['cache']
    s = shell_clear_cache % (date_time, params['service_file'], params['bin_dir'], cache_redis['host'],
                             cache_redis['port'], cache_redis['db'])
    File.write_file(params['shell_dir'], 'redis-cache-clear.sh', s)
    params['clear_script'] = os.path.join(params['shell_dir'], 'redis-cache-clear.sh')


def __make_start_all(params, date_time, service_type):
    if params['shell']:
        shell_template = '''
#!/usr/bin/env bash
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: %s

export service_file=%s

sh %s
    ''' % (date_time, params['service_file'], '\nsh '.join(params['shell']))
        fname = 'start-%s-all.sh' % service_type
        File.write_file(params['shell_dir'], fname, shell_template)
        params['shell'].append(os.path.join(params['shell_dir'], fname))
        params['start_script'] = os.path.join(params['shell_dir'], fname)


def __make_stop_all(params, date_time, redis_key, service_type):
    if params['shell']:
        fpath = os.path.join(params['template_dir'], 'stop.sh')
        shell_stop_template = File.read_file(fpath)

        # 生成停止全部脚本
        s = shell_stop_template % (date_time, params['service_file'], redis_key, params['bin_dir'])
        fname = 'kill-%s-all.sh' % service_type
        File.write_file(params['shell_dir'], fname, s)
        params['shell'].append(os.path.join(params['shell_dir'], fname))
        params['kill_script'] = os.path.join(params['shell_dir'], fname)


def game_build_shell(params):
    action_build_shell(params, 'game')


def sdk_build_shell(params):
    action_build_shell(params, 'sdk')


def shell_build_shell(params):
    action_build_shell(params, 'shell')
