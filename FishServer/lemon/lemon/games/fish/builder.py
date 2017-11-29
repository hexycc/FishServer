#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-12-04

import random
from framework.context import Context


class PathMaker(object):
    area_range = (
        ((80, 640), (0, 0)), ((640, 1200), (0, 0)),
        ((1280, 1280), (60, 360)), ((1280, 1280), (360, 660)),
        ((640, 1200), (720, 720)), ((80, 640), (720, 720)),
        ((0, 0), (360, 660)), ((0, 0), (60, 360))
    )
    pt_type_undefine = 0
    pt_type_line = 1
    pt_type_spline = 2
    pt_type_bezier = 3
    pt_type_inprinting = 10

    def generate_in_out_pt(self):
        area_len = len(self.area_range)
        index = random.randrange(0, area_len)
        p1_range = self.area_range[index]
        index = random.randrange(index + 2, index + 7) % area_len
        p2_range = self.area_range[index]
        x1 = random.randint(*p1_range[0])
        y1 = random.randint(*p1_range[1])
        x2 = random.randint(*p2_range[0])
        y2 = random.randint(*p2_range[1])
        return x1, y1, x2, y2

    def generate_in_out_pt_2(self):
        area_len = len(self.area_range)
        index = random.randrange(0, area_len)
        p1_range = self.area_range[index]
        index = random.randrange(index + 3, index + 6) % area_len
        p2_range = self.area_range[index]
        x1 = random.randint(*p1_range[0])
        y1 = random.randint(*p1_range[1])
        x2 = random.randint(*p2_range[0])
        y2 = random.randint(*p2_range[1])
        return x1, y1, x2, y2

    def generate_inner_pt(self):
        x = random.randint(80, 1200)
        y = random.randint(60, 660)
        return x, y

    def build_line(self):
        x1, y1, x2, y2 = self.generate_in_out_pt_2()
        return [self.pt_type_line, x1, y1, x2, y2]

    def build_line_2(self):
        y1 = y2 = random.randint(180, 540)
        if random.randint(0, 1) == 0:
            x1, x2 = 0, 1280
        else:
            x1, x2 = 1280, 0
        return [self.pt_type_line, x1, y1, x2, y2]

    def build_spline(self):
        x1, y1, x2, y2 = self.generate_in_out_pt_2()
        spline = [self.pt_type_spline, x1, y1]
        while len(spline) < 13:
            x, y = self.generate_inner_pt()
            spline.append(x)
            spline.append(y)
        spline.append(x2)
        spline.append(y2)
        return spline

    def build_bezier(self):
        x1, y1, x2, y2 = self.generate_in_out_pt_2()
        x, y = self.generate_inner_pt()
        return [self.pt_type_bezier, x1, y1, x, y, x2, y2]

    def generate_inprinting(self):
        count = random.randrange(5, 10)
        inprinting = [self.pt_type_inprinting, count, 1500]
        t = random.choice([self.build_line, self.build_bezier])()
        inprinting.extend(t)
        return inprinting

    def generate_basic_path(self):
        funcs = [self.build_line, self.build_bezier]
        func = random.choice(funcs)
        return func()


class MapBuilder(PathMaker):
    """
    新手场201: |--5分钟-->|--30秒boss-->|--5分钟-->|--30秒boss-->|--5分钟-->|--鱼潮1分钟-->|
    中级场202: |--5分钟-->|--30秒boss-->|--5分钟-->|--30秒boss-->|--5分钟-->|--悬赏3分钟-->|--1分钟-->|--鱼潮1分钟-->|
    高级场203: |--5分钟-->|--30秒boss-->|--5分钟-->|--30秒boss-->|--5分钟-->|--悬赏3分钟-->|--1分钟-->|--鱼潮1分钟-->|
    银龙: 第一次出现时间随机, 然后每隔20s出现, 鱼潮不能出现
    钻石宝箱: 每局出现一次, 后7分钟随机出现
    一网打尽: 每局出现一次, 普通boss出现后30s出现
    炸弹: 每局出现一次, 前7分钟随机出现
    """
    map_event_common = 0
    map_event_boss = 1
    map_event_tide = 2
    map_event_special = 3
    map_event_bonus = 4
    map_event_red_dragon = 5
    map_event_bounty = 6

    fish_info_map = {}
    timeline_map = {}

    bk_imgs = ('1', '2', '3', '4')

    def __init__(self, roomtype):
        self.roomtype = roomtype
        self.fish_id = 0
        self.uptime = 0
        self.start_ms = 0
        self.events = []
        self.fishs = []
        self.tide = {}
        self.bounty = {}
        self.img = None
        self.next_img = None
        self.tide_img = None
        self.fish_map = {}
        self.total_ts = 0
        self.next_dragsil_in_time = None            # 下一次银龙出现的时间
        self.next_box_in_time = None                # 下一次钻石宝盒出现的时间
        self.next_wipe_in_time = None               # 下一次一网打尽出现的时间
        self.next_bomb_in_time = None               # 下一次炸弹的出现时间
        self.wipe_fishs = []

    @classmethod
    def load_config(cls, gid):
        for roomtype in (201, 202, 203):
            conf = Context.Configure.get_game_item_json(gid, 'timeline.%d.config' % roomtype)
            conf = Context.copy_json_obj(conf)
            for k in ('boss', 'tide', 'bounty'):
                conf[k] = [int(t*10) for t in conf[k]]
            cls.timeline_map[roomtype] = conf

            conf = Context.Configure.get_game_item_json(gid, 'fish.%d.config' % roomtype)
            kvs = {}
            for k in ('common', 'boss', 'bonus'):
                types = [item['type'] for item in conf[k]]
                kvs[k] = types
            kvs['little'] = kvs['common'][:9]
            kvs['middle'] = kvs['common'][9:]
            kvs['bonus'] = kvs['bonus'][:-1]    # 红龙任务中红龙奖金鱼去掉
            kvs['boss'] = kvs['boss'][:-1]      # 红龙任务中红龙去掉
            cls.fish_info_map[roomtype] = kvs

    @classmethod
    def get_total_time(cls, roomtype):
        return cls.timeline_map[roomtype]['total']

    @property
    def little(self):
        return self.fish_info_map[self.roomtype]['little']

    @property
    def middle(self):
        return self.fish_info_map[self.roomtype]['middle']

    @property
    def common(self):
        return self.fish_info_map[self.roomtype]['common']

    @property
    def boss(self):
        return self.fish_info_map[self.roomtype]['boss']

    @property
    def bonus(self):
        return self.fish_info_map[self.roomtype]['bonus']

    def fish_type(self, fish):
        b = self.fish_map.get(fish)
        if b:
            return b['t']

    def new_map(self, next_img=None):
        duration, ev_list, fishs = self.__new_map(next_img)
        self.events.extend(ev_list)
        self.fishs.extend(fishs)
        return duration, ev_list, fishs

    def __new_map(self, next_img):
        if next_img:
            self.img = next_img
        else:
            self.img = random.choice(self.bk_imgs)
        imgs = [k for k in self.bk_imgs if k != self.img]
        self.next_img, self.tide_img = random.sample(imgs, 2)
        self.total_ts = self.get_total_time(self.roomtype)
        self.start_ms = Context.Time.current_ms()
        self.uptime = 300
        start, fishs = 0, []
        self.next_dragsil_in_time = random.randint(250, 600)
        self.next_box_in_time = random.randint(14 * 600, 15 * 600)
        self.next_wipe_in_time = random.randint(11 * 600, 15 * 600)
        self.next_bomb_in_time = random.randint(600, 7 * 600)

        while start < self.uptime:
            if random.randint(0, 1000) <= 125:
                fish = self.__make_bonus(start, False)
            elif start >= self.next_dragsil_in_time:
                fish = self.__make_dragsil(start)
            elif start >= self.next_box_in_time:
                fish = self.__make_box(start)
            elif start >= self.next_wipe_in_time:
                fish = self.__make_wipe(start)
            elif start >= self.next_bomb_in_time:
                fish = self.__make_bomb(start)
            else:
                fish = self.__make_common(start)
            if isinstance(fish, list):
                fishs.extend(fish)
            else:
                fishs.append(fish)
            start += random.randint(5, 20)

        return 30, [], fishs

    def has_more_map(self):
        return self.uptime + 100 < self.total_ts * 10

    def clear_map(self):
        self.fish_map.clear()
        self.tide.clear()
        self.fishs = []
        self.events = []

    def clear_bounty_event(self):
        self.events = [ev for ev in self.events if ev['type'] != self.map_event_bounty]

    def get_tide_map(self):
        start = self.uptime
        timeline = self.timeline_map[self.roomtype]
        if start in timeline['tide']:
            show, tide = self.new_fish_tide(start)
            self.uptime = start + show * 10
            event = {'in': start, 'type': self.map_event_tide, 'show': show}
            self.events.append(event)
            return show, [event], tide
        return None

    def get_bounty_map(self):
        start = self.uptime
        timeline = self.timeline_map[self.roomtype]
        if start in timeline['bounty']:
            show, bounty = self.new_bounty_task(start)
            event = {'in': start, 'type': self.map_event_bounty, 'show': show}
            self.events.append(event)
            return show, [event], bounty
        return None

    def delta_map(self):
        start = self.uptime
        duration, ev_list, fishs = self.__delta_map(start)
        self.events.extend(ev_list)
        self.fishs.extend(fishs)
        return start, duration, ev_list, fishs

    def __delta_map(self, start):
        timeline = self.timeline_map[self.roomtype]
        self.uptime = start + 300
        fishs, event_list = [], []
        while start < self.uptime:
            if start in timeline['boss']:
                show, fish = self.__make_boss(start)
                event = {'in': start, 'type': self.map_event_boss, 'show': show}
                event_list.append(event)
            elif start >= self.next_dragsil_in_time:
                fish = self.__make_dragsil(start)
            elif start >= self.next_box_in_time:
                fish = self.__make_box(start)
            elif start >= self.next_wipe_in_time:
                fish = self.__make_wipe(start)
            elif start >= self.next_bomb_in_time:
                fish = self.__make_bomb(start)
            else:
                if random.randint(0, 1000) <= 125:
                    fish = self.__make_bonus(start, False)
                else:
                    fish = self.__make_common(start)
            start += random.randint(5, 20)
            if isinstance(fish, list):
                fishs.extend(fish)
            else:
                fishs.append(fish)
        return 30, event_list, fishs

    def make_red_dragon(self):
        start = self.uptime
        self.uptime += 2100
        ev = {'in': start, 'type': self.map_event_red_dragon, 'show': 210}
        self.events.append(ev)
        fish = self.__make_red_dragon(start)
        self.fishs.append(fish)
        return start, 210, [ev], [fish]

    def __make_red_dragon(self, start):
        self.fish_id += 1
        fish = {
            't': 301,
            'i': self.fish_id,
            'n': start,
            's': 210,
        }
        self.fish_map[self.fish_id] = fish
        return fish

    def make_little_red_dragon(self):
        self.fish_id += 1
        fish = {
            't': 302,
            'i': self.fish_id,
        }
        self.fish_map[self.fish_id] = fish
        return fish

    def make_red_dragon_bonus(self):
        self.fish_id += 1
        fish = {
            't': 303,
            'i': self.fish_id,
        }
        self.fish_map[self.fish_id] = fish
        return fish

    def get_map_info(self):
        map_info = {
            'img': self.img,
            'next_img': self.next_img,
        }
        if self.tide:
            map_info['tide'] = self.tide
        if self.fishs:
            map_info['fishs'] = self.fishs
        if self.events:
            map_info['events'] = self.events
        if self.bounty:
            map_info['bounty'] = self.bounty
        return map_info

    def adjust_map_info(self, uptime):
        index = 0
        for i, fish in enumerate(self.fishs, 1):
            if 'p' in fish and fish['p'][0] == self.pt_type_inprinting:
                end_ts = fish['n'] * 100 + fish['s'] * 1000 + fish['p'][1] * fish['p'][2]
            else:
                end_ts = fish['n'] * 100 + fish['s'] * 1000
            if uptime <= end_ts:
                break
            index = i
        if index > 0:
            del self.fishs[0:index]

        if self.tide:
            end_ts = self.tide['in'] * 100 + self.tide['show'] * 1000
            if uptime >= end_ts:
                self.tide.clear()

        if self.events:
            ev_list = []
            for ev in self.events:
                end_ts = ev['in'] * 100 + ev['show'] * 1000
                if uptime < end_ts:
                    ev_list.append(ev)
            self.events = ev_list

    def get_all_wipe_fish(self):
        return self.wipe_fishs

    def clear_wipe_fish(self):
        self.wipe_fishs = []

    def __make_common(self, start):
        """
        普通的鱼走直线, 样条, 贝塞尔, 可以指定印随鱼阵
        """
        self.fish_id += 1
        pt = self.generate_basic_path()
        if random.randint(0, 90) > 30:
            _type = random.choice(self.little)
        else:
            _type = random.choice(self.middle)

        fish = {
            't': _type,
            'i': self.fish_id,
            'n': start,
            's': 30,
            'p': pt,
        }

        self.fish_map[self.fish_id] = fish
        return fish

    def __make_boss(self, start):
        """
        boss 只走直线
        """
        self.fish_id += 1
        fish = {
            't': random.choice(self.boss),
            'i': self.fish_id,
            'n': start,
            's': 60,
            'p': self.build_line_2(),
        }
        self.fish_map[self.fish_id] = fish
        return 60, fish

    def __make_dragsil(self, start):
        self.fish_id += 1
        fish = {
            't': 151,
            'i': self.fish_id,
            'n': start,
            's': 30,
            'p': self.build_line_2(),
        }
        self.fish_map[self.fish_id] = fish
        self.next_dragsil_in_time = start + 500
        if self.next_dragsil_in_time + 30 >= 16*60:
            self.next_dragsil_in_time = 600 * 999
        return fish

    def __make_box(self, start):
        self.fish_id += 1
        fish = {
            't': 152,
            'i': self.fish_id,
            'n': start,
            's': 30,
            'p': self.build_line_2(),
        }
        self.fish_map[self.fish_id] = fish
        self.next_box_in_time = 600 * 999
        return fish

    def __make_wipe(self, start):
        fishs = []
        ids = random.sample((161, 162, 163, 164, 165, 166, 167, 168), 6)
        for i in (0, 1, 2, 3, 4, 5):
            self.fish_id += 1
            fish = {
                't': ids[i],
                'i': self.fish_id,
                'n': start,
                's': 30,
                'p': self.build_line(),
            }
            self.fish_map[self.fish_id] = fish
            self.wipe_fishs.append(self.fish_id)
            fishs.append(fish)
        self.next_wipe_in_time = 600 * 999
        return fishs

    def __make_bomb(self, start):
        self.fish_id += 1
        fish = {
            't': 153,
            'i': self.fish_id,
            'n': start,
            's': 30,
            'p': self.build_line_2(),
        }
        self.fish_map[self.fish_id] = fish
        self.next_bomb_in_time = 600 * 999
        return fish

    def make_bonus(self, start):
        fish = self.__make_bonus(start)
        for i, b in enumerate(self.fishs):
            if b['n'] > start:
                self.fishs.insert(i, fish)
                break
        else:
            self.fishs.append(fish)
        return fish

    def __make_bonus(self, start, inner=True):
        self.fish_id += 1
        pt = self.build_bezier()
        if inner:
            _t = self.generate_inner_pt()
            pt[1] = _t[0]
            pt[2] = _t[1]
        fish = {
            't': random.choice(self.bonus),
            'i': self.fish_id,
            'n': start,
            's': 30,
            'p': pt,
        }
        self.fish_map[self.fish_id] = fish
        return fish

    def __make_inprinting(self, start):
        self.fish_id += 1
        pt = self.generate_inprinting()
        fish = {
            't': random.choice(self.common),
            'i': self.fish_id,
            'n': start,
            's': 30,
            'p': pt,
        }
        self.fish_map[self.fish_id] = fish
        count = pt[1]
        while count > 1:
            self.fish_id += 1
            self.fish_map[self.fish_id] = fish
            count -= 1
        return fish

    def new_fish_tide(self, start):
        which = random.randint(1, 5)
        func = getattr(self, '_make_tide_%s' % which)
        return func(start)

    def _make_tide_1(self, start):
        tide_info = [[101, 72], [102, 72], [176, 6]]
        return self.__make_tide(start, 1, tide_info)

    def _make_tide_2(self, start):
        tide_info = [[101, 44], [102, 51], [176, 3]]
        return self.__make_tide(start, 2, tide_info)

    def _make_tide_3(self, start):
        tide_info = [[101, 8], [102, 16], [103, 32], [176, 2]]
        return self.__make_tide(start, 3, tide_info)

    def _make_tide_4(self, start):
        tide_info = [[101, 36], [102, 36], [103, 18], [176, 6]]
        return self.__make_tide(start, 4, tide_info)

    def _make_tide_5(self, start):
        tide_info = [[101, 24], [102, 24], [103, 16], [104, 14]]
        return self.__make_tide(start, 5, tide_info)

    def __make_tide(self, start, which, tide_info):
        info = []
        tide = {
            'type': which,
            'info': info,
            'in': start,
            'show': 60,
            'img': self.tide_img,
        }
        self.tide = tide
        for _t, _c in tide_info:
            info.append({'id': self.fish_id + 1, 'type': _t})
            while _c > 0:
                _c -= 1
                self.fish_id += 1
                fish = {
                    't': _t,
                    'i': self.fish_id,
                    'n': start,
                    's': 60,
                }
                self.fish_map[self.fish_id] = fish

        return 60, tide

    def new_bounty_task(self, start):
        little = random.choice(self.little)
        middle = random.choice(self.middle)
        bonus = random.choice(self.bonus)
        info = [[little, 2], [middle, 1], [bonus, 1]]
        bounty = {
            'in': start,
            'show': 180,
            'info': info
        }
        self.bounty = bounty
        return 180, bounty

    def new_cook_task(self, start):
        little = random.choice(self.little)
        middle = random.choice(self.middle)
        bonus = random.choice(self.bonus)
        info = [[little, 2], [middle, 1], [bonus, 1]]
        task = {
            'in': start,
            'show': 180,
            'info': info
        }
        return 180, task
