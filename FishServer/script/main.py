#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-20

import os
import sys

from framework.helper import Log
from framework.entity.manager import TaskManager


def useage():
    print '''
Usage:
    game.sh -config [service_file]   编译整个游戏工程
    game.sh -action start            启动所有服务进程
    game.sh -action stop             停止所有服务进程
    game.sh -help                    打印帮助并退出
'''
    return 0


def parse_cmd_lines():
    param = {}
    for x in xrange(2, len(sys.argv)):
        flg = sys.argv[x]
        if flg == '-config' or flg == '-c':
            x += 1
            param['service_file'] = os.path.abspath(sys.argv[x])
        elif flg == '-action' or flg == '-a':
            x += 1
            param['action'] = sys.argv[x]
        elif flg == '-h' or flg == '-help':
            param['help'] = True
            return param
    #
    # if 'service_file' not in param:
    #     raise Exception('miss service file')

    file_path = os.path.abspath(__file__)
    param['script_dir'] = os.path.dirname(file_path)
    param['src_dir'] = os.path.dirname(param['script_dir'])
    param['root_dir'] = os.path.dirname(param['src_dir'])
    param['log_dir'] = param['root_dir'] + '/log'
    param['bin_dir'] = param['root_dir'] + '/bin'
    param['shell_dir'] = param['bin_dir'] + '/shell'
    param['output_dir'] = param['bin_dir'] + '/output'
    param['lua_dir'] = param['script_dir'] + '/lua'
    param['template_dir'] = param['script_dir'] + '/template'
    param['web_root'] = param['bin_dir'] + '/webroot'
    return param


def get_user_name(params):
    import getpass
    params['username'] = getpass.getuser()


def main():
    if sys.argv[1] not in ('game', 'sdk', 'shell'):
        raise Exception('game, sdk or shell please !!!')

    service_type = sys.argv[1]
    params = parse_cmd_lines()
    if params.get('help'):
        useage()
    else:
        get_user_name(params)
        tasks = []
        if 'service_file' in params:
            tasks.append('load_server')
            tasks.append('log_conf')
            tasks.append('copy_file')
            tasks.append('build_shell')
            tasks.append('load_config')
            tasks.append('init_context')
            tasks.append('load_lua')
            tasks.append('make_end')
        action = params.get('action')
        if action == 'start':
            tasks.append('stop')
            tasks.append('push_config')
            if service_type == 'game':
                tasks.append('make_clear')
                tasks.append('start')
            elif service_type == 'sdk':
                tasks.append('start')
            elif service_type == 'shell':
                tasks.append('start')
        elif action == 'stop':
            tasks.append('stop')

        if not tasks:
            useage()
        else:
            Log.log('begin start')
            Log.log('=================================================')
            for step, task in enumerate(tasks, 1):
                Log.log('---------%2s/%s: %s_%s' % (step, len(tasks), service_type, task))
                func = None
                exec 'from task.task_%s import %s_%s as func' % (task, service_type, task)
                if func(params):
                    raise Exception('start failed !!!')
            Log.log('=================================================')
            Log.log('start done')
    TaskManager.add_simple_task(TaskManager.end_loop)


if __name__ == '__main__':
    TaskManager.add_simple_task(main)
    TaskManager.start_loop()
