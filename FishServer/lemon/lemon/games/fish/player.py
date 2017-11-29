#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-12-04

from const import Enum
from props import FishProps
from account import FishAccount
from lemon.entity.player import Player
from framework.util.tool import Time
from framework.context import Context


class FishPlayer(Player):
    def __init__(self, uid):
        super(FishPlayer, self).__init__(uid)
        self._props_info = None
        self.bullet_number = 0          # 子弹计数器
        self.barrel_angle = 0           # 炮筒角度
        self._barrel_level = 1          # 炮筒等级
        self.barrel_multiple = 1        # 炮筒倍数
        self.state = Enum.user_state_free
        self.identity = Enum.identity_type_unknown
        self.lock = {}
        self.violent = {}
        self.bullet_map = {}            # 记录子弹和倍数
        self.around_fish = [None] * 3   # 围绕的鱼
        self.attack_timer = None
        self.call_fish_timer = None
        self.offline_timer = None
        self.bounty_task = {}
        self.today_chip_pool = 0
        self.today_common_chip_pool = 0
        self.today_pay_total = 0
        self.today_fish_301 = 0
        self.chip_pool = 0
        self.blocked = None
        self.session_ver = '0.0.0'
        self.egg_addition_odds = 0

    def leave_table(self):
        super(FishPlayer, self).leave_table()
        self._props_info = None
        self.bullet_number = 0
        self.barrel_angle = 0
        self._barrel_level = 1
        self.barrel_multiple = 1
        self.state = Enum.user_state_free
        self.identity = Enum.identity_type_unknown
        self.lock.clear()
        self.violent.clear()
        self.bullet_map.clear()
        self.bounty_task.clear()
        self.around_fish = [None] * 3  # 围绕的鱼
        self.today_chip_pool = 0
        self.today_common_chip_pool = 0
        self.today_pay_total = 0
        self.today_fish_301 = 0
        self.chip_pool = 0
        self.blocked = None
        self.session_ver = '0.0.0'
        self.egg_addition_odds = 0
        if self.attack_timer:
            self.attack_timer.cancel()
            self.attack_timer = None

        if self.call_fish_timer:
            self.call_fish_timer.cancel()
            self.call_fish_timer = None

        if self.offline_timer:
            self.offline_timer.cancel()
            self.offline_timer = None

    def switch_scene(self):
        self.lock.clear()
        self.violent.clear()
        if self.attack_timer:
            self.attack_timer.cancel()
            self.attack_timer = None

        if self.call_fish_timer:
            self.call_fish_timer.cancel()
            self.call_fish_timer = None

    def get_free_around_loc(self):
        for i in (0, 1, 2):
            if self.around_fish[i] is None:
                return i

    def get_around_loc(self, fish_id):
        for i in (0, 1, 2):
            if self.around_fish[i] == fish_id:
                return i

    def set_around_loc(self, loc, fish_id):
        self.around_fish[loc] = fish_id

    def del_around_fish(self, loc):
        self.around_fish[loc] = None

    def clear_around_fish(self):
        self.around_fish = [None] * 3

    def get_all_around_fishs(self):
        l = []
        for i in (0, 1, 2):
            if self.around_fish[i]:
                l.append([i, self.around_fish[i]])
        return l

    def catch_bounty_fish(self, goal, fish_type, multi):
        if fish_type not in self.bounty_task:
            self.bounty_task[fish_type] = 1
        else:
            self.bounty_task[fish_type] += 1

        if 'count' not in self.bounty_task:
            self.bounty_task['count'] = 1
        else:
            self.bounty_task['count'] += 1

        self.bounty_task['ts'] = Time.current_ms()

        for _t, _cnt in goal.iteritems():
            if _cnt > self.bounty_task.get(_t, 0):
                return
        if multi not in self.bounty_task:
            self.bounty_task['multi'] = multi

    @property
    def props_info(self):
        return self._props_info

    @props_info.setter
    def props_info(self, props_list):
        self._props_info = dict(props_list)

    @property
    def props(self, pid):
        return self._props_info.get(pid, 0)

    @property
    def nick(self):
        return self.user_info['nick']

    @property
    def barrel_level(self):
        return self._barrel_level

    @barrel_level.setter
    def barrel_level(self, level):
        self._barrel_level = level
        self.barrel_multiple = FishAccount.trans_barrel_level(self.gid, level)

    @property
    def max_barrel_level(self):
        return self.game_info['barrel_level']

    @max_barrel_level.setter
    def max_barrel_level(self, level):
        if self.game_info['barrel_level'] != level:
            self.game_info['barrel_level'] = level
            Context.Data.set_game_attr(self.uid, self.gid, 'barrel_level', level)

    @property
    def max_barrel_multi(self):
        return FishAccount.trans_barrel_level(self.gid, self.game_info['barrel_level'])

    @property
    def barrel_skin(self):
        return self.game_info['barrel_skin']

    @barrel_skin.setter
    def barrel_skin(self, skin):
        if self.game_info['barrel_skin'] != skin:
            self.game_info['barrel_skin'] = skin
            Context.Data.set_game_attr(self.uid, self.gid, 'barrel_skin', skin)

    @property
    def chip(self):
        return self.game_info['chip']

    @chip.setter
    def chip(self, value):
        self.game_info['chip'] = value

    @property
    def exp(self):
        return self.game_info['exp']

    @exp.setter
    def exp(self, value):
        self.game_info['exp'] = value

    def in_locking(self, uptime):
        end = self.lock.get('end', 0)
        if end and end > uptime:
            return True

        self.lock.clear()
        return False

    def in_violent(self, uptime):
        end = self.violent.get('end', 0)
        if end and end > uptime:
            return True

        self.violent.clear()
        return False

    def get_pay_addition(self):
        conf = Context.Configure.get_game_item_json(self.gid, 'odds.addition.pay')
        if self.today_common_chip_pool > 0 or self.today_chip_pool > 0:
            if self.today_pay_total > 0:
                return conf['addition']
            else:
                return self.egg_addition_odds
        return None

    def get_red_dragon_addition(self):
        if self.today_pay_total > 0:
            if self.today_fish_301 < 10:
                total = self.today_pay_total / 600
                if self.today_fish_301 < total:
                    return 0.0002
        return 0

    def attenuation_red_dragon(self, odds):
        if self.today_fish_301:
            odds -= self.today_fish_301 * 0.00005
            if odds < 0.00005:
                odds = 0.00005
        return odds

    def incr_chip_pool(self, chip):
        if self.today_common_chip_pool > 0:
            self.today_common_chip_pool = Context.Daily.incr_daily_data(self.uid, self.gid, 'common.chip.pool', chip)
        elif self.today_chip_pool > 0:
            self.today_chip_pool = Context.Daily.incr_daily_data(self.uid, self.gid, 'chip.pool', chip)
        else:
            self.chip_pool = Context.Data.hincr_game(self.uid, self.gid, 'chip_pool', chip)

    def can_shot(self):
        return self.game_info['barrel_level'] >= self._barrel_level

    def is_pump(self, number):
        return number % 10 == 0

    def use_props(self, pid, roomtype):
        left = self._props_info.get(pid)
        if left:
            real, final = FishProps.incr_props(self.uid, self.gid, pid, -1, 'game.use', roomtype=roomtype)
            self._props_info[pid] = final
            if real == -1:
                return True, final
        self._props_info[pid] = 0
        return False, 0

    def buy_props(self, pid):
        if self.game_info['diamond'] > 0:
            conf = FishProps.get_config_by_id(self.gid, pid)
            price = conf['price']
            if self.game_info['diamond'] >= price:
                real, final = Context.UserAttr.incr_diamond(self.uid, self.gid, -price, 'table.buy.%d' % pid)
                self.game_info['diamond'] = final
                if real == -price:
                    return final
        return None

    def incr_chip(self, delta, event, **kwargs):
        real, final = Context.UserAttr.incr_chip(self.uid, self.gid, delta, event, **kwargs)
        self.game_info['chip'] = final
        return real, final

    def incr_diamond(self, delta, event, **kwargs):
        real, final = Context.UserAttr.incr_diamond(self.uid, self.gid, delta, event, **kwargs)
        self.game_info['diamond'] = final
        return real, final

    def incr_coupon(self, delta, event, **kwargs):
        real, final = Context.UserAttr.incr_coupon(self.uid, self.gid, delta, event, **kwargs)
        self.game_info['coupon'] = final
        return real, final

    def issue_rewards(self, rewards, event, **kwargs):
        result = FishProps.issue_rewards(self.uid, self.gid, rewards, event, **kwargs)
        if result:
            if 'chip' in result:
                self.game_info['chip'] = result['chip']
            if 'coupon' in result:
                self.game_info['coupon'] = result['coupon']
            if 'diamond' in result:
                self.game_info['diamond'] = result['diamond']
            if 'props' in result:
                props = self._props_info
                for one in result['props']:
                    if one['id'] in props:
                        props[one['id']] += one['count']
                    else:
                        props[one['id']] = one['count']
        return result

    def check_bankrupt(self, leave=False):
        bankrupt = False
        if leave:
            if self.game_info['chip'] < 1:
                bankrupt = True
        else:
            if not self.bullet_map and self.game_info['chip'] < 1:
                bankrupt = True
        if bankrupt:
            chip = Context.UserAttr.get_chip(self.uid, self.gid)
            if chip > 0:
                self.game_info['chip'] = chip
                bankrupt = False
        return bankrupt
