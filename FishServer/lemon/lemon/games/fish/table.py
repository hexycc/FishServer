#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-26

import random
from const import Enum
from const import Message
from rank import FishRank
from props import FishProps
from builder import MapBuilder
from account import FishAccount
from registry import FishRegistry
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Tool
from lemon.entity.table import Table
from framework.entity.msgpack import MsgPack
from lemon.entity.gametimer import GameTimer


class FishTable(Table):
    MAX_PLAYER_CNT = 4
    pool_reward_map = {}                # 产出的金币
    pool_shot_map = {}                  # 投入的金币
    pool_pump_map = {}                  # 抽水
    red_pool_reward_map = {}            # 红龙产出的金币
    red_pool_shot_map = {}              # 红龙投入的金币
    red_pool_pump_map = {}              # 红龙抽水
    official_div_base_map = {}          # 分母平衡值
    official_macro_control_map = {}     # 宏观调节值

    def __init__(self, gid, tid):
        super(FishTable, self).__init__(gid, tid)
        self.players = [None] * self.MAX_PLAYER_CNT
        self.fish_config = {}
        self.super_weapon_config = {}   # 超级武器配置
        self.switch_timer = GameTimer()
        self.delta_timer = GameTimer()
        self.red_dragon_timer = GameTimer()
        self.red_dragon_task_state = Enum.task_state_free
        # self.red_dragon_cost = 0
        self.bounty_timer = GameTimer()
        self.bounty_task = {}
        self.bounty_task_state = Enum.task_state_free
        self.lasted_freeze = {}
        self.total_freeze = 0
        self.map = None
        self.special_fishs = {}         # 暂存的等待report的鱼, type:uid

    def reset_param(self, empty=True):
        self.switch_timer.cancel()
        self.delta_timer.cancel()
        if self.red_dragon_task_state == Enum.task_state_clear:
            self.red_dragon_task_state = Enum.task_state_free
        elif self.red_dragon_task_state != Enum.task_state_free:
            self.red_dragon_task_state = Enum.task_state_free
            self.red_dragon_timer.cancel()
        self.bounty_timer.cancel()
        self.bounty_task = {}
        self.bounty_task_state = Enum.task_state_free
        self.lasted_freeze = {}
        self.total_freeze = 0
        self.map = None
        self.special_fishs = {}

    def fetch_table_info(self):
        key = 'table:%d:%d' % (self.gid, self.tid)
        attrs = ['room_type', 'play_mode', 'seat0', 'seat1', 'seat2', 'seat3']
        kvs = Context.RedisCache.hash_mget_as_dict(key, *attrs)
        if len(kvs) != len(attrs):
            self._error('miss field', kvs)
            return False
        self.table_info = dict([(k, int(v)) for k, v in kvs.iteritems()])
        for i in range(self.MAX_PLAYER_CNT):
            k = 'seat' + str(i)
            v = self.table_info[k]
            if v > 0:
                self.table_info[v] = i

        room_type = self.table_info['room_type']
        config = Context.Configure.get_room_config(self.gid, room_type)
        if not config:
            self._error('miss room config')
            return False

        room_config = Context.copy_json_obj(config)

        violent_addition = Context.Configure.get_game_item_float(self.gid, 'odds.addition.violent', 0)
        room_config['violent_addition'] = violent_addition
        pay_addition = Context.Configure.get_game_item_json(self.gid, 'odds.addition.pay', None)
        room_config['pay_addition'] = pay_addition

        key = 'game.%d.info.hash' % self.gid
        fileds = ['official.div.base.%d' % room_type, 'official.macro.control.%d' % room_type]
        div_base, macro_control = Context.RedisMix.hash_mget(key, *fileds)

        config = Context.Configure.get_game_item_json(self.gid, 'fish.%d.config' % room_type)
        if not config:
            self._error('miss fish config')
            return False

        fish_config = {'map': {}}
        for k, fishs in config.iteritems():
            types = set()
            for fish in fishs:
                fish['class'] = k
                fish_config['map'][fish['type']] = fish
                types.add(fish['type'])
            fish_config[k] = list(types)

        config = Context.Configure.get_game_item_json(self.gid, 'super.weapon.%d.config' % room_type)
        if not config:
            self._error('miss super weapon config')
            return False

        if div_base:
            self.official_div_base_map[room_type] = int(div_base)
        if macro_control:
            self.official_macro_control_map[room_type] = int(macro_control)

        self.fish_config = fish_config
        self.room_config = room_config
        self.super_weapon_config = config
        return True

    def player_leave(self, uid):
        if uid in self.all_user:
            player = self.all_user[uid]
            self.update_gamedata(player)
            del self.all_user[uid]
            if player.sid is not None:
                self.players[player.sid] = None

            self.remove_player(uid)
            self._check_bankrupt(player, True)
            player.leave_table()

        if not self.all_user:
            self._info('table empty, recycle it')
            self.reset_param(True)
            self.set_recycle_flag()
            self.red_dragon_timer.cancel()
            self.red_dragon_task_state = Enum.task_state_free

    def update_gamedata(self, player):
        try:
            attrs = {
                'uid': player.uid,
                'avatar': player.user_info['avatar'],
                'sex': player.user_info['sex'],
                'nick': player.user_info['nick'],
                'vip': player.game_info['vip']['level'],
                'chip': player.chip,
                'exp': player.exp,
            }
            data = Context.json_dumps(attrs)
            FishRank.add(player.uid, self.gid, 'chip', player.chip, data)
            FishRank.add(player.uid, self.gid, 'exp', player.exp, data)
            egg = FishProps.get_egg_count(player.uid, self.gid)
            if egg:
                attrs['egg'] = egg
                FishRank.add(player.uid, self.gid, 'egg', egg, Context.json_dumps(attrs))
        except Exception, e:
            Context.Log.exception(player.uid)

    def __init_map_info(self, next_img=None):
        if not self.map:
            self.map = MapBuilder(self.room_type)
            duration, _, _ = self.map.new_map(next_img)
            self.set_timer('switch', self.map.total_ts + 0.5)
            self.set_timer('delta', duration - 6)
            for player in self.players:
                if player:
                    player.switch_scene()
            if self.play_mode == Enum.play_mode_task:
                if 'red_dragon' in self.room_config:
                    if not self.red_dragon_timer.IsActive():
                        self.red_dragon_task_state = Enum.task_state_free
                        self.set_timer('red_dragon', 45*60)

    def delta_update(self):
        uptime = self.real_uptime()
        if self.__map_as_tide(uptime):
            return 0
        if self.__map_as_bounty(uptime):
            return 0
        self.__map_as_delta(uptime)
        return 0

    def __map_as_tide(self, uptime):
        info = self.map.get_tide_map()
        if info:
            duration, ev_list, tide = info
            if self.map.has_more_map():
                self.set_timer('delta', duration)
            mo = MsgPack(Message.FISH_MSG_DELTA_SCENE | Message.ID_NTF)
            mo.set_param('tide', tide)
            mo.set_param('events', ev_list)
            mo.set_param('uptime', uptime)
            self.table_broadcast(mo)
            return True

    def __map_as_bounty(self, uptime):
        if self.play_mode != Enum.play_mode_task:
            return False

        count = 0
        for p in self.players:
            if p and p.state == Enum.user_state_playing:
                count += 1
        if count < 4:
            self._info('no enough player, bounty task pass', count)
            return

        info = self.map.get_bounty_map()
        if info:
            duration, ev_list, bounty = info
            start, show, _ev_list, fishs = self.map.delta_map()
            self.set_timer('delta', show)

            self.__cache_bounty_task(bounty)
            self.bounty_task_state = Enum.task_state_pre
            rel_uptime, rea_uptime, left = self.relative_time()
            # self.switch_timer.cancel()
            tm = start * 100 - rel_uptime + left
            self.set_timer('bounty_start', tm / 1000.0, show=duration)

            ev_list.extend(_ev_list)
            mo = MsgPack(Message.FISH_MSG_DELTA_SCENE | Message.ID_NTF)
            mo.set_param('bounty', bounty)
            mo.set_param('events', ev_list)
            if fishs:
                mo.set_param('fishs', fishs)
            mo.set_param('uptime', uptime)
            self.table_broadcast(mo)
            return True

    def __map_as_delta(self, uptime):
        start, duration, ev_list, fishs = self.map.delta_map()
        if self.map.has_more_map():
            self.set_timer('delta', duration)

        mo = MsgPack(Message.FISH_MSG_DELTA_SCENE | Message.ID_NTF)
        if fishs:
            mo.set_param('fishs', fishs)
        if ev_list:
            mo.set_param('events', ev_list)
        mo.set_param('uptime', uptime)
        self.table_broadcast(mo)
        return True

    def __cache_bounty_task(self, bounty):
        info = {}
        for _t, _cnt in bounty['info']:
            info[_t] = _cnt
        self.bounty_task = info

    def set_timer(self, action, tm, **kwargs):
        param = kwargs
        param['action'] = action
        param['gameId'] = self.gid
        param['tableId'] = self.tid

        self._info(action, tm, param)
        if action == 'delta':
            self.delta_timer.cancel()
            self.delta_timer.setTimeout(tm, param)
        elif action == 'switch':
            self.switch_timer.cancel()
            self.switch_timer.setTimeout(tm, param)
        elif action == 'red_dragon':
            self.red_dragon_timer.cancel()
            self.red_dragon_timer.setTimeout(tm, param)
        elif action == 'red_dragon_start':
            self.red_dragon_timer.cancel()
            self.red_dragon_timer.setTimeout(tm, param)
        elif action == 'red_dragon_end':
            self.red_dragon_timer.cancel()
            self.red_dragon_timer.setTimeout(tm, param)
        elif action == 'bounty_start':
            self.bounty_timer.cancel()
            self.bounty_timer.setTimeout(tm, param)
        elif action == 'bounty_end':
            self.bounty_timer.cancel()
            self.bounty_timer.setTimeout(tm, param)
        elif action == 'call_fish':
            uid = kwargs['userId']
            player = self.all_user.get(uid)
            if player:
                if player.call_fish_timer:
                    player.call_fish_timer.cancel()
                else:
                    player.call_fish_timer = GameTimer()
                player.call_fish_timer.setTimeout(tm, param)
        elif action == 'attack':
            uid = kwargs['userId']
            player = self.all_user.get(uid)
            if player:
                if player.attack_timer:
                    player.attack_timer.cancel()
                else:
                    player.attack_timer = GameTimer()
                player.attack_timer.setTimeout(tm, param)
        elif action == 'offline':
            uid = kwargs['userId']
            player = self.all_user.get(uid)
            if player:
                if player.offline_timer:
                    player.offline_timer.cancel()
                else:
                    player.offline_timer = GameTimer()
                player.offline_timer.setTimeout(tm, param)

        return param

    def real_uptime(self):
        return Time.current_ms() - self.map.start_ms

    def relative_time(self):
        uptime = self.real_uptime()
        self.__check_freeze(uptime)
        total = self.total_freeze
        left_ms = 0
        if self.lasted_freeze:
            left_ms = self.lasted_freeze['end'] - uptime
            total += uptime - self.lasted_freeze['start']

        return uptime - total, uptime, left_ms

    def onTimer(self, cmd, gid, msg):
        # todo: sometime maybe can not cancel
        self._info('-------------', msg)
        action = msg.get_param('action')
        if action == 'delta':
            self.delta_update()
        elif action == 'switch':
            self.delta_timer.cancel()
            next_img = self.map.next_img
            self.reset_param(False)
            self.__init_map_info(next_img)
            self.notify_next_scene()
        elif action == 'offline':
            self.__handle_user_offline(msg)
        elif action == 'red_dragon':
            self.__handle_red_dragon()
        elif action == 'call_fish':
            self.__handle_call_fish(msg)
        elif action == 'attack':
            self.__handle_attack(msg)
        elif action == 'red_dragon_start':
            self.__handle_task_start(msg)
        elif action == 'red_dragon_end':
            self.__handle_task_end(msg)
        elif action == 'bounty_start':
            self.__handle_task_start(msg)
        elif action == 'bounty_end':
            self.__handle_task_end(msg)

    def __handle_user_offline(self, msg):
        uid = msg.get_param('userId')
        self._info(uid, 'offline timer begin')
        player = self.all_user.get(uid)
        if player.offline_timer:
            player.offline_timer.cancel()
            player.offline_timer = None
            if player.state == Enum.user_state_offline:
                self.player_leave(uid)

                Context.Online.incr_online(self.gid, self.room_type, False)
        self._info(uid, 'offline timer end')

    def __handle_call_fish(self, msg):
        uid = msg.get_param('userId')
        self._info(uid, 'call fish timer begin')
        player = self.all_user.get(uid)
        if player:
            if player.call_fish_timer:
                player.call_fish_timer = None
                if player.state == Enum.user_state_playing:
                    is_first = msg.get_param('first', False)
                    self.__make_round_fish(player, is_first)

                if player.attack_timer is None:
                    self.set_timer('attack', 1, userId=uid)

    def __make_round_fish(self, player, first=False):
        if first:
            while True:
                new_loc = player.get_free_around_loc()
                if new_loc is None:
                    break
                fish = self.map.make_little_red_dragon()
                mo = MsgPack(Message.FISH_MSG_CALL_FISH | Message.ID_NTF)
                mo.set_param('u', player.uid)
                mo.set_param('fish', fish)
                mo.set_param('loc', new_loc)
                self.table_broadcast(mo)
                player.set_around_loc(new_loc, fish['i'])
        else:
            new_loc = player.get_free_around_loc()
            if new_loc is not None:
                fish = self.map.make_little_red_dragon()
                mo = MsgPack(Message.FISH_MSG_CALL_FISH | Message.ID_NTF)
                mo.set_param('u', player.uid)
                mo.set_param('fish', fish)
                mo.set_param('loc', new_loc)
                self.table_broadcast(mo)
                player.set_around_loc(new_loc, fish['i'])
                new_loc = player.get_free_around_loc()
                if new_loc is not None:
                    self.set_timer('call_fish', 5, userId=player.uid)

    def __handle_attack(self, msg):
        uid = msg.get_param('userId')
        pre_loc = msg.get_param('loc', 0)
        self._info(uid, 'attack timer begin')
        player = self.all_user.get(uid)
        if player:
            if player.state == Enum.user_state_playing:
                for i in (0, 1, 2):
                    loc = (pre_loc + i + 1) % 3
                    fish = player.around_fish[loc]
                    if fish:
                        fish_type = self.map.fish_type(fish)
                        if fish_type == 302:
                            break
                else:
                    player.attack_timer = None
                    self._info('no loc found, stop attack timer')
                    return

                self.set_timer('attack', 1, userId=uid, loc=loc)
                mo = MsgPack(Message.FISH_MSG_FISH_ATTACK | Message.ID_NTF)
                mo.set_param('u', uid)
                mo.set_param('i', fish)
                valid = random.randint(0, 10000)
                if valid < 500:
                    real, final = player.incr_chip(-20000, 'attack')
                    if real == -20000:
                        del self.map.fish_map[fish]
                        new_fish = self.map.make_red_dragon_bonus()
                        player.set_around_loc(loc, new_fish['i'])
                        mo.set_param('c', final)
                        mo.set_param('t', -real)
                        mo.set_param('fish', new_fish)
                        mo.set_param('loc', loc)

                self.table_broadcast(mo)

    def __handle_task_start(self, msg):
        show = msg.get_param('show')
        if self.red_dragon_task_state != Enum.task_state_free:
            self.set_timer('red_dragon_end', show)
            for player in self.players:
                if player and player.state == Enum.user_state_playing:
                    self.set_timer('call_fish', 1, userId=player.uid, first=True)
            self.red_dragon_task_state = Enum.task_state_ing
        if self.bounty_task_state != Enum.task_state_free:
            self.set_timer('bounty_end', show)
            self.bounty_task_state = Enum.task_state_ing

    def __handle_task_end(self, msg):
        if self.red_dragon_task_state == Enum.task_state_ing:
            mo = MsgPack(Message.FISH_MSG_RED_DRAGON_END | Message.ID_NTF)
            mo.set_param('fail', 1)
            back = []
            for p in self.players:
                if p:
                    count = 0
                    for fish in p.around_fish:
                        fish_type = self.map.fish_type(fish)
                        if fish_type == 303:
                            count += 1
                    if count > 0:
                        real, final = p.incr_chip(count * 20000, 'return')
                        back.append({'u': p.uid, 't': real, 'c': final})

            if back:
                mo.set_param('return', back)
            self.table_broadcast(mo)
            self.__clear_task(True)
            # clear map
            self.map.clear_map()
            self.set_timer('switch', 5)
        elif self.bounty_task_state == Enum.task_state_ing:
            # self.delta_timer.cancel()
            mo = MsgPack(Message.FISH_MSG_BOUNTY_END | Message.ID_NTF)
            mo.set_param('fail', 1)
            self.table_broadcast(mo)
            self.__clear_task(False)
            # clear map
            # self.map.clear_map()
            # self.set_timer('switch', 5)
            # clear event
            self.map.clear_bounty_event()
            self.bounty_task_state = Enum.task_state_free

    def __random_task_reward(self, multi):
        which = random.randint(1, 3)
        if which == 1:
            return {'chip': multi * 100}
        elif which == 2:
            diamond = int(multi * 5 / 100)
            if diamond > 50:
                diamond = 50
            return {'diamond': diamond}
        else:
            return {'props': [{'id': 204, 'count': 1}]}

    def __clear_task(self, red_dragon=True):
        if red_dragon:
            if self.red_dragon_task_state != Enum.task_state_clear:
                self.red_dragon_task_state = Enum.task_state_clear
                # self.red_dragon_cost = 0
                self.red_dragon_timer.cancel()
                for p in self.players:
                    if p:
                        if p.call_fish_timer:
                            p.call_fish_timer.cancel()
                            p.call_fish_timer = None
                        if p.attack_timer:
                            p.attack_timer.cancel()
                            p.attack_timer = None
                        p.clear_around_fish()
        else:
            if self.bounty_task_state != Enum.task_state_clear:
                self.bounty_task_state = Enum.task_state_clear
                self.bounty_timer.cancel()
                self.bounty_task.clear()
                for p in self.players:
                    if p:
                        p.bounty_task.clear()

    def __handle_red_dragon(self):
        if self.bounty_task_state != Enum.task_state_free:
            self.set_timer('red_dragon', 45*60)
            return 0

        count = 0
        for p in self.players:
            if p and p.state == Enum.user_state_playing:
                count += 1
        if count < 2:
            self._info('no enough player, red dragon pass', count)
            self.set_timer('red_dragon', 45*60)
            return 0

        # self.red_dragon_cost = 0
        self.red_dragon_task_state = Enum.task_state_pre
        start, show, ev_list, fishs = self.map.make_red_dragon()
        rel_uptime, rea_uptime, left = self.relative_time()
        self.delta_timer.cancel()
        self.switch_timer.cancel()
        tm = start * 100 - rel_uptime + left
        self.set_timer('red_dragon_start', tm / 1000.0, show=show)

        mo = MsgPack(Message.FISH_MSG_DELTA_SCENE | Message.ID_NTF)
        if fishs:
            mo.set_param('fishs', fishs)
        if ev_list:
            mo.set_param('events', ev_list)
        mo.set_param('uptime', rea_uptime)
        self.table_broadcast(mo)
        return 0

    @property
    def play_mode(self):
        return self.table_info['play_mode']

    @property
    def div_base(self):
        return self.official_div_base_map.get(self.room_type, 1000000)

    @property
    def macro_control(self):
        t = self.official_macro_control_map.get(self.room_type, 0)
        return t + 0.0

    @property
    def pool_shot(self):
        return self.pool_shot_map.get(self.room_type)

    @property
    def pool_reward(self):
        return self.pool_reward_map.get(self.room_type)

    @property
    def pool_pump(self):
        return self.pool_pump_map.get(self.room_type, 0)

    @property
    def violent_addition(self):
        return self.room_config['violent_addition']

    @property
    def pay_addition(self):
        return self.room_config['pay_addition']

    def on_join(self, uid):
        self._info(uid, 'req to join')
        if uid in self.all_user:
            player = self.all_user[uid]
            if player.state == Enum.user_state_offline:
                player.state = Enum.user_state_free
            self._info('the user is already here, maybe reconnect')
            return 0

        player = FishRegistry.get_player(uid)
        if not player:
            self._warn('not found player', uid)
            return Enum.join_table_failed_unknown

        if not self.fetch_table_info():
            return Enum.join_table_failed_unknown

        if not self.is_join_legal(uid):
            self._warn('player is not distributed here')
            return Enum.join_table_failed_unknown

        user_info = FishAccount.get_user_info(uid, self.gid)
        _, game_info = FishAccount.get_game_info(uid, self.gid)
        chip_min = self.room_config.get('chip_min', -1)
        if chip_min != -1 and chip_min > game_info['chip']:
            self._warn('%d chip %d < %d' % (uid, game_info['chip'], chip_min))
            return Enum.join_table_failed_limit_min

        chip_max = self.room_config.get('chip_max', -1)
        if chip_max != -1 and chip_max < game_info['chip']:
            self._warn('%d chip %d > %d' % (uid, game_info['chip'], chip_max))
            return Enum.join_table_failed_limit_max

        props_list = FishProps.get_props_list(uid, self.gid)

        player.gid = self.gid
        player.user_info = user_info
        player.game_info = game_info
        player.props_info = props_list
        player.identity = Enum.identity_type_player
        player.state = Enum.user_state_free

        fileds = ['chip.pool', 'common.chip.pool', 'pay_total', 'fish.301', 'egg.chip.pool']
        values = Context.Daily.get_daily_data(uid, self.gid, *fileds)
        kvs = Tool.make_dict(fileds, values)
        if kvs['pay_total']:
            player.today_pay_total = int(kvs['pay_total'])
        if kvs['chip.pool']:
            player.today_chip_pool = int(kvs['chip.pool'])
        if kvs['common.chip.pool']:
            player.today_common_chip_pool = int(kvs['common.chip.pool'])

        chip_pool = Context.Data.get_game_attr_int(uid, self.gid, 'chip_pool', 0)
        if chip_pool:
            player.chip_pool = chip_pool

        if kvs['fish.301']:
            player.today_fish_301 = int(kvs['fish.301'])
        if kvs['egg.chip.pool']:
            egg_addition_conf = Context.Configure.get_game_item_json(self.gid, 'odds.addition.egg')
            player.egg_addition_odds = egg_addition_conf['addition']

        blocked = Context.Data.get_game_attr(uid, self.gid, 'block')
        if blocked:
            player.blocked = float(blocked)
        player.session_ver = Context.Data.get_game_attr(uid, self.gid, 'session_ver')

        if self.room_config['level_max1'] > player.max_barrel_level:
            player.barrel_level = player.max_barrel_level
        else:
            player.barrel_level = self.room_config['level_max1']
        self.all_user[uid] = player

        Context.Online.incr_online(self.gid, self.room_type, True)
        self._info(uid, 'join success')
        return 0

    def on_sit_down(self, uid, sid):
        self._info(uid, 'req to sit', sid)
        if sid < 0 or sid >= self.MAX_PLAYER_CNT:
            self._error(uid, 'error seat id', sid)
            return Enum.sit_down_failed_error_seat_id

        if uid not in self.all_user:
            self._warn(uid, 'not join table')
            return Enum.sit_down_failed_error_not_join

        player = self.all_user[uid]
        if player.identity != Enum.identity_type_player:
            self._warn(uid, 'error identity', player.identity)
            return Enum.sit_down_failed_error_identity

        if player.sid == sid:
            player.state = Enum.user_state_playing
            if self.red_dragon_task_state == Enum.task_state_ing:
                self.set_timer('call_fish', 5, userId=uid)
                self.set_timer('attack', 1, userId=uid)
            self._info(uid, 'already sit here, maybe reconnect', sid)
            return 0

        if self.players[sid]:
            self._warn(self.players[sid].uid, 'is already here', sid)
            return Enum.sit_down_failed_other_here

        if uid not in self.table_info or self.table_info[uid] != sid:
            self._warn(uid, 'is not assigned to here', sid)
            return Enum.sit_down_failed_other_here

        player.state = Enum.user_state_playing
        player.sid = sid
        self.players[sid] = player

        if self.red_dragon_task_state == Enum.task_state_ing:
            if player.call_fish_timer is None:
                self.set_timer('call_fish', 3, userId=uid, first=True)

        self._info(uid, 'sit %d success' % sid)
        return 0

    def on_leave(self, uid):
        self._info(uid, 'leave')
        if uid not in self.all_user:
            self._warn(uid, 'not here')
            return Enum.leave_table_failed_not_join

        player = self.all_user[uid]
        if player.identity != Enum.identity_type_player:
            self._warn(uid, 'error identity', player.identity)
            return Enum.leave_table_failed_error_identity

        self.player_leave(uid)

        Context.Online.incr_online(self.gid, self.room_type, False)
        self._info(uid, 'leave success')
        return 0

    def on_offline(self, uid):
        self._info(uid, 'offline')
        if uid not in self.all_user:
            self._warn(uid, 'not here')
            return Enum.leave_table_failed_not_join

        player = self.all_user[uid]
        player.state = Enum.user_state_offline
        self.set_timer('offline', 10, userId=uid)
        return 0

    def on_reconnect(self, uid):
        self._info(uid, 'reconnect')
        if uid not in self.all_user:
            self._warn(uid, 'not here')
            return Enum.reconnect_failed_id

        player = self.all_user[uid]
        player.state = Enum.user_state_playing
        return 0

    def on_client_message(self, uid, cmd, mi):
        player = self.all_user.get(uid)
        if not player or player.sid is None:
            self._error(uid, 'illegal seat id')
            return -1

        mo = None
        if cmd == Message.FISH_MSG_BOARD_INFO | Message.ID_REQ:
            mo = self.on_board_info(uid, player, mi)
        elif cmd == Message.FISH_MSG_SHOT_BULLET | Message.ID_REQ:
            mo = self.on_shot_bullet(uid, player, mi)
        elif cmd == Message.FISH_MSG_MOVE_BARREL | Message.ID_REQ:
            mo = self.on_move_barrel(uid, player, mi)
        elif cmd == Message.FISH_MSG_HIT_FISH | Message.ID_REQ:
            mo = self.on_hit_fish(uid, player, mi)
        elif cmd == Message.FISH_MSG_UNLOCK_BARREL | Message.ID_REQ:
            mo = self.on_unlock_barrel(uid, player, mi)
        elif cmd == Message.FISH_MSG_SWITCH_BARREL | Message.ID_REQ:
            mo = self.on_switch_barrel(uid, player, mi)
        elif cmd == Message.FISH_MSG_SKILL_LOCK | Message.ID_REQ:
            mo = self.on_skill_lock(uid, player, mi)
        elif cmd == Message.FISH_MSG_SKILL_FREEZE | Message.ID_REQ:
            mo = self.on_skill_freeze(uid, player, mi)
        elif cmd == Message.FISH_MSG_SKILL_VIOLENT | Message.ID_REQ:
            mo = self.on_skill_violent(uid, player, mi)
        elif cmd == Message.FISH_MSG_SKILL_SUPER_WEAPON | Message.ID_REQ:
            mo = self.on_skill_super_weapon(uid, player, mi)
        elif cmd == Message.FISH_MSG_SKILL_PORTAL | Message.ID_REQ:
            mo = self.on_skill_portal(uid, player, mi)
        elif cmd == Message.FISH_MSG_LOCK_FISH | Message.ID_REQ:
            mo = self.on_lock_fish(uid, player, mi)
        elif cmd == Message.FISH_MSG_REPORT_FISHS | Message.ID_REQ:
            mo = self.on_report_fishs(uid, player, mi)

        if isinstance(mo, MsgPack):
            Context.GData.send_to_connect(uid, mo)

        return 0

    def on_board_info(self, uid, player, mi):
        self.__init_map_info()
        mo = MsgPack(Message.FISH_MSG_BOARD_INFO | Message.ID_NTF)
        # 桌面信息
        mo.set_param('start', self.map.start_ms)
        uptime = self.real_uptime()
        mo.set_param('uptime', uptime)
        self.__check_freeze(uptime)
        freeze = {'total': self.total_freeze}
        if self.lasted_freeze:
            freeze['start'] = self.lasted_freeze['start']
        mo.set_param('freeze', freeze)
        board_info, rank_info = [], []
        for player in self.players:
            if player and player.state != Enum.user_state_offline:
                info = self.get_broad_info(player)
                board_info.append(info)
                if self.red_dragon_task_state > Enum.task_state_pre:
                    all_round = player.get_all_around_fishs()
                    if all_round:
                        around_info = []
                        for loc, fish in all_round:
                            fish_type = self.map.fish_type(fish)
                            if fish_type:
                                around_info.append({
                                    'l': loc,
                                    'i': fish,
                                    't': fish_type
                                })
                                if around_info:
                                    info['around'] = around_info
                if self.bounty_task_state > Enum.task_state_pre:
                    _count = self.bounty_task.get('count', 0)
                    _ts = self.bounty_task.get('ts', 0)
                    rank_info.append((player.uid, _count, _ts))
                    if player.bounty_task:
                        prey = []
                        for _t, _cnt in self.bounty_task.iteritems():
                            cnt = player.bounty_task.get(_t, 0)
                            prey.append([_t, cnt])

                        if prey:
                            info['prey'] = prey

        if rank_info:
            rank_info.sort(cmp=self.__cmp_bounty_rank, reverse=True)
            ranks = [rank[0] for rank in rank_info]
            mo.set_param('ranks', ranks)

        mo.set_param('board', board_info)
        # 向其他人广播
        self.table_broadcast(mo, exclude=uid)

        # 地图信息
        rel_uptime, rea_uptime, left = self.relative_time()
        self.map.adjust_map_info(rel_uptime)
        mo.set_cmd(Message.FISH_MSG_BOARD_INFO | Message.ID_ACK)
        mo.set_param('map', self.map.get_map_info())
        Context.GData.send_to_connect(uid, mo)
        return 0

    def get_broad_info(self, player):
        info = {
            'u': player.uid,
            'a': player.barrel_angle,
            'b': player.bullet_number,
            'mt': player.barrel_multiple,
            'lv': player.barrel_level
        }
        return info

    def on_shot_bullet(self, uid, player, mi):
        bullet = mi.get_param('b')
        angle = mi.get_param('a')

        if not self.map:
            self._warn('maybe not req map')
            return 1

        if not player.can_shot():
            self._warn('can not shot')
            return 2

        uptime = self.real_uptime()
        if player.in_violent(uptime):
            cost = player.barrel_multiple * 2
        else:
            cost = player.barrel_multiple
        real, final = player.incr_chip(-cost, 'game.shot.bullet', roomtype=self.room_type)
        if real != -cost:
            self._warn(uid, 'have no enough chip', -cost, final)
            return 3

        key = 'game.%d.info.hash' % self.gid
        _pool_shot = 'pool.shot.%d' % self.room_type
        _shot_times = 'shot.times.%d' % self.room_type
        if player.is_pump(bullet):
            # out.chip.pump 相关key设计失误, 导致统计麻烦, 不应该带out.chip, -_-
            _out_chip_pump = 'out.chip.pump.%d' % self.room_type
            Context.Stat.mincr_daily_data(self.gid, _shot_times, 1, _pool_shot, cost, _out_chip_pump, cost)
            pool_shot, pool_pump = Context.RedisMix.hash_mincrby(key, _pool_shot, cost, _out_chip_pump, cost)
            self.pool_shot_map[self.room_type] = pool_shot
            self.pool_pump_map[self.room_type] = pool_pump
        else:
            Context.Stat.mincr_daily_data(self.gid, _shot_times, 1, _pool_shot, cost)
            self.pool_shot_map[self.room_type] = Context.RedisMix.hash_incrby(key, _pool_shot, cost)

        # change chip pool
        player.incr_chip_pool(cost)

        mo = MsgPack(Message.FISH_MSG_SHOT_BULLET | Message.ID_NTF)
        mo.set_param('u', uid)
        mo.set_param('b', bullet)
        player.bullet_number = bullet
        player.bullet_map[bullet] = {'multi': player.barrel_multiple, 'cost': cost}
        if angle is not None:
            mo.set_param('a', angle)
            player.barrel_angle = angle
        mo.set_param('c', final)
        # mo.set_param('ts', uptime)
        self.table_broadcast(mo)
        return 0

    def on_move_barrel(self, uid, player, mi):
        angle = mi.get_param('a')
        mo = MsgPack(Message.FISH_MSG_MOVE_BARREL | Message.ID_NTF)
        mo.set_param('u', uid)
        mo.set_param('a', angle)
        player.barrel_angle = angle
        self.table_broadcast(mo)
        return 0

    def on_hit_fish(self, uid, player, mi):
        bullet = mi.get_param('b')
        if bullet not in player.bullet_map:
            self._warn('bullet %d maybe hit already' % bullet)
            return 1

        info = player.bullet_map[bullet]
        del player.bullet_map[bullet]
        # mo = MsgPack(Message.FISH_MSG_HIT_FISH | Message.ID_NTF)
        # mo.set_param('u', uid)
        # mo.set_param('i', fish)
        # mo.set_param('b', bullet)
        # self.table_broadcast(mo)
        fish = mi.get_param('i')
        fish_type = self.map.fish_type(fish)
        if fish_type is None:
            self._info('fish %d maybe caught already' % fish)
            self._check_bankrupt(player)
            return 0

        fish_config = self.fish_config['map'][fish_type]
        fix_stat = None
        if fish_type == 301:    # 红龙
            # self.red_dragon_cost += info['cost']
            fix_stat = ['pool.shot.%d' % self.room_type, -info['cost'], 'red.pool.shot.%d' % self.room_type, info['cost']]
            self.pool_shot_map[self.room_type] -= info['cost']
        elif fish_config['class'] in ('boss', 'bonus') and player.get_pay_addition():
            fix_stat = ['pool.shot.%d' % self.room_type, -info['cost'], 'buff.pool.shot.%d' % self.room_type, info['cost']]
            self.pool_shot_map[self.room_type] -= info['cost']

        if player.is_pump(bullet):
            if fix_stat:
                self.pool_pump_map[self.room_type] -= info['cost']
                if fish_type == 301:
                    _ = ['out.chip.pump.%d' % self.room_type, -info['cost'], 'out.chip.red.pump.%d' % self.room_type, info['cost']]
                else:
                    _ = ['out.chip.pump.%d' % self.room_type, -info['cost'], 'out.chip.buff.pump.%d' % self.room_type, info['cost']]
                fix_stat.extend(_)
                Context.Stat.mincr_daily_data(self.gid, *_)
                Context.RedisMix.hash_mincrby('game.%d.info.hash' % self.gid, *fix_stat)
            self._check_bankrupt(player)
            return 0

        if fix_stat:
            Context.Stat.mincr_daily_data(self.gid, *fix_stat)
            Context.RedisMix.hash_mincrby('game.%d.info.hash' % self.gid, *fix_stat)

        catched_list, catched_buff = [], []
        success, is_buff = self.check_catch_fish(player, fish_type, fish_config)
        if success:
            if fish_type in [151, 153]:    # 银龙或炸弹
                uptime = self.real_uptime()
                self.special_fishs[fish_type] = {'uid': uid, 'ts': uptime + self.map.start_ms, 'multiple': info['multi']}
                ack = MsgPack(Message.FISH_MSG_HIT_FISH | Message.ID_ACK)
                ack.set_param('i', fish)
                ack.set_param('ts', uptime)
                return ack
            elif 161 <= fish_type <= 168:  # 一网打尽
                _fishs = self.map.get_all_wipe_fish()
                catched_list.extend(_fishs)
                catched_buff.extend(len(_fishs) * [is_buff])
                self.map.clear_wipe_fish()
            else:
                catched_list.append(fish)
                catched_buff.append(is_buff)

        self.process_hit_fish(info['multi'], fish, player, catched_list, catched_buff)
        return 0

    def process_hit_fish(self, multi, fish, player, catched_list, catched_buff):
        red_dragon_end = False
        bounty_end = False
        catched_bounty_fish = False
        if catched_list:
            if self.red_dragon_task_state == Enum.task_state_ing:
                self.__check_call_fish(catched_list)
                red_dragon_end = self.__check_task_end(player, catched_list)
            elif self.bounty_task_state == Enum.task_state_ing:
                catched_bounty_fish = self.__check_catch_bounty_fish(player, multi, catched_list)
                bounty_end = self.__check_task_end(player, catched_list)

            final_info, catch_fish_list, up_reward_list = self.process_catch_fishs(player, catched_list, catched_buff, multi)
            mo = MsgPack(Message.FISH_MSG_CATCH_FISH | Message.ID_NTF)
            mo.set_param('u', player.uid)
            mo.set_param('i', fish)
            if final_info:
                mo.update_param(final_info)
            if catch_fish_list:
                mo.set_param('r', catch_fish_list)
            self.table_broadcast(mo)
            if up_reward_list:
                self._notify_exp_upgrade(player, up_reward_list)

        self._check_bankrupt(player)

        if catched_bounty_fish:
            self.__notify_rank_change(player)

        if red_dragon_end and self.red_dragon_task_state == Enum.task_state_ing:
            self.__clear_task(True)
            # clear map
            self.map.clear_map()
            self.set_timer('switch', 5)
            mo = MsgPack(Message.FISH_MSG_RED_DRAGON_END | Message.ID_NTF)
            self.table_broadcast(mo)
        if bounty_end and self.bounty_task_state == Enum.task_state_ing:
            mo = MsgPack(Message.FISH_MSG_BOUNTY_END | Message.ID_NTF)
            reward = self.__random_task_reward(bounty_end)
            rw = player.issue_rewards(reward, 'bounty.reward')
            rw = FishProps.convert_reward(rw)
            mo.set_param('u', player.uid)
            mo.update_param(rw)
            self.table_broadcast(mo)
            self.__clear_task(False)
            # clear map
            # self.map.clear_map()
            # self.set_timer('switch', 5)
            # clear event
            self.map.clear_bounty_event()
            self.bounty_task_state = Enum.task_state_free

    def __notify_rank_change(self, player):
        mo = MsgPack(Message.FISH_MSG_RANK_CHANGE | Message.ID_NTF)
        mo.set_param('u', player.uid)
        info = player.bounty_task
        detail = []
        for _t, _cnt in self.bounty_task.iteritems():
            cnt = info.get(_t, 0)
            detail.append([_t, cnt])
        if detail:
            mo.set_param('dt', detail)
        rank_info = []
        for p in self.players:
            if p and p.state == Enum.user_state_playing:
                _ts = p.bounty_task.get('ts', p.uid)
                _count = p.bounty_task.get('count', 0)
                rank_info.append((p.uid, _count, _ts))
        if rank_info:
            rank_info.sort(cmp=self.__cmp_bounty_rank, reverse=True)
            ranks = [rank[0] for rank in rank_info]
            mo.set_param('rk', ranks)
        self.table_broadcast(mo)

    def __cmp_bounty_rank(self, left, right):
        result = cmp(left[1], right[1])
        if result == 0:
            result = -cmp(left[2], right[2])
        return result

    def __check_call_fish(self, catched_list):
        for fish in catched_list:
            fish_type = self.map.fish_type(fish)
            if fish_type in [302, 303]:
                for p in self.players:
                    loc = None if not p else p.get_around_loc(fish)
                    if loc is not None:
                        p.del_around_fish(loc)
                        if p.call_fish_timer:
                            if p.call_fish_timer.IsActive():
                                self.set_timer('call_fish', 5, userId=p.uid)
                        else:
                            self.set_timer('call_fish', 5, userId=p.uid)
                        break

    def __check_catch_bounty_fish(self, player, multi, catched_list):
        yes = False
        for fish in catched_list:
            fish_type = self.map.fish_type(fish)
            if fish_type in self.bounty_task:
                player.catch_bounty_fish(self.bounty_task, fish_type, multi)
                yes = True
        return yes

    def __check_task_end(self, player, catched_list):
        if self.red_dragon_task_state == Enum.task_state_ing:
            for fish in catched_list:
                fish_type = self.map.fish_type(fish)
                if fish_type == 301:    # red dragon death
                    return True
        elif self.bounty_task_state == Enum.task_state_ing:
            multi = player.bounty_task.get('multi', 0)
            if multi:  # done
                return multi

    def _check_bankrupt(self, player, leave=False):
        if player.check_bankrupt(leave):
            mo = FishAccount.check_bankrupt(player.uid, self.gid)
            if leave:
                Context.GData.send_to_connect(player.uid, mo)
            else:
                self.table_broadcast(mo)

    def _notify_exp_upgrade(self, player, up_reward_list):
        mo = MsgPack(Message.FISH_MSG_EXP_UPGRADE | Message.ID_NTF)
        level, diff = FishAccount.get_exp_info(player.uid, self.gid, player.exp)
        mo.set_param('exp', player.exp)
        mo.set_param('lv', level)
        if diff:
            mo.set_param('df', diff)
        final_reward = FishProps.merge_reward_result(True, *up_reward_list)
        final_reward = FishProps.convert_reward(final_reward)
        mo.update_param(final_reward)
        Context.GData.send_to_connect(player.uid, mo)
        return 0

    def check_catch_fish(self, player, fish_type, fish_config):
        if fish_type in (301, 302, 303) and self.red_dragon_task_state != Enum.task_state_ing:
            return False, False

        if fish_type in self.special_fishs:
            owner = self.special_fishs[fish_type]
            uptime = self.real_uptime()
            cache_uptime = owner['ts'] - self.map.start_ms
            if cache_uptime > 0 and cache_uptime + 500 >= uptime:     # 已经被标记为捕获, 等待report
                return False, False
            del self.special_fishs[fish_type]   # expired
        odds = fish_config['odds']
        if self.pool_shot and self.pool_reward:
            rate = odds * ((self.pool_shot - self.pool_reward + self.macro_control - self.pool_pump) / self.div_base + 1)
        else:
            rate = odds
        wave = fish_config['wave']
        if rate > wave[0]:
            rate = wave[0]
        elif rate < wave[1]:
            rate = wave[1]

        is_buff = False
        if player.blocked:
            rate *= (1 - player.blocked)
        else:
            uptime = self.real_uptime()
            if player.in_violent(uptime):
                rate *= (1 + self.violent_addition)

            if fish_type == 301:
                rate = player.attenuation_red_dragon(rate)
                pay_addition = player.get_red_dragon_addition()
                if pay_addition:
                    rate += pay_addition
                    is_buff = True
            elif fish_config['class'] in ('bonus', 'boss'):
                pay_addition = player.get_pay_addition()
                if pay_addition:
                    rate *= (1 + pay_addition)
                    is_buff = True

        rand = random.randint(0, 100000)
        self._debug('rate----', is_buff, rand, odds, rate, self.pool_shot, self.pool_reward, self.pool_pump, self.div_base, self.macro_control)
        return rand < int(rate * 100000), is_buff

    def __issue_catch_reward(self, player, fish, is_buff, fish_config, multiple):
        fish_class = fish_config['class']
        fish_type = fish_config['type']
        final_chip, reward_info = None, {}
        bonus_pool, bonus_count = None, None
        pipe_args = ['fish.' + str(fish_type), 1, 'class.' + str(fish_class), 1]
        if fish_class == 'bonus' or fish_class == 'boss':
            pipe_args.append('fake.bonus.count')
            pipe_args.append(1)
            _, _, bonus_count = Context.Daily.mincr_daily_data(player.uid, self.gid, *pipe_args)
        else:
            Context.Daily.mincr_daily_data(player.uid, self.gid, *pipe_args)

        del self.map.fish_map[fish]  # 已经被捕获
        point = fish_config.get('point', 0)
        if point > 0:
            if isinstance(point, list):
                point = random.choice(point)
            chip = point * multiple
            fake_chip = chip
            # 如果是奖金鱼, 按比例放入奖金池
            if fish_class == 'bonus' or fish_class == 'boss':
                ratio = Context.Configure.get_game_item_float(self.gid, 'bonus.pool.ratio', 0)
                pool_chip = int(chip * ratio)
                bonus_pool = Context.Data.hincr_game(player.uid, self.gid, 'bonus_pool', pool_chip)
                chip -= pool_chip
            _, final_chip = player.incr_chip(chip, 'catch.fish', roomtype=self.room_type)
            Context.Daily.incr_daily_data(player.uid, self.gid, 'win.chip', chip)
            reward_info['chip'] = final_chip
            reward_info['reward'] = {'chip': chip}
            if fake_chip != chip:
                reward_info['reward']['fake_chip'] = fake_chip

        if 'reward' in fish_config:  # 击杀鱼后有其他奖励
            _rewards = self.__parse_catch_reward(player, self.gid, fish_config['reward'])
            if _rewards:
                reward_info = FishProps.merge_reward_result(True, reward_info, _rewards)

        if 'chip' in reward_info:
            chg_chip = reward_info['reward']['chip']
            player.incr_chip_pool(-chg_chip)

            if fish_type == 301:
                key, field = 'game.%d.info.hash' % self.gid, 'red.pool.reward.%d' % self.room_type
                Context.RedisMix.hash_incrby(key, field, chg_chip)
                if is_buff:
                    player.today_fish_301 += 1
            elif is_buff:
                key, field = 'game.%d.info.hash' % self.gid, 'buff.pool.reward.%d' % self.room_type
                Context.RedisMix.hash_incrby(key, field, chg_chip)
            else:
                key, field = 'game.%d.info.hash' % self.gid, 'pool.reward.%d' % self.room_type
                self.pool_reward_map[self.room_type] = Context.RedisMix.hash_incrby(key, field, chg_chip)

            Context.Stat.incr_daily_data(self.gid, field, chg_chip)
            if fish_class == 'boss':    # boss或者超级boss
                nick = player.nick.decode('utf-8')
                if fish_type == 301:
                    s_pet, desc = self.__make_super_boss_desc(reward_info)
                    led = u'恭喜%s在%s中，击杀终极首领，获得%s' % (nick, self.room_name, desc)
                    if s_pet:
                        led += u'，并且幸运的被神蛋砸中，兴奋冲昏了头脑'
                else:
                    led = u'恭喜%s玩家，在%s捕获%s倍首领，获得%s金币' % (nick, self.room_name, point, chg_chip)
                mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                mo.set_param('game', {'list': [led], 'ts': Time.current_ts()})
                Context.GData.broadcast_to_system(mo)

        return reward_info, bonus_pool, bonus_count

    def __make_super_boss_desc(self, reward):
        s_pet, info = False, []
        if 'props' in reward['reward']:
            for one in reward['reward']['props']:
                if 211 <= one['id'] <= 214:
                    desc = FishProps.get_props_desc(one['id']) + u'%d个' % one['count']
                    info.append(desc)
                elif one['id'] == FishProps.S_PET_EGG:
                    s_pet = True
        chip = reward['reward'].get('chip')
        if chip:
            info.append(u'%d金币' % chip)
        return s_pet, u'，'.join(info)

    def __parse_catch_reward(self, player, gid, rewards_info):
        rewards_list = []
        for odds, rewards in rewards_info:
            rewards = Context.copy_json_obj(rewards)
            _rewards = None
            if odds == 1:  # 必中
                _rewards = random.choice(rewards)
            else:
                rand = random.randint(1, 100000)
                if rand <= 100000 * odds:  # 掉落
                    _rewards = random.choice(rewards)
            if _rewards and 'egg' in _rewards:
                _props = _rewards.get('props', [])
                _eggs, multi = [], player.barrel_multiple
                for box in _rewards['egg']:
                    if multi >= box[1]:
                        _count = multi / box[1]
                        multi %= box[1]
                        _eggs.append({'id': box[0], 'count': _count})
                del _rewards['egg']
                if _eggs:
                    _props.extend(_eggs)
                    self.__stat_egg_fall(player.uid, _eggs)
                    _rewards['props'] = _props

            self.__filter_fall_props(player, _rewards)
            if _rewards:
                _rewards = player.issue_rewards(_rewards, 'fish.fall', roomtype=self.room_type)
                if _rewards:
                    rewards_list.append(_rewards)

        if rewards_list:
            final_reward = FishProps.merge_reward_result(True, *rewards_list)
            return final_reward
        return {}

    def __filter_fall_props(self, player, rewards):
        if rewards and 'props' in rewards:
            props = player.props_info
            rcs = []
            for item in rewards['props']:
                if 201 <= item['id'] <= 204:
                    left = props.get(item['id'], 0)
                    if left >= 10:
                        continue
                if 215 <= item['id'] <= 218 and player.barrel_multiple < 1000:
                    continue
                if 223 == item['id'] and player.barrel_multiple < 10000:
                    continue
                rcs.append(item)
            if rcs:
                rewards['props'] = rcs
            else:
                del rewards['props']

    def __stat_egg_fall(self, uid, egg_list):
        pipe_args = []
        for egg in egg_list:
            pid, count = egg['id'], egg['count']
            field = 'game.fall.props.%d' % pid
            total = Context.Daily.incr_daily_data(uid, self.gid, field, count)
            if total == count:  # 今日第一次, 记录获得人数
                pipe_args.append('user.count.get.props.%d' % pid)
                pipe_args.append(1)
            pipe_args.append(field)
            pipe_args.append(count)
        if pipe_args:
            Context.Stat.mincr_daily_data(self.gid, *pipe_args)

    def notify_next_scene(self):
        mo = MsgPack(Message.FISH_MSG_NEXT_SCENE | Message.ID_NTF)
        mo.set_param('start', self.map.start_ms)
        uptime = self.real_uptime()
        mo.set_param('uptime', uptime)
        mo.set_param('map', self.map.get_map_info())
        self.table_broadcast(mo)
        return 0

    def on_unlock_barrel(self, uid, player, mi):
        mo = MsgPack(Message.FISH_MSG_UNLOCK_BARREL | Message.ID_ACK)
        conf = Context.Configure.get_game_item_json(self.gid, 'barrel.unlock.config')
        if not conf:
            self._error('miss barrel.unlock.config')
            return mo.set_error(1, 'system error')

        next_level = player.max_barrel_level + 1
        # if next_level > len(conf):
        if next_level > 36:
            return mo.set_error(2, 'max level')

        level_conf = conf[next_level - 1]
        cost = -level_conf['diamond']
        real, final = player.incr_diamond(cost, 'unlock.barrel')
        if real != cost:
            return mo.set_error(3, 'lack diamond')

        player.max_barrel_level = next_level
        multiple = FishAccount.trans_barrel_level(self.gid, next_level)
        reward = player.issue_rewards(level_conf['reward'], 'unlock.barrel')
        reward = FishProps.convert_reward(reward)
        mo = MsgPack(Message.FISH_MSG_UNLOCK_BARREL | Message.ID_NTF)
        mo.set_param('u', uid)
        mo.update_param(reward)
        final = reward.get('d', final)
        mo.set_param('d', final)
        self.table_broadcast(mo, exclude=uid)
        mo.set_param('lv', next_level)
        mo.set_param('mt', multiple)
        return mo

    def on_switch_barrel(self, uid, player, mi):
        mo = MsgPack(Message.FISH_MSG_SWITCH_BARREL | Message.ID_NTF)
        delta = mi.get_param('da')
        switch_skin = mi.get_param('si')
        level = mi.get_param('lv', 0)
        if level > 0:
            if level > self.room_config['level_max1'] or level > player.max_barrel_level:
                return -1
            player.barrel_level = level
            mo.set_param('lv', level)
            mo.set_param('mt', player.barrel_multiple)
        elif delta in (-1, 1):    # 切换炮台
            switch_level = player.barrel_level + delta
            max_barrel_level = player.max_barrel_level
            if switch_level == max_barrel_level + 2:                # 当前已经是等级预览
                switch_level = self.room_config['level_min1']
            elif switch_level > self.room_config['level_max1']:     # 最高限制
                switch_level = self.room_config['level_min1']
            elif switch_level < self.room_config['level_min1']:     # 最低限制
                switch_level = self.room_config['level_max1']

            if switch_level > max_barrel_level:
                switch_level = max_barrel_level + 1  # 等级预览
                if switch_level > 36:
                    if delta == -1:
                        switch_level = max_barrel_level
                    else:
                        switch_level = self.room_config['level_min1']

            player.barrel_level = switch_level
            mo.set_param('lv', switch_level)
            mo.set_param('mt', player.barrel_multiple)

        if switch_skin is not None:
            player.barrel_skin = switch_skin
            mo.set_param('si', switch_skin)
            mo.set_param('lv', player.barrel_level)
            mo.set_param('mt', player.barrel_multiple)

        mo.set_param('u', uid)
        self.table_broadcast(mo)
        return 0

    def on_skill_lock(self, uid, player, mi):
        """
        锁定
        """
        if self.map is None:
            return

        uptime = self.real_uptime()
        mo = MsgPack(Message.FISH_MSG_SKILL_LOCK | Message.ID_NTF)
        if player.in_locking(uptime):
            return mo.set_error(1, 'locking')

        res, final = player.use_props(FishProps.PROP_LOCK_FISH, self.room_type)
        if not res:
            diamond = player.buy_props(FishProps.PROP_LOCK_FISH)
            if diamond is None:
                return mo.set_error(2, 'no more')
            mo.set_param('d', diamond)

        player.lock['start'] = uptime
        player.lock['end'] = uptime + 15000

        mo.set_param('u', uid)
        mo.set_param('ts', uptime)
        mo.set_param('lt', final)
        self.table_broadcast(mo)
        return 0

    def on_lock_fish(self, uid, player, mi):
        if self.map is None:
            return

        uptime = self.real_uptime()
        mo = MsgPack(Message.FISH_MSG_LOCK_FISH | Message.ID_NTF)
        if player.in_locking(uptime) or player.in_violent(uptime):
            fish = mi.get_param('i')
            mo.set_param('u', uid)
            mo.set_param('i', fish)
            mo.set_param('ts', uptime)
            self.table_broadcast(mo)
            return 0
        return mo.set_error(1, 'not in locking')

    def on_skill_freeze(self, uid, player, mi):
        if self.map is None:
            return

        mo = MsgPack(Message.FISH_MSG_SKILL_FREEZE | Message.ID_NTF)
        if self.red_dragon_task_state > Enum.task_state_pre:
            return mo.set_error(1, 'in task')
        if self.bounty_task_state > Enum.task_state_pre:
            return mo.set_error(1, 'in, task')

        res, final = player.use_props(FishProps.PROP_FREEZE, self.room_type)
        if not res:
            diamond = player.buy_props(FishProps.PROP_FREEZE)
            if diamond is None:
                return mo.set_error(2, 'no more')
            mo.set_param('d', diamond)

        uptime = self.real_uptime()
        self.__check_freeze(uptime)
        if self.lasted_freeze:
            left_ms = self.lasted_freeze['end'] - uptime
            delay_timer = 15000 - left_ms
            self.total_freeze += delay_timer
        else:
            delay_timer = 15000

        # delay scene switch timer
        delay_second = delay_timer / 1000.0
        if self.delta_timer.IsActive():
            self.delta_timer.delay(delay_second)
            self._info('freeze, delay delta_timer', delay_second)
        if self.switch_timer.IsActive():
            self.switch_timer.delay(delay_second)
            self._info('freeze, delay switch_timer', delay_second)

        if self.red_dragon_task_state == Enum.task_state_pre:
            if self.red_dragon_timer.IsActive():
                self.red_dragon_timer.delay(delay_second)
                self._info('freeze, delay red_dragon_timer', delay_second)

        if self.bounty_task_state == Enum.task_state_pre:
            if self.bounty_timer.IsActive():
                self.bounty_timer.delay(delay_second)
                self._info('freeze, delay bounty_timer', delay_second)

        self.lasted_freeze['start'] = uptime
        self.lasted_freeze['end'] = uptime + 15000
        mo.set_param('u', uid)
        mo.set_param('ts', uptime)
        mo.set_param('lt', final)
        self.table_broadcast(mo)
        return 0

    def __check_freeze(self, uptime):
        if self.lasted_freeze:
            end_ms = self.lasted_freeze['end']
            if end_ms <= uptime:  # expired
                self.total_freeze += 15000
                self.lasted_freeze.clear()

    def on_skill_violent(self, uid, player, mi):
        """
        双倍击杀概率, 30秒内击杀获得双倍金币, vip3以上使用
        """
        if self.map is None:
            return

        mo = MsgPack(Message.FISH_MSG_SKILL_VIOLENT | Message.ID_NTF)
        vip_level = FishAccount.get_vip_level(uid, self.gid)
        can = 0
        if vip_level < 3:
            can = Context.Data.setnx_game_attr(uid, self.gid, 'try_violent', 1)
            if not can:
                return mo.set_error(1, 'level limit')

        res, final = player.use_props(FishProps.PROP_VIOLENT, self.room_type)
        if not res:
            diamond = player.buy_props(FishProps.PROP_VIOLENT)
            if diamond is None:
                if can:
                    Context.Data.del_game_attrs(uid, self.gid, 'try_violent')
                return mo.set_error(2, 'no more')
            mo.set_param('d', diamond)

        uptime = self.real_uptime()
        player.violent['start'] = uptime
        player.violent['end'] = uptime + 30000
        mo.set_param('u', uid)
        mo.set_param('ts', uptime)
        mo.set_param('lt', final)
        self.table_broadcast(mo)
        return 0

    def on_skill_super_weapon(self, uid, player, mi):
        """
        vip2以上使用, 辐射一块
        """
        if self.map is None:
            return

        mo = MsgPack(Message.FISH_MSG_SKILL_SUPER_WEAPON | Message.ID_NTF)
        if self.red_dragon_task_state > Enum.task_state_pre:
            return mo.set_error(10, 'in task')
        if self.bounty_task_state > Enum.task_state_pre:
            return mo.set_error(10, 'in task')

        pt = mi.get_param('pt')
        vip_level = FishAccount.get_vip_level(uid, self.gid)
        can = 0
        if vip_level < 2:
            can = Context.Data.setnx_game_attr(uid, self.gid, 'try_super_weapon', 1)
            if not can:
                return mo.set_error(1, 'level limit')

        res, final = player.use_props(FishProps.PROP_SUPER_WEAPON, self.room_type)
        if not res:
            diamond = player.buy_props(FishProps.PROP_SUPER_WEAPON)
            if diamond is None:
                if can:
                    Context.Data.del_game_attrs(uid, self.gid, 'try_super_weapon')
                return mo.set_error(2, 'no more')
            mo.set_param('d', diamond)

        uptime = self.real_uptime()
        fishs = mi.get_param('fishs')
        fishs = set(fishs)
        catched_list, catched_buff = [], []
        for fish in fishs:
            fish_type = self.map.fish_type(fish)
            if not fish_type or fish_type in self.fish_config['boss']:    # boss无效
                continue
            fish_config = self.fish_config['map'][fish_type]
            if 0 < fish_config['point'] <= self.super_weapon_config['dead']:
                catched_list.append(fish)
                catched_buff.append(False)
            else:
                success, is_buff = self.check_catch_fish(player, fish_type, fish_config)
                if success:
                    catched_list.append(fish)
                    catched_buff.append(is_buff)

        mo.set_param('u', uid)
        mo.set_param('pt', pt)
        mo.set_param('ts', uptime)
        mo.set_param('lt', final)

        # 固定金币获得
        fixed_chip, final = player.incr_chip(self.super_weapon_config['fix'], 'super.weapon.fix')
        mo.set_param('fc', fixed_chip)
        mo.set_param('c', final)

        if catched_list:    # 有鱼挂
            multiple = self.super_weapon_config['multi']
            final_info, catch_fish_list, up_reward_list = self.process_catch_fishs(player, catched_list, catched_buff, multiple)
            mo.update_param(final_info)
            if catch_fish_list:
                mo.set_param('r', catch_fish_list)
            self.table_broadcast(mo)

            if up_reward_list:  # 等级升级提醒
                self._notify_exp_upgrade(player, up_reward_list)
        else:
            self.table_broadcast(mo)

        return 0

    def on_skill_portal(self, uid, player, mi):
        """
        随机召唤一只鱼
        """
        if self.map is None:
            return

        mo = MsgPack(Message.FISH_MSG_SKILL_PORTAL | Message.ID_NTF)
        if self.red_dragon_task_state > Enum.task_state_pre:
            return mo.set_error(1, 'in task')
        if self.bounty_task_state > Enum.task_state_pre:
            return mo.set_error(1, 'in task')

        res, final = player.use_props(FishProps.PROP_PORTAL, self.room_type)
        if not res:
            diamond = player.buy_props(FishProps.PROP_PORTAL)
            if diamond is None:
                return mo.set_error(2, 'no more')
            mo.set_param('d', diamond)

        uptime = self.real_uptime()
        fish = self.map.make_bonus(int(uptime) / 100)
        mo.set_param('u', uid)
        mo.set_param('fish', fish)
        mo.set_param('ts', uptime)
        mo.set_param('lt', final)
        self.table_broadcast(mo)
        return 0

    def check_exp_level(self, player, gid, exp, delta):
        prev_level, prev_diff = FishAccount.get_exp_info(player.uid, gid, exp)
        player.exp = Context.Data.hincr_game(player.uid, gid, 'exp', delta)
        now_level, now_diff = FishAccount.get_exp_info(player.uid, gid, player.exp)

        up_reward_list = []
        while prev_level < now_level:
            # 升级礼包
            conf = Context.Configure.get_game_item_json(gid, 'exp.level.reward')
            rewards = conf[prev_level]
            rewards_info = player.issue_rewards(rewards, 'exp.upgrade')
            prev_level += 1
            up_reward_list.append(rewards_info)
        return up_reward_list

    def on_report_fishs(self, uid, player, mi):
        fish = mi.get_param('fish')
        ts = mi.get_param('ts')
        fish_type = self.map.fish_type(fish)
        if not fish_type:
            self._warn('fish %d maybe caught already' % fish)
            return 0
        owner = self.special_fishs.get(fish_type)
        if not owner or owner['uid'] != uid:
            self._warn('uid not match')
            return 0

        del self.special_fishs[fish_type]
        if owner['ts'] - self.map.start_ms != ts:
            self._warn('ts not match')
            return 0

        uptime = self.real_uptime()
        if owner['ts'] + 500 < uptime:
            self._info('report expired, pass')
            return 0

        multiple = owner['multiple']
        fishs = mi.get_param('fishs')
        fishs = set(fishs)
        catched_list, catched_buff = [fish], [False]
        for fish in fishs:
            fish_type = self.map.fish_type(fish)
            if fish_type not in self.fish_config['common']:
                continue
            fish_config = self.fish_config['map'][fish_type]
            if fish_config['point'] < 30:
                catched_list.append(fish)
                catched_buff.append(False)
            else:
                success, is_buff = self.check_catch_fish(player, fish_type, fish_config)
                if success:
                    catched_list.append(fish)
                    catched_buff.append(is_buff)

        mo = MsgPack(Message.FISH_MSG_CATCH_FISH | Message.ID_NTF)
        mo.set_param('u', uid)
        mo.set_param('b', fish)
        final_info, catch_fish_list, up_reward_list = self.process_catch_fishs(player, catched_list, catched_buff, multiple)
        if final_info:
            mo.update_param(final_info)
        if catch_fish_list:
            mo.set_param('r', catch_fish_list)
        self.table_broadcast(mo)

        if up_reward_list:  # 等级升级提醒
            self._notify_exp_upgrade(player, up_reward_list)
        return 0

    def process_catch_fishs(self, player, fishs, buffs, multiple):
        catch_reward_list, catch_fish_list = [], []
        bonus_pool, bonus_count = 0, 0
        for fish, buff in zip(fishs, buffs):
            fish_type = self.map.fish_type(fish)
            fish_config = self.fish_config['map'][fish_type]
            catch_reward, bonus_pool, bonus_count = self.__issue_catch_reward(player, fish, buff, fish_config, multiple)
            catch_reward_list.append(catch_reward)
            catch_reward = FishProps.convert_reward(catch_reward)
            catch_fish_list.append({'i': fish, 'w': catch_reward['w']})

        if len(catch_reward_list) == 1:
            final_info = FishProps.convert_reward(catch_reward_list[0])
            del final_info['w']
        else:
            final_info = FishProps.merge_reward_result(False, *catch_reward_list)
            final_info = FishProps.convert_reward(final_info)

        if bonus_pool > 0:
            final_info['bonus_pool'] = bonus_pool
        if bonus_count > 0:
            final_info['bonus_count'] = bonus_count

        up_reward_list = self.check_exp_level(player, self.gid, player.exp, len(catch_fish_list))
        return final_info, catch_fish_list, up_reward_list
