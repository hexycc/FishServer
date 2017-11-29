#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-20

from framework.entity.const import FlagType
from lemon.games.fish import class_map as fish_class

classMap = {
    2: fish_class,
}


def init_game(server_type):
    _type = FlagType.trans_server_type(server_type)
    for gid, class_map in classMap.iteritems():
        for t in class_map:
            if t == _type:
                attr = getattr(class_map[t], 'on_startup', None)
                if attr:
                    attr(gid)
                break
