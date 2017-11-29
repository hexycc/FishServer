#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-05-06

import os
import json
import copy
from framework.helper import File
from framework.helper import Global
from framework.helper import add_global_config


def action_load_server(params):
    """加载服务器配置文件"""
    if 'service_file' not in params:
        raise Exception('miss service_file')

    data = File.read_file(params['service_file'])
    params['server'] = json.loads(data)
    mode = params['server']['mode']
    Global.run_mode = mode
    Global.http_game = params['server']['http.game']

    server = params['server']
    for k in ('host', 'port', 'db'):
        v = os.environ.get('redis_%s' % k, None)
        if v:
            server['redis.%s' % k] = v if k == 'host' else int(v)
        if 'redis.%s' % k in server:
            server['redis']['config'][k] = server['redis.%s' % k]

    http_port = server.get('http.port', 8080)
    http_port = os.environ.get('http_port', http_port)
    server['http.port'] = int(http_port)

    tcp_port = os.environ.get('tcp_port', None)
    if tcp_port:
        server['tcp.port'] = int(tcp_port)

    type_set = set()
    tcp_port = server['tcp.port']
    http_port = server['http.port']
    for process in server['process']:
        if process['type'] not in type_set:
            type_set.add(process['type'])
            process['first'] = 1
        if process['type'] == 'sdk':
            process['port'] = http_port
            http_port += 2
        else:
            process['port'] = tcp_port
            tcp_port += 2
        process['shell_key'] = '%s-%s-%05d.sh' % (process['type'], server['name'], process['id'])
        process['log_key'] = '%s-%s-%05d' % (process['type'], server['name'], process['id'])

    redis_info = params['server']['redis']
    redis_key = '%s:%s:%s' % (redis_info['config']['host'], redis_info['config']['port'], redis_info['config']['db'])
    params['redis_key'] = redis_key

    add_global_config('redis.config', redis_info)


def __build_server_info(params):
    servers, processes = params['server']['servers'], params['server']['process']
    server_map = {}
    for p in processes:
        t = {
            'serverId': p['id'],
            'host': servers[p['server']]['intranet'],
            'internet': servers[p['server']]['internet'],
            'port': p['port'],
        }
        if 'first' in p:
            t['first'] = p['first']
        if 'domain' in servers[p['server']]:
            t['domain'] = servers[p['server']]['domain']
        else:
            t['domain'] = t['internet']
        if p['type'] not in server_map:
            server_map[p['type']] = []
        server_map[p['type']].append(t)

    add_global_config('server.map', server_map)
    return server_map


def game_load_server(params):
    action_load_server(params)
    server_map = __build_server_info(params)
    connect_server = copy.deepcopy(server_map['connect'])
    for conn in connect_server:
        conn['port'] += 1
    add_global_config('connect.server', connect_server)
    params['connect.server'] = connect_server


def sdk_load_server(params):
    action_load_server(params)
    __build_server_info(params)


shell_load_server = sdk_load_server
