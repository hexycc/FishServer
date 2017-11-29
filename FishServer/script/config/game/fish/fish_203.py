#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-03-14

from framework.helper import *

fish_type_101 = {
    'type': 101,
    'point': 2,
    'odds': 0.33333,
    'wave': [0.55000, 0.16667],
    'name': u'鹧鸪',
    'reward': [
        [0.02000, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]],
    ]
}
fish_type_102 = {
    'type': 102,
    'point': 3,
    'odds': 0.22222,
    'wave': [0.34333, 0.12500],
    'name': u'麻雀',
    'reward': [
        [0.01900, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}
fish_type_103 = {
    'type': 103,
    'point': 4,
    'odds': 0.16777,
    'wave': [0.25700, 0.10000],
    'name': u'海鸥',
    'reward': [
        [0.01800, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}
fish_type_104 = {
    'type': 104,
    'point': 5,
    'odds': 0.13333,
    'wave': [0.20500, 0.08333],
    'name': u'八哥',
    'reward': [
        [0.01700, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}
fish_type_105 = {
    'type': 105,
    'point': 6,
    'odds': 0.11111,
    'wave': [0.16967, 0.07143],
    'name': u'鸽子',
    'reward': [
        [0.01600, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}
fish_type_106 = {
    'type': 106,
    'point': 7,
    'odds': 0.09524,
    'wave': [0.14486, 0.05556],
    'name': u'猫头鹰',
    'reward': [
        [0.01500, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}
fish_type_107 = {
    'type': 107,
    'point': 8,
    'odds': 0.08333,
    'wave': [0.12650, 0.05000],
    'name': u'画眉',
    'reward': [
        [0.01400, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}
fish_type_108 = {
    'type': 108,
    'point': 9,
    'odds': 0.07407,
    'wave': [0.11241, 0.04545],
    'name': u'白鹭',
    'reward': [
        [0.01300, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}
fish_type_109 = {
    'type': 109,
    'point': 10,
    'odds': 0.06667,
    'wave': [0.10120, 0.04167],
    'name': u'林雕',
    'reward': [
        [0.01200, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}
fish_type_110 = {
    'type': 110,
    'point': 12,
    'odds': 0.05556,
    'wave': [0.08423, 0.03571],
    'name': u'苍鹰',
    'reward': [
        [0.01100, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}
fish_type_111 = {
    'type': 111,
    'point': 15,
    'odds': 0.04444,
    'wave': [0.06717, 0.02941],
    'name': u'秃鹫',
    'reward': [
        [0.01000, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}
fish_type_112 = {
    'type': 112,
    'point': 18,
    'odds': 0.03704,
    'wave': [0.05656, 0.02500],
    'name': u'火烈鱼',
    'reward': [
        [0.00900, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}
fish_type_113 = {
    'type': 113,
    'point': 25,
    'odds': 0.02667,
    'wave': [0.04010, 0.01786],
    'name': u'孔雀',
    'reward': [
        [0.00800, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}
fish_type_114 = {
    'type': 114,
    'point': 20,
    'odds': 0.03333,
    'wave': [0.05020, 0.02273],
    'name': u'紫燕',
    'reward': [
        [0.00700, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}
fish_type_115 = {
    'type': 115,
    'point': 30,
    'odds': 0.02222,
    'wave': [0.03338, 0.01515],
    'name': u'大鹏',
    'reward': [
        [0.00600, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}
fish_type_116 = {
    'type': 116,
    'point': 35,
    'odds': 0.01950,
    'wave': [0.02860, 0.01316],
    'name': u'毕方',
    'reward': [
        [0.00500, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}
fish_type_117 = {
    'type': 117,
    'point': 40,
    'odds': 0.01667,
    'wave': [0.02600, 0.01163],
    'name': u'鬼车',
    'reward': [
        [0.00400, [
            {'props': [{'id': 202, 'count': 1}]},
            {'props': [{'id': 201, 'count': 1}]},
            {'diamond': 1},
            {'diamond': 1}
        ]]
    ]
}

fish_type_151 = {
    'type': 151,
    'point': [150, 180, 210, 240],
    'odds': 0.00417,
    'wave': [0.00427, 0.00274],
    'name': u'齐天大圣'
}
fish_type_152 = {
    'type': 152,
    'point': 0,
    'odds': 0.00417,
    'wave': [0.00427, 0.00274],
    'name': u'钻石宝箱',
    'reward': [
        [1, [{'diamond': 50}]]
    ]
}
fish_type_153 = {
    'type': 153,
    'point': [200, 240, 280, 300],
    'odds': 0.00417,
    'wave': [0.00427, 0.00274],
    'name': u'炸弹'
}
fish_type_161 = {
    'type': 161,
    'point': 40,
    'odds': 0.00417,
    'wave': [0.00427, 0.00274],
    'name': u'一网打尽'
}
fish_type_162 = {
    'type': 162,
    'point': 40,
    'odds': 0.00417,
    'wave': [0.00427, 0.00274],
    'name': u'一网打尽'
}
fish_type_163 = {
    'type': 163,
    'point': 40,
    'odds': 0.00417,
    'wave': [0.00427, 0.00274],
    'name': u'一网打尽'
}
fish_type_164 = {
    'type': 164,
    'point': 40,
    'odds': 0.00417,
    'wave': [0.00427, 0.00274],
    'name': u'一网打尽'
}
fish_type_165 = {
    'type': 165,
    'point': 40,
    'odds': 0.00417,
    'wave': [0.00427, 0.00274],
    'name': u'一网打尽'
}
fish_type_166 = {
    'type': 166,
    'point': 40,
    'odds': 0.00417,
    'wave': [0.00427, 0.00274],
    'name': u'一网打尽'
}
fish_type_167 = {
    'type': 167,
    'point': 40,
    'odds': 0.00417,
    'wave': [0.00427, 0.00274],
    'name': u'一网打尽'
}
fish_type_168 = {
    'type': 168,
    'point': 40,
    'odds': 0.00417,
    'wave': [0.00427, 0.00274],
    'name': u'一网打尽'
}

fish_type_176 = {
    'type': 176,
    'point': 50,
    'odds': 0.02005,
    'wave': [0.02200, 0.01360],
    'name': u'奖金鱼',
    'reward': [
        [0.15000, [
            {'props': [{'id': 215, 'count': 1}]},
            {'props': [{'id': 216, 'count': 1}]},
            {'props': [{'id': 217, 'count': 1}]},
            {'props': [{'id': 218, 'count': 1}]},
        ]]
    ]
}
fish_type_177 = {
    'type': 177,
    'point': 80,
    'odds': 0.01255,
    'wave': [0.01325, 0.00850],
    'name': u'奖金鱼',
    'reward': [
        [0.15000, [
            {'props': [{'id': 215, 'count': 1}]},
            {'props': [{'id': 216, 'count': 1}]},
            {'props': [{'id': 217, 'count': 1}]},
            {'props': [{'id': 218, 'count': 1}]},
        ]]
    ]
}
fish_type_178 = {
    'type': 178,
    'point': 100,
    'odds': 0.01005,
    'wave': [0.01050, 0.00680],
    'name': u'奖金鱼',
    'reward': [
        [0.15000, [
            {'props': [{'id': 215, 'count': 1}]},
            {'props': [{'id': 216, 'count': 1}]},
            {'props': [{'id': 217, 'count': 1}]},
            {'props': [{'id': 218, 'count': 1}]},
        ]]
    ]
}
fish_type_179 = {
    'type': 179,
    'point': 120,
    'odds': 0.00838,
    'wave': [0.00867, 0.00567],
    'name': u'奖金鱼',
    'reward': [
        [0.15000, [
            {'props': [{'id': 215, 'count': 1}]},
            {'props': [{'id': 216, 'count': 1}]},
            {'props': [{'id': 217, 'count': 1}]},
            {'props': [{'id': 218, 'count': 1}]},
        ]]
    ]
}
fish_type_180 = {
    'type': 180,
    'point': 150,
    'odds': 0.00672,
    'wave': [0.00683, 0.00453],
    'name': u'奖金鱼',
    'reward': [
        [0.15000, [
            {'props': [{'id': 215, 'count': 1}]},
            {'props': [{'id': 216, 'count': 1}]},
            {'props': [{'id': 217, 'count': 1}]},
            {'props': [{'id': 218, 'count': 1}]},
        ]]
    ]
}
fish_type_181 = {
    'type': 181,
    'point': 160,
    'odds': 0.00630,
    'wave': [0.00633, 0.00425],
    'name': u'奖金鱼',
    'reward': [
        [0.15000, [
            {'props': [{'id': 215, 'count': 1}]},
            {'props': [{'id': 216, 'count': 1}]},
            {'props': [{'id': 217, 'count': 1}]},
            {'props': [{'id': 218, 'count': 1}]},
        ]]
    ]
}
fish_type_182 = {
    'type': 182,
    'point': 200,
    'odds': 0.00505,
    'wave': [0.00510, 0.00340],
    'name': u'奖金鱼',
    'reward': [
        [0.15000, [
            {'props': [{'id': 215, 'count': 1}]},
            {'props': [{'id': 216, 'count': 1}]},
            {'props': [{'id': 217, 'count': 1}]},
            {'props': [{'id': 218, 'count': 1}]},
        ]]
    ]
}
fish_type_183 = {
    'type': 183,
    'point': 250,
    'odds': 0.00405,
    'wave': [0.00406, 0.00272],
    'name': u'奖金鱼',
    'reward': [
        [0.15000, [
            {'props': [{'id': 215, 'count': 1}]},
            {'props': [{'id': 216, 'count': 1}]},
            {'props': [{'id': 217, 'count': 1}]},
            {'props': [{'id': 218, 'count': 1}]},
        ]]
    ]
}

fish_type_201 = {
    'type': 201,
    'point': 120,
    'odds': 0.00833,
    'wave': [0.00843, 0.00407],
    'name': u'青鸾',
    'reward': [
        [1, [{'diamond': 10}]],
        [1, [
            {'props': [{'id': 215, 'count': 1}]},
            {'props': [{'id': 216, 'count': 1}]},
            {'props': [{'id': 217, 'count': 1}]},
            {'props': [{'id': 218, 'count': 1}]},
        ]]
    ]
}
fish_type_202 = {
    'type': 202,
    'point': 200,
    'odds': 0.00500,
    'wave': [0.00510, 0.00246],
    'name': u'重名鱼',
    'reward': [
        [1, [{'diamond': 10}]],
        [1, [
            {'props': [{'id': 215, 'count': 1}]},
            {'props': [{'id': 216, 'count': 1}]},
            {'props': [{'id': 217, 'count': 1}]},
            {'props': [{'id': 218, 'count': 1}]},
        ]]
    ]
}
fish_type_203 = {
    'type': 203,
    'point': 300,
    'odds': 0.00333,
    'wave': [0.00343, 0.00165],
    'name': u'百鸣鱼',
    'reward': [
        [1, [{'diamond': 10}]],
        [1, [
            {'props': [{'id': 215, 'count': 1}]},
            {'props': [{'id': 216, 'count': 1}]},
            {'props': [{'id': 217, 'count': 1}]},
            {'props': [{'id': 218, 'count': 1}]},
        ]]
    ]
}
fish_type_204 = {
    'type': 204,
    'point': 400,
    'odds': 0.00200,
    'wave': [0.00210, 0.00099],
    'name': u'三足金乌',
    'reward': [
        [1, [{'diamond': 10}]],
        [1, [
            {'props': [{'id': 215, 'count': 1}]},
            {'props': [{'id': 216, 'count': 1}]},
            {'props': [{'id': 217, 'count': 1}]},
            {'props': [{'id': 218, 'count': 1}]},
        ]]
    ]
}
fish_type_205 = {
    'type': 205,
    'point': 500,
    'odds': 0.00250,
    'wave': [0.00260, 0.00124],
    'name': u'凤凰',
    'reward': [
        [1, [{'diamond': 10}]],
        [1, [
            {'props': [{'id': 215, 'count': 1}]},
            {'props': [{'id': 216, 'count': 1}]},
            {'props': [{'id': 217, 'count': 1}]},
            {'props': [{'id': 218, 'count': 1}]},
        ]]
    ]
}
fish_type_206 = {
    'type': 206,
    'point': 600,
    'odds': 0.00167,
    'wave': [0.00177, 0.00083],
    'name': u'神龙',
    'reward': [
        [1, [{'diamond': 10}]],
        [1, [
            {'props': [{'id': 215, 'count': 1}]},
            {'props': [{'id': 216, 'count': 1}]},
            {'props': [{'id': 217, 'count': 1}]},
            {'props': [{'id': 218, 'count': 1}]},
        ]]
    ]
}

fish_type_301 = {
    'type': 301,
    'point': 463,
    'odds': 0.0005,
    'wave': [0.0005, 0.0005],
    'var': [1500000, 100000, 0.02],
    'name': u'红龙',
    'reward': [
        [1, [{'egg': [[213, 500], [212, 300], [211, 100]]}]],
        [0.0001, [{'props': [{'id': 223, 'count': 1}]}, ]]
    ]
}

fish_type_302 = {
    'type': 302,
    'point': 8,
    'odds': 0.02005,
    'wave': [0.02200, 0.01360],
    'name': u'小红龙'
}

fish_type_303 = {
    'type': 303,
    'point': 50,
    'odds': 0.02005,
    'wave': [0.02200, 0.01360],
    'name': u'红龙奖金鱼',
    'reward': [
        [0.15000, [
            {'props': [{'id': 215, 'count': 1}]},
            {'props': [{'id': 216, 'count': 1}]},
            {'props': [{'id': 217, 'count': 1}]},
            {'props': [{'id': 218, 'count': 1}]},
        ]]
    ]
}

add_game_config(2, 'fish.203.config', {
    'common': [fish_type_101, fish_type_102, fish_type_103, fish_type_104, fish_type_105,
               fish_type_106, fish_type_107, fish_type_108, fish_type_109, fish_type_110,
               fish_type_111, fish_type_112, fish_type_113, fish_type_114, fish_type_115,
               fish_type_116, fish_type_117],
    'special': [fish_type_151, fish_type_152, fish_type_153,
                fish_type_161, fish_type_162, fish_type_163, fish_type_164,
                fish_type_165, fish_type_166, fish_type_167, fish_type_168,
                fish_type_302],
    'bonus': [fish_type_176, fish_type_177, fish_type_178, fish_type_179, fish_type_180,
              fish_type_181, fish_type_182, fish_type_183, fish_type_303],
    'boss': [fish_type_201, fish_type_202, fish_type_203, fish_type_204, fish_type_205,
             fish_type_206, fish_type_301],
})
