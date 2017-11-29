#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-12-17

from account import FishAccount
from lemon.entity.rank import Rank
from framework.util.tool import Tool
from framework.context import Context
from framework.entity.const import Message
from framework.entity.msgpack import MsgPack


class FishRank(Rank):
    def get_ranks(self, uid, gid, mi):
        rank_name = mi.get_param('rank')
        if not rank_name:
            rank_name = ['chip', 'exp']
        elif isinstance(rank_name, (str, unicode)):
            rank_name = [rank_name]

        start = mi.get_param('start', 0)
        end = mi.get_param('end', 49)
        if start < 0 or end < start:
            return
        if end - start > 49:
            end = start + 49

        mo = MsgPack(Message.MSG_SYS_RANK_LIST | Message.ID_ACK)
        rank_list, mine = {}, {}
        if 'chip' in rank_name:
            _, rank_list['chip'] = self.get_chip_rank_list(uid, gid, start, end)
        if 'exp' in rank_name:
            _, rank_list['exp'] = self.get_exp_rank_list(uid, gid, start, end)

        mo.update_param(rank_list)
        if 'chip' in rank_list or 'exp' in rank_list:
            _info = self.__get_user_info(uid, gid)
            mine.update(_info)
        if mine:
            mo.set_param('mine', mine)
        return mo

    def get_chip_rank_list(self, uid, gid, start, end):
        """
        头像, vip等级, 昵称, 游戏等级, 金币
        """
        rank = None
        _list = self.get_rank_list(gid, 'chip', start, end)
        for i, item in enumerate(_list):
            _list[i] = item[2]
            if uid == item[0]:
                rank = i
        return rank, _list

    def get_exp_rank_list(self, uid, gid, start, end):
        """
        头像, vip等级, 昵称, 游戏等级, 经验值
        """
        rank = None
        _list = self.get_rank_list(gid, 'exp', start, end)
        for i, item in enumerate(_list):
            _list[i] = item[2]
            if uid == item[0]:
                rank = i
        return rank, _list

    def __get_user_info(self, uid, gid):
        game_attr = ['chip', 'exp']
        chip, exp = Context.Data.get_game_attrs(uid, gid, game_attr)
        chip = Tool.to_int(chip, 0)
        exp = Tool.to_int(exp, 0)
        user_attr = ['nick', 'avatar', 'sex']
        nick, avatar, sex = Context.Data.get_attrs(uid, user_attr)
        sex = Tool.to_int(sex, 0)
        level = FishAccount.get_vip_level(uid, gid)
        return {
            'uid': uid,
            'chip': chip,
            'exp': exp,
            'sex': sex,
            'nick': nick,
            'avatar': avatar,
            'vip': level
        }


FishRank = FishRank()
