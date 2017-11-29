#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-03-14

from lemon.entity.props import Props
from framework.context import Context


class FishProps(Props):
    PROP_LOCK_FISH = 201        # 锁定
    PROP_FREEZE = 202           # 冰冻
    PROP_VIOLENT = 203          # 狂暴
    PROP_SUPER_WEAPON = 204     # 超级武器
    PROP_PORTAL = 205           # 传送门
    PROP_EGG_BRONZE = 211       # 铜蛋
    PROP_EGG_SILVER = 212       # 银蛋
    PROP_EGG_GOLD = 213         # 金蛋
    PROP_EGG_COLOR = 214        # 彩蛋
    GREEN_STONE = 215           # 绿灵石
    YELLOW_STONE = 216          # 血精石
    VIOLET_STONE = 217          # 金刚石
    RED_STONE = 218             # 紫晶石
    GEM = 219                   # 强化精华

    def check_props(self, pid):
        return pid in (201, 202, 203, 204, 205, 211, 212, 213, 214, 215, 216,
                       217, 218, 219)

    def get_props_config(self, gid):
        return Context.Configure.get_game_item_json(gid, 'props.config')

    def get_config_by_id(self, gid, pid):
        conf = Context.Configure.get_game_item_json(gid, 'props.config')
        for item in conf:
            if item['id'] == pid:
                return item

    def get_props_list(self, uid, gid, pids=None):
        if pids is None:
            pids = [201, 202, 203, 204, 205, 211, 212, 213, 214, 215, 216,
                    217, 218, 219]
        key = 'props:%d:%d' % (gid, uid)
        kvs = Context.RedisCluster.hash_mget_as_dict(uid, key, *pids)
        props_list = []
        for k, v in kvs.iteritems():
            if int(v) > 0:
                props_list.append([int(k), int(v)])
        return props_list

    def get_egg_count(self, uid, gid):
        key = 'props:%d:%d' % (gid, uid)
        kvs = Context.RedisCluster.hash_mget_as_dict(uid, key, 211, 212, 213, 214)
        count = 0
        for k, v in kvs.iteritems():
            if int(v) > 0:
                count += int(v)
        return count

    def get_props_desc(self, pid):
        if pid == self.PROP_LOCK_FISH:
            return u'锁定'
        elif pid == self.PROP_FREEZE:
            return u'冰冻'
        elif pid == self.PROP_VIOLENT:
            return u'狂暴'
        elif pid == self.PROP_SUPER_WEAPON:
            return u'超级武器'
        elif pid == self.PROP_PORTAL:
            return u'传送门'
        elif pid == self.PROP_EGG_BRONZE:
            return u'铜蛋'
        elif pid == self.PROP_EGG_SILVER:
            return u'银蛋'
        elif pid == self.PROP_EGG_GOLD:
            return u'金蛋'
        elif pid == self.PROP_EGG_COLOR:
            return u'彩蛋'
        elif pid == self.GREEN_STONE:
            return u'绿灵石'
        elif pid == self.RED_STONE:
            return u'血精石'
        elif pid == self.YELLOW_STONE:
            return u'金刚石'
        elif pid == self.VIOLET_STONE:
            return u'紫晶石'
        elif pid == self.GEM:
            return u'强化精华'

    def convert_reward(self, rewards_info):
        result = {}
        if 'chip' in rewards_info:
            result['c'] = rewards_info['chip']
        if 'diamond' in rewards_info:
            result['d'] = rewards_info['diamond']
        if 'fake_chip' in rewards_info:
            result['f'] = rewards_info['fake_chip']
        if 'coupon' in rewards_info:
            result['o'] = rewards_info['coupon']
        if 'props' in rewards_info:
            props = []
            for one in rewards_info['props']:
                props.append([one['id'], one['count']])
            if props:
                result['p'] = props
        if 'reward' in rewards_info:
            rw = self.convert_reward(rewards_info['reward'])
            if rw:
                result['w'] = rw
        return result

    def convert_pid_count(self, reward):
        if 'chip' in reward:
            return FishProps.PROP_CHIP, reward['chip']
        elif 'diamond' in reward:
            return FishProps.PROP_DIAMOND, reward['diamond']
        elif 'coupon' in reward:
            return FishProps.PROP_COUPON, reward['coupon']
        elif 'rmb' in reward:
            return FishProps.PROP_RMB, reward['rmb']
        elif 'props' in reward:
            for one in reward['props']:
                return one['id'], one['count']
        return None, None


FishProps = FishProps()
