#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-08-26

import random
from const import Message
from props import FishProps
from framework.util.tool import Time
from framework.util.tool import Tool
from framework.context import Context
from framework.entity.msgpack import MsgPack


class FishTask(object):
    def on_task_list(self, uid, gid, mi):
        conf = Context.Configure.get_game_item_json(gid, 'task.config')
        task_list = Context.Daily.get_daily_data(uid, gid, 'task.list')
        if task_list:
            task_list = Context.json_loads(task_list)
        else:
            what_day = Time.weekday(today=True)
            task_types = conf['daily'][what_day]
            task_map = {}
            for task in conf['task']:
                task_map[task['type']] = task
            total_degree, task_list = 0, []
            for i, task_type in enumerate(task_types):
                task = {'id': i, 'type': task_type}
                if task_type == 2:  # boss
                    task['total'] = random.randint(*task_map[task_type]['range'])
                    task['desc'] = task_map[task_type]['desc']
                    task['degree'] = task_map[task_type]['degree']
                elif task_type == 3:
                    task['total'] = random.randint(*task_map[task_type]['range'])
                    task['desc'] = task_map[task_type]['desc']
                    task['degree'] = task_map[task_type]['degree']
                elif task_type == 11:
                    barrel_level = Context.Data.get_game_attr_int(uid, gid, 'barrel_level', 1)
                    task['total'] = random.randint(*task_map[task_type]['range']) * barrel_level
                    task['desc'] = task_map[task_type]['desc']
                    task['degree'] = task_map[task_type]['degree']
                elif task_type == 21:
                    task['desc'] = task_map[task_type]['desc']
                    task['degree'] = task_map[task_type]['degree']
                elif task_type == 31:
                    task['desc'] = task_map[task_type]['desc']
                    task['degree'] = task_map[task_type]['degree']
                else:
                    break
                total_degree += task['degree']
                task_list.append(task)

            if total_degree < conf['total_degree']:
                fish_config = Context.Configure.get_game_item_json(gid, 'fish.201.config')
                fish_config = Context.copy_json_obj(fish_config)
                while total_degree < conf['total_degree']:  # 普通鱼填充, 直到达到最大活跃值
                    task_type = 1
                    task = {'id': len(task_list), 'type': task_type}
                    index = random.randrange(0, len(fish_config['common']))
                    fish = fish_config['common'][index]
                    del fish_config['common'][index]
                    task['total'] = random.randint(*task_map[task_type]['range'])
                    task['desc'] = task_map[task_type]['desc']
                    task['fish_type'] = fish['type']
                    if isinstance(task_map[task_type]['degree'], list):
                        for rg in task_map[task_type]['degree']:
                            if task['total'] >= rg[0]:
                                task['degree'] = rg[1]
                                break
                        else:
                            task['degree'] = task_map[task_type]['degree'][-1][1]
                    else:
                        task['degree'] = task_map[task_type]['degree']
                    total_degree += task['degree']
                    task_list.insert(0, task)

            Context.Daily.set_daily_data(uid, gid, 'task.list', Context.json_dumps(task_list))

        rewards, degree = [], 0
        for task in task_list:
            if task['type'] == 1:
                count = Context.Daily.get_daily_data(uid, gid, 'fish.' + str(task['fish_type']))
                task['count'] = Tool.to_int(count, 0)
            elif task['type'] == 2:
                count = Context.Daily.get_daily_data(uid, gid, 'class.boss')
                task['count'] = Tool.to_int(count, 0)
            elif task['type'] == 3:
                count = Context.Daily.get_daily_data(uid, gid, 'class.bonus')
                task['count'] = Tool.to_int(count, 0)
            elif task['type'] == 11:
                count = Context.Daily.get_daily_data(uid, gid, 'win.chip')
                task['count'] = Tool.to_int(count, 0)
            elif task['type'] == 21:
                task['done'] = 1
                degree += task['degree']

            if 'count' in task and task['count'] >= task['total']:
                task['done'] = 1
                degree += task['degree']

        # 处理奖励
        _ids = range(len(conf['reward']))
        for i, _id in enumerate(_ids):
            _ids[i] = 'task.reward.%d' % _id

        _states = Context.Daily.get_daily_data(uid, gid, *_ids)
        for _state, reward in zip(_states, conf['reward']):
            _state = 1 if _state else 0
            _reward = FishProps.convert_reward(reward['reward'])
            rewards.append({'degree': reward['degree'], 'state': _state, 'reward': _reward})

        mo = MsgPack(Message.MSG_SYS_TASK_LIST | Message.ID_ACK)
        mo.set_param('tasks', task_list)
        mo.set_param('reward', rewards)
        mo.set_param('degree', degree)
        return mo

    def on_consume_task(self, uid, gid, mi):
        _id = mi.get_param('id')
        mo = MsgPack(Message.MSG_SYS_CONSUME_TASK | Message.ID_ACK)
        task_list = Context.Daily.get_daily_data(uid, gid, 'task.list')
        if not task_list:
            return mo.set_error(1, 'no task')

        task_list = Context.json_loads(task_list)
        degree = 0
        for task in task_list:
            if task['type'] == 1:
                count = Context.Daily.get_daily_data(uid, gid, 'fish.' + str(task['fish_type']))
                task['count'] = Tool.to_int(count, 0)
            elif task['type'] == 2:
                count = Context.Daily.get_daily_data(uid, gid, 'class.boss')
                task['count'] = Tool.to_int(count, 0)
            elif task['type'] == 3:
                count = Context.Daily.get_daily_data(uid, gid, 'class.bonus')
                task['count'] = Tool.to_int(count, 0)
            elif task['type'] == 11:
                count = Context.Daily.get_daily_data(uid, gid, 'win.chip')
                task['count'] = Tool.to_int(count, 0)
            elif task['type'] == 21:
                degree += task['degree']

            if 'count' in task and task['count'] >= task['total']:
                task['done'] = 1
                degree += task['degree']

        conf = Context.Configure.get_game_item_json(gid, 'task.config')
        for i, reward in enumerate(conf['reward']):
            if i == _id:
                if degree < reward['degree']:
                    return mo.set_error(2, 'not done')
                state = Context.Daily.incr_daily_data(uid, gid, 'task.reward.%d' % _id, 1)
                if state > 1:
                    return mo.set_error(3, 'received')
                reward = FishProps.issue_rewards(uid, gid, reward['reward'], 'task.reward.%d' % _id)
                _reward = FishProps.convert_reward(reward)
                mo.update_param(_reward)
                break
        else:
            mo.set_error(4, 'error id')

        return mo

    def get_total_degree(self, uid, gid):
        task_list = Context.Daily.get_daily_data(uid, gid, 'task.list')
        if not task_list:
            return 0

        task_list = Context.json_loads(task_list)
        degree = 0
        for task in task_list:
            if task['type'] == 1:
                count = Context.Daily.get_daily_data(uid, gid, 'fish.' + str(task['fish_type']))
                task['count'] = Tool.to_int(count, 0)
            elif task['type'] == 2:
                count = Context.Daily.get_daily_data(uid, gid, 'class.boss')
                task['count'] = Tool.to_int(count, 0)
            elif task['type'] == 3:
                count = Context.Daily.get_daily_data(uid, gid, 'class.bonus')
                task['count'] = Tool.to_int(count, 0)
            elif task['type'] == 11:
                count = Context.Daily.get_daily_data(uid, gid, 'win.chip')
                task['count'] = Tool.to_int(count, 0)
            elif task['type'] == 21:
                degree += task['degree']

            if 'count' in task and task['count'] >= task['total']:
                task['done'] = 1
                degree += task['degree']

        return degree


FishTask = FishTask()
