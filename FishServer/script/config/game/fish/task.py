#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-01-12

from framework.helper import *

add_game_config(2, 'task.config', {
    'task': [
        {'type': 1, 'desc': u'捕获', 'range': [10, 50], 'degree': [[30, 10], [10, 5]]},
        {'type': 2, 'desc': u'捕获首领', 'range': [1, 3], 'degree': 10},
        {'type': 3, 'desc': u'捕获奖金鱼', 'range': [3, 5], 'degree': 10},
        {'type': 11, 'desc': u'赚取金币', 'range': [300, 500], 'degree': 10},
        {'type': 21, 'desc': u'每日登陆', 'degree': 10},
        {'type': 31, 'desc': u'充值任意金额', 'degree': 20}
    ],
    'daily': [
        [2, 3, 11, 21],
        [2, 3, 11, 21],
        [2, 3, 11, 21],
        [2, 3, 11, 21],
        [2, 3, 11, 21],
        [2, 3, 11, 21],
        [2, 3, 11, 21, 31],
    ],
    'total_degree': 100,
    'reward': [
        {'degree': 50, 'reward': {'chip': 2000}},
        {'degree': 80, 'reward': {'chip': 5000}},
        {'degree': 100, 'reward': {'chip': 10000}},
    ]
})
