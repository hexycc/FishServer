#!/usr/bin/env python
# -*- coding=utf-8 -*-

# author: likebeta <ixxoo.me@gmail.com>
# create: 2015-12-02

import random
from framework.helper import *

add_game_config(2, 'room.config', [
    {
        'room_type': 201,
        'room_name': u'百跑场',
        'room_fee': 0,
        'base_point': 1,
        'chip_min': 0,
        'chip_max': -1,
        'barrel_min': 1,            # 能进入最小炮倍数
        'barrel_max': 25,           # 能进入最大炮倍数
        'level_min': 1,
        'level_max': 13,
        'barrel_min1': 1,           # 能开炮最小开炮倍数
        'barrel_max1': 25,          # 能开炮最大炮倍数
        'level_min1': 1,
        'level_max1': 13,
    },
    {
        'room_type': 202,
        'room_name': u'千炮场',
        'room_fee': 0,
        'base_point': 1,
        'chip_min': 0,
        'chip_max': -1,
        'barrel_min': 30,
        'barrel_max': 10000,
        'level_min': 14,
        'level_max': 54,
        'barrel_min1': 30,
        'barrel_max1': 1000,
        'level_min1': 14,
        'level_max1': 36,
    },
    {
        'room_type': 203,
        'room_name': u'万炮场',
        'room_fee': 0,
        'base_point': 1,
        'chip_min': 100000,
        'chip_max': -1,
        'barrel_min': 300,
        'barrel_max': 10000,
        'level_min': 27,
        'level_max': 54,
        'barrel_min1': 300,
        'barrel_max1': 10000,
        'level_min1': 27,
        'level_max1': 54,
        # 'red_dragon': 1
    },
])

if Global.run_mode == 1:
    add_room_map(2, 201, 20000)
    add_room_map(2, 202, 20002)
    add_room_map(2, 203, 20004)
elif Global.run_mode == 2:
    add_room_map(2, 201, 20000)
    add_room_map(2, 202, 20002)
    add_room_map(2, 203, 20004)
else:
    add_room_map(2, 201, 20000)
    add_room_map(2, 202, 20000)
    add_room_map(2, 203, 20000)

add_game_config(2, 'timeline.201.config', {
    'total': 17 * 60,
    'boss': [300, 630],
    'tide': [16 * 60],
    'bounty': []
})

add_game_config(2, 'timeline.202.config', {
    'total': 21 * 60,
    'boss': [300, 630],
    'tide': [20 * 60],
    'bounty': [16 * 60]
})

add_game_config(2, 'timeline.203.config', {
    'total': 21 * 60,
    'boss': [300, 630],
    'tide': [20 * 60],
    'bounty': [16 * 60]
})

add_game_config(2, 'super.weapon.201.config', {'fix': 30 * 400, 'multi': 30, 'dead': 10})
add_game_config(2, 'super.weapon.202.config', {'fix': 300 * 400, 'multi': 300, 'dead': 10})
add_game_config(2, 'super.weapon.203.config', {'fix': 300 * 400, 'multi': 300, 'dead': 10})

add_game_config(2, 'bonus.pool.ratio', 0.1)

__barrel_unlock_config = [
    {'level': 1, 'multiple': 1},  # 默认已解锁
    {'level': 2, 'multiple': 2, 'diamond': 2, 'reward': {'chip': 100}},
    {'level': 3, 'multiple': 3, 'diamond': 2, 'reward': {'chip': 100}},
    {'level': 4, 'multiple': 4, 'diamond': 3, 'reward': {'chip': 150}},
    {'level': 5, 'multiple': 5, 'diamond': 3, 'reward': {'chip': 150}},
    {'level': 6, 'multiple': 6, 'diamond': 5, 'reward': {'chip': 200}},
    {'level': 7, 'multiple': 7, 'diamond': 5, 'reward': {'chip': 200}},
    {'level': 8, 'multiple': 8, 'diamond': 5, 'reward': {'chip': 200}},
    {'level': 9, 'multiple': 9, 'diamond': 5, 'reward': {'chip': 200}},
    {'level': 10, 'multiple': 10, 'diamond': 8, 'reward': {'chip': 500}},
    {'level': 11, 'multiple': 15, 'diamond': 8, 'reward': {'chip': 1000}},
    {'level': 12, 'multiple': 20, 'diamond': 8, 'reward': {'chip': 1000}},
    {'level': 13, 'multiple': 25, 'diamond': 8, 'reward': {'chip': 2000}},
    {'level': 14, 'multiple': 30, 'diamond': 8, 'reward': {'chip': 2000}},
    {'level': 15, 'multiple': 35, 'diamond': 10, 'reward': {'chip': 3000}},
    {'level': 16, 'multiple': 40, 'diamond': 10, 'reward': {'chip': 3000}},
    {'level': 17, 'multiple': 45, 'diamond': 10, 'reward': {'chip': 5000}},
    {'level': 18, 'multiple': 50, 'diamond': 10, 'reward': {'chip': 5000}},
    {'level': 19, 'multiple': 60, 'diamond': 20, 'reward': {'chip': 6000}},
    {'level': 20, 'multiple': 70, 'diamond': 20, 'reward': {'chip': 6000}},
    {'level': 21, 'multiple': 80, 'diamond': 20, 'reward': {'chip': 7000}},
    {'level': 22, 'multiple': 90, 'diamond': 20, 'reward': {'chip': 7000}},
    {'level': 23, 'multiple': 100, 'diamond': 20, 'reward': {'chip': 8000}},
    {'level': 24, 'multiple': 150, 'diamond': 30, 'reward': {'chip': 8000}},
    {'level': 25, 'multiple': 200, 'diamond': 40, 'reward': {'chip': 10000}},
    {'level': 26, 'multiple': 250, 'diamond': 50, 'reward': {'chip': 10000}},
    {'level': 27, 'multiple': 300, 'diamond': 60, 'reward': {'chip': 15000}},
    {'level': 28, 'multiple': 350, 'diamond': 70, 'reward': {'chip': 15000}},
    {'level': 29, 'multiple': 400, 'diamond': 80, 'reward': {'chip': 20000}},
    {'level': 30, 'multiple': 450, 'diamond': 90, 'reward': {'chip': 20000}},
    {'level': 31, 'multiple': 500, 'diamond': 100, 'reward': {'chip': 30000}},
    {'level': 32, 'multiple': 600, 'diamond': 150, 'reward': {'chip': 40000}},
    {'level': 33, 'multiple': 700, 'diamond': 200, 'reward': {'chip': 50000}},
    {'level': 34, 'multiple': 800, 'diamond': 250, 'reward': {'chip': 60000}},
    {'level': 35, 'multiple': 900, 'diamond': 300, 'reward': {'chip': 70000}},
    {'level': 36, 'multiple': 1000, 'diamond': 500, 'reward': {'chip': 100000}},

    {'level': 37, 'multiple': 1500, 'stone': 10, 'diamond': 20, 'gem': 200, 'fail_gem': [4, 6], 'ratio': 0.4,
     'reward': {'chip': 0}},
    {'level': 38, 'multiple': 2000, 'stone': 10, 'diamond': 20, 'gem': 300, 'fail_gem': [4, 6], 'ratio': 0.35,
     'reward': {'chip': 0}},
    {'level': 39, 'multiple': 2500, 'stone': 10, 'diamond': 20, 'gem': 400, 'fail_gem': [4, 6], 'ratio': 0.30,
     'reward': {'chip': 0}},
    {'level': 40, 'multiple': 3000, 'stone': 10, 'diamond': 20, 'gem': 500, 'fail_gem': [4, 6], 'ratio': 0.25,
     'reward': {'chip': 0}},
    {'level': 41, 'multiple': 3500, 'stone': 10, 'diamond': 20, 'gem': 600, 'fail_gem': [6, 8], 'ratio': 0.01,
     'reward': {'chip': 0}},
    {'level': 42, 'multiple': 4000, 'stone': 10, 'diamond': 20, 'gem': 700, 'fail_gem': [6, 8], 'ratio': 0.09,
     'reward': {'chip': 0}},
    {'level': 43, 'multiple': 4500, 'stone': 10, 'diamond': 20, 'gem': 800, 'fail_gem': [6, 8], 'ratio': 0.05,
     'reward': {'chip': 0}},
    {'level': 44, 'multiple': 5000, 'stone': 10, 'diamond': 20, 'gem': 1000, 'fail_gem': [6, 8], 'ratio': 0.07,
     'reward': {'chip': 0}},
    {'level': 45, 'multiple': 5500, 'stone': 10, 'diamond': 20, 'gem': 1200, 'fail_gem': [8, 10], 'ratio': 0.06,
     'reward': {'chip': 0}},
    {'level': 46, 'multiple': 6000, 'stone': 10, 'diamond': 20, 'gem': 1400, 'fail_gem': [8, 10], 'ratio': 0.05,
     'reward': {'chip': 0}},
    {'level': 47, 'multiple': 6500, 'stone': 10, 'diamond': 20, 'gem': 1600, 'fail_gem': [8, 10], 'ratio': 0.04,
     'reward': {'chip': 0}},
    {'level': 48, 'multiple': 7000, 'stone': 10, 'diamond': 20, 'gem': 1800, 'fail_gem': [8, 10], 'ratio': 0.03,
     'reward': {'chip': 0}},
    {'level': 49, 'multiple': 7500, 'stone': 10, 'diamond': 20, 'gem': 2000, 'fail_gem': [8, 10], 'ratio': 0.02,
     'reward': {'chip': 0}},
    {'level': 50, 'multiple': 8000, 'stone': 10, 'diamond': 20, 'gem': 2500, 'fail_gem': [8, 10], 'ratio': 0.01,
     'reward': {'chip': 0}},
    {'level': 51, 'multiple': 8500, 'stone': 10, 'diamond': 20, 'gem': 3000, 'fail_gem': [8, 10], 'ratio': 0.005,
     'reward': {'chip': 0}},
    {'level': 52, 'multiple': 9000, 'stone': 10, 'diamond': 20, 'gem': 3500, 'fail_gem': [8, 10], 'ratio': 0.0025,
     'reward': {'chip': 0}},
    {'level': 53, 'multiple': 9500, 'stone': 10, 'diamond': 20, 'gem': 4000, 'fail_gem': [8, 10], 'ratio': 0.00125,
     'reward': {'chip': 0}},
    {'level': 54, 'multiple': 10000, 'stone': 10, 'diamond': 20, 'gem': 8000, 'fail_gem': [8, 10], 'ratio': 0.000625,
     'reward': {'chip': 0}},
]

add_game_config(2, 'barrel.unlock.config', __barrel_unlock_config)

__barrel_level_config = [t['multiple'] for t in __barrel_unlock_config]
add_game_config(2, 'barrel.level.config', __barrel_level_config)

add_game_config(2, 'login.reward', {
    'common': [1000, 2000, 3000, 4000, 5000, 8000, 10000],
    'vip': [2000, 3000, 4000, 5000, 10000, 16000, 20000],
    'new': [{'chip': 1000},
            {'diamond': 100},
            {'props': [{'id': 211, 'count': 1}]},
            {'chip': 4000},
            {'props': [{'id': 212, 'count': 1}]},
            {'chip': 6000},
            {'props': [{'id': 213, 'count': 1}]}],
})

add_game_config(2, 'game.startup', 100)

add_game_config(2, 'benefit.config', {
    'reward': [
        {'chip': 5000, 'wait': 30},
        {'chip': 5000, 'wait': 120},
        {'chip': 5000, 'wait': 300},
    ],
    # 'limit': 0,
})

add_game_config(2, 'exp.level', [0, 5, 20, 50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 51200, 102400,
                                 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1100000,
                                 1200000, 1300000, 1400000, 1500000, 1600000])

add_game_config(2, 'exp.level.reward', [
    {'chip': 100, 'coupon': 10, 'props': [{'id': 201, 'count': 1}, {'id': 202, 'count': 1},
                                          {'id': 203, 'count': 1}, {'id': 204, 'count': 1}, {'id': 205, 'count': 1}]},
    {'chip': 150, 'diamond': 10, 'props': [{'id': 205, 'count': 2}, {'id': 201, 'count': 1}]},
    {'chip': 200, 'diamond': 10, 'props': [{'id': 205, 'count': 2}, {'id': 201, 'count': 1}]},
    {'chip': 250, 'diamond': 10, 'props': [{'id': 205, 'count': 2}, {'id': 201, 'count': 1}]},
    {'chip': 300, 'diamond': 5, 'props': [{'id': 204, 'count': 1}]},
    {'chip': 350, 'diamond': 6, 'props': [{'id': 202, 'count': 1}, {'id': 201, 'count': 1}]},
    {'chip': 400, 'diamond': 7, 'props': [{'id': 202, 'count': 1}, {'id': 201, 'count': 1}]},
    {'chip': 450, 'diamond': 8, 'props': [{'id': 202, 'count': 1}, {'id': 201, 'count': 1}]},
    {'chip': 500, 'diamond': 9, 'props': [{'id': 202, 'count': 1}, {'id': 201, 'count': 1}]},
    {'chip': 550, 'diamond': 10, 'props': [{'id': 204, 'count': 1}, {'id': 203, 'count': 1}]},
    {'chip': 600, 'diamond': 11, 'props': [{'id': 205, 'count': 2}, {'id': 201, 'count': 2}]},
    {'chip': 650, 'diamond': 12, 'props': [{'id': 205, 'count': 2}, {'id': 201, 'count': 2}]},
    {'chip': 700, 'diamond': 13, 'props': [{'id': 205, 'count': 2}, {'id': 201, 'count': 2}]},
    {'chip': 750, 'diamond': 14, 'props': [{'id': 205, 'count': 2}, {'id': 201, 'count': 2}]},
    {'chip': 800, 'diamond': 15, 'props': [{'id': 204, 'count': 2}]},
    {'chip': 850, 'diamond': 16, 'props': [{'id': 202, 'count': 1}, {'id': 201, 'count': 2}]},
    {'chip': 900, 'diamond': 17, 'props': [{'id': 202, 'count': 1}, {'id': 201, 'count': 2}]},
    {'chip': 950, 'diamond': 18, 'props': [{'id': 202, 'count': 1}, {'id': 201, 'count': 2}]},
    {'chip': 1000, 'diamond': 19, 'props': [{'id': 202, 'count': 1}, {'id': 201, 'count': 2}]},
    {'chip': 1050, 'diamond': 20, 'props': [{'id': 204, 'count': 2}, {'id': 203, 'count': 2}]},
    {'chip': 1100, 'diamond': 21, 'props': [{'id': 205, 'count': 3}, {'id': 201, 'count': 3}]},
    {'chip': 1150, 'diamond': 22, 'props': [{'id': 205, 'count': 3}, {'id': 201, 'count': 3}]},
    {'chip': 1200, 'diamond': 23, 'props': [{'id': 205, 'count': 3}, {'id': 201, 'count': 3}]},
    {'chip': 1250, 'diamond': 24, 'props': [{'id': 205, 'count': 3}, {'id': 201, 'count': 3}]},
    {'chip': 1300, 'diamond': 25, 'props': [{'id': 204, 'count': 2}, {'id': 203, 'count': 2}]},
    {'chip': 1350, 'diamond': 26, 'props': [{'id': 202, 'count': 2}, {'id': 201, 'count': 3}]},
    {'chip': 1400, 'diamond': 27, 'props': [{'id': 202, 'count': 2}, {'id': 201, 'count': 3}]},
    {'chip': 1450, 'diamond': 28, 'props': [{'id': 202, 'count': 2}, {'id': 201, 'count': 3}]},
    {'chip': 1500, 'diamond': 29, 'props': [{'id': 202, 'count': 2}, {'id': 201, 'count': 3}]},
    {'chip': 1550, 'diamond': 30, 'props': [{'id': 204, 'count': 3}, {'id': 203, 'count': 3}]},
])

add_game_config(2, 'vip.level', [20, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000])

add_game_config(2, 'vip.config', [
    {'pay': 20, 'desc': u'签到翻倍奖励'},
    {'pay': 200, 'desc': u'开启超级武器技能'},
    {'pay': 500, 'desc': u'开启狂暴技能'},
    {'pay': 1000, 'desc': u'充值额外返利10%', 'rebate': 0.1},
    {'pay': 2000, 'desc': u'开启寒冰陷阱技能', 'rebate': 0.1},
    {'pay': 5000, 'desc': u'充值额外返利20%', 'rebate': 0.2},
    {'pay': 10000, 'desc': u'提高击杀几率', 'rebate': 0.2, 'chip': 500000, 'stone': 5},
    {'pay': 20000, 'desc': u'提高击杀几率', 'rebate': 0.2, 'chip': 1000000, 'stone': 10},
    {'pay': 50000, 'desc': u'提高击杀几率', 'rebate': 0.2, 'chip': 2000000, 'stone': 20},
])
#抽奖配置
add_game_config(2, 'raffle.config', {
    'config': [
        {
            'id': 1,
            'name': u'普通抽奖',
            'limit': 0,
            'reward': [[0.001, {'coupon': 5}], [0.03, {'diamond': 10}], [0.05, {'diamond': 5}],
                       [0.2, {'chip': 600}], [0.3, {'chip': 300}], [0.419, {'chip': 100}]]
        },
        {
            'id': 2,
            'name': u'青铜抽奖',
            'limit': 20000,
            'reward': [[0.001, {'coupon': 15}], [0.03, {'diamond': 100}], [0.05, {'diamond': 50}],
                       [0.2, {'chip': 50000}], [0.3, {'chip': 24000}], [0.419, {'chip': 8000}]]
        },
        {
            'id': 3,
            'name': u'白银抽奖',
            'limit': 100000,
            'reward': [[0.001, {'coupon': 30}], [0.03, {'diamond': 200}], [0.04, {'diamond': 100}],
                       [0.2, {'chip': 250000}], [0.3, {'chip': 120000}], [0.419, {'chip': 40000}]]
        },
        {
            'id': 4,
            'name': u'黄金抽奖',
            'limit': 200000,
            'reward': [[0.0002, {'coupon': 70}], [0.03, {'diamond': 400}], [0.02, {'diamond': 200}],
                       [0.1008, {'chip': 500000}], [0.27, {'chip': 240000}], [0.579, {'chip': 80000}]]
        },
        {
            'id': 5,
            'name': u'白金抽奖',
            'limit': 400000,
            'reward': [[0.0002, {'coupon': 150}], [0.03, {'diamond': 800}], [0.04, {'diamond': 400}],
                       [0.0908, {'chip': 1000000}], [0.29, {'chip': 480000}], [0.619, {'chip': 160000}]]
        },
        {
            'id': 6,
            'name': u'至尊抽奖',
            'limit': 1200000,
            'reward': [[0.0002, {'coupon': 450}], [0.03, {'diamond': 2400}],
                       [0.04, {'diamond': 1200}],
                       [0.0808, {'chip': 3000000}], [0.295, {'chip': 1440000}], [0.649, {'chip': 480000}]]
        },
    ],
    'loop': [5, 5, 10]
})
#游戏技能
add_game_config(2, 'props.config', [
    {
        'id': 201,
        'diamond': 200,
        'count': 100,
        'price': 2,
        'present': {'pay': 200},
        'desc': u'看到大鱼别犹豫，立即使用锁定技能！要不就被别人抢走了'
    },
    {
        'id': 202,
        'diamond': 200,
        'count': 40,
        'price': 5,
        'present': {'pay': 200},
        'desc': u'什么！鱼要逃走了？赶快使用全屏冰冻，瞬间为你冰冻'
    },
    {
        'id': 203,
        'diamond': 200,
        'count': 10,
        'price': 20,
        'present': {'pay': 200},
        'use': {'vip': 3},
        'buy': {'vip': 3},
        'desc': u'使用狂暴技能，立即获得双倍击杀概率'
    },
    {
        'id': 204,
        'diamond': 200,
        'count': 1,
        'price': 200,
        'present': {'pay': 200},
        'use': {'vip': 2},
        'buy': {'vip': 2},
        'desc': u'发射一颗威力强大的超级武器，记得对准鱼多的地方扔哦！(对首领无效)'
    },
    {
        'id': 205,
        'diamond': 200,
        'count': 100,
        'price': 2,
        'present': {'pay': 200},
        'desc': u'快快使用传送门，传送出一只神秘奖金鱼吧'
    },
    {
        'id': 211,
        'count': 1,
        'content': {'chip': 150000},
        'present': {'pay': 200},
        'desc': u'使用后可获得150000金币!'
    },
    {
        'id': 212,
        'count': 1,
        'content': {'chip': 250000,
                    'props': [{'id': 220, 'dRate': 0.1, 'count': 1}]},
        'present': {'pay': 200},
        'desc': u'使用后可获得250000金币，有几率开出C级宠物蛋!'
    },
    {
        'id': 213,
        'count': 1,
        'content': {'chip': 500000,
                    'props': [{'id': 221, 'dRate': 0.05, 'count': 1}]},
        'present': {'pay': 200},
        'desc': u'使用后可获得500000金币，有几率开出B级宠物蛋!'
    },
    {
        'id': 214,
        'count': 1,
        'content': {'chip': 1000000,
                    'props': [{'id': 222, 'dRate': 0.02, 'count': 1}]},
        'present': {'pay': 200},
        'desc': u'使用后可获得1000000金币，有几率开出A级宠物蛋!'
    },
    {
        'id': 215,
        'diamond': 200,
        'count': 10,
        'price': 2,
        'present': {'pay': 200},
        'resolve': [2, 3],
        'desc': u'绿灵石是用于强化1000倍以上炮台的必备材料；使用1000倍（含）以上炮台击杀“奖金鱼”时，有一定几率掉落，击杀首领必掉落。'
    },
    {
        'id': 216,
        'diamond': 200,
        'count': 10,
        'price': 2,
        'present': {'pay': 200},
        'resolve': [2, 3],
        'desc': u'金刚石是用于强化1000倍以上炮台的必备材料；使用1000倍（含）以上炮台击杀“奖金鱼”时，有一定几率掉落，击杀首领必掉落。'
    },
    {
        'id': 217,
        'diamond': 200,
        'count': 10,
        'price': 2,
        'present': {'pay': 200},
        'resolve': [2, 3],
        'desc': u'紫晶石是用于强化1000倍以上炮台的必备材料；使用1000倍（含）以上炮台击杀“奖金鱼”时，有一定几率掉落，击杀首领必掉落。'
    },
    {
        'id': 218,
        'diamond': 200,
        'count': 10,
        'price': 2,
        'present': {'pay': 200},
        'resolve': [2, 3],
        'desc': u'血精石是用于强化1000倍以上炮台的必备材料；使用1000倍（含）以上炮台击杀“奖金鱼”时，有一定几率掉落，击杀首领必掉落。'
    },
    {
        'id': 219,
        'diamond': 200,
        'count': 10,
        'price': 2,
        'present': {'pay': 200},
        'desc': u'使用强化精华强化1000倍以上炮台，100%强化成功；强化精华可通过分解血精石、紫晶石、金刚石、绿灵石获得。'
    },
])
# 兑换商城
add_game_config(2, 'exchange.config', [
    {'type': 'diamond', 'desc': u'500钻石', 'cost': 300, 'count': 500},
    {'type': 'diamond', 'desc': u'1200钻石', 'cost': 600, 'count': 1200}
])

# html
if Global.run_mode == 1:
    __url_base = 'http://www.10000game.net'
elif Global.run_mode == 2:
    __url_base = 'http://test_server_url'
else:
    __url_base = 'http://192.168.1.21'
#页面交互
html_config = {
    'http_game': Global.http_game,
    'activity': __url_base + '/notice.html',
    'rank': __url_base + '/ranklist.html',
    'history': __url_base + '/history.html'
}
add_game_config(2, 'html.config', html_config)

add_game_config(2, 'sms.config', {
    'appId': 'aaf98f8953b303c10153c15b5f1231666',
    'accountSid': 'aaf98f894ecd7d6a014e1d3e17ee60b56',
    'accountToken': '0d28e7481a8d4d88b8c41b2e8340cae58',
    'serverIP': 'app.cloopen.com',
    'serverPort': '8883',
    'tempId': '76610',
    'softVersion': '2013-12-26'
})

# 概率加成
add_game_config(2, 'odds.addition.violent', 0.5)

add_game_config(2, 'odds.addition.pay', {
    'damping': 0.1,
    'total': 10,
    'addition': 2.5,
    'multi': 10000
})

add_game_config(2, 'odds.addition.egg', {
    'addition': 1,
    'max': 15000000,
    '213': 300000,
    '214': 600000
})

if Global.run_mode in (1, 2):
    add_game_config(2, 'cdkey.server.url', 'http://api2.10000game.net/api/changecode/changed.json')
else:
    add_game_config(2, 'cdkey.server.url', 'http://inner_server_url')
