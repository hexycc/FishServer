#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-09-14

import json
from framework.interface import IContext
from framework.interface import ICallable


class Global(IContext, ICallable):
    def __init__(self):
        self.params = {}
        self.start_key = {}
        self.process_info = {}

    def load_static_data(self):
        import os
        bin_dir = os.environ.get('bin_dir')
        control_path = os.path.join(bin_dir, 'output/control.json')
        with open(control_path) as f:
            self.params = json.load(f)
        proc_key = os.environ.get('proc_key')
        data = proc_key.split(':')
        self.start_key['redis.host'] = data[0]
        self.start_key['redis.port'] = int(data[1])
        self.start_key['redis.db'] = int(data[2])
        self.start_key['tcp.port'] = int(data[3])
        for process in self.params['server']['process']:
            if process['id'] == int(data[4]):
                self.process_info = process
                break
        else:
            raise Exception('can not find config of process', int(data[4]))

    def dump_static_info(self):
        pass

    def process_type(self):
        return self.process_info['type']

    def process_id(self):
        return self.process_info['id']

    def proc_key(self):
        return self.process_info['proc_key']

    def log_path(self):
        return self.process_info['log_file']

    def bi_log_path(self):
        return self.process_info['bi_log_file']

    def network_log_path(self):
        return self.process_info['network_log_file']

    def web_root(self):
        return self.params['web_root']

    def run_mode(self):
        return self.params['server']['mode']

    def bin_dir(self):
        return self.params['bin_dir']

    def http_game(self):
        return self.params['server']['http.game']

    def http_sdk(self):
        return self.params['server']['http.sdk']

    def debug_flag(self):
        return self.params['server'].get('debug', [])

    def config_time(self):
        return self.params['update.time']

    def is_first(self):
        return 'first' in self.process_info


Global = Global()
