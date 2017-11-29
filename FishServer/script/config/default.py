#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-05-06

from framework.helper import *

add_global_config('shell.access_key', '0c3f53dc3a9ce8cd6d9b7f88793b3620')
add_global_config('ip.limit.user', 20)

add_game_config(2, 'appKey', 'jiyu_self_game_2_hGvtylaIYuJAOAuJ')

add_global_config('game.desc', [
    {'id': 2, 'name': u'天天捕鱼'}
])

from config.game.fish import *
