#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-02-12

import os
import random


def init_context(redis_config):
    random.seed()
    from context import Context
    Context.Log.info('context init in')

    Context.init_with_redis_key(redis_config)
    Context.load_lua_script()

    Context.Configure.on_startup()

    bin_dir = Context.Global.bin_dir()
    keyword_path = os.path.join(bin_dir, 'script/resource/filter_keywords.txt')
    Context.KeywordFilter.loadFromFile(keyword_path, 'utf-8')
    Context.Log.info('load filter keywords from', keyword_path)

    Context.Log.info('context init out')
    Context.Log.info('server is first process', Context.Global.is_first())


def init_log(log_path, bi_log_path):
    from context import Context
    Context.Log.open_log(log_path)
    Context.Log.open_bi_log(bi_log_path)
    Context.Log.info('log init in')
    flags = Context.Global.debug_flag()
    Context.Log.show_debug_network('network' in flags)
    Context.Log.show_debug_redis('redis' in flags)
    if 'debug' not in flags:
        Context.Log.set_level(Context.Log.INFO)
    Context.Log.info('log init out')
