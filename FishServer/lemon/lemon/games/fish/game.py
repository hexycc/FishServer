#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-23

from lemon.entity.game import Game


class FishGame(Game):
    def on_startup(self, gid):
        from builder import MapBuilder
        MapBuilder.load_config(gid)


FishGame = FishGame()
