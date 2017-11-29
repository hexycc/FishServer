#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-23

from lemon.games.fish.quick import FishQuick
from lemon.games.fish.game import FishGame
from lemon.games.fish.entity import FishEntity
from lemon.games.fish.account import FishAccount
from lemon.games.fish.registry import FishRegistry
from lemon.games.fish.http import FishHttp
from lemon.games.fish.shell import FishShell

class_map = {
    'quick': FishQuick,
    'game': FishGame,
    'registry': FishRegistry,
    'entity': FishEntity,
    'account': FishAccount,
    'http': FishHttp,
    'shell': FishShell,
}
