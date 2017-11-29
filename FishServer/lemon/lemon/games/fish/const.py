#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-23

from framework.entity import const


class Message(const.Message):
    FISH_MSG_BOARD_INFO = const.Message.ID_BASE_OUTER_GAME + 0x01            # 桌面信息, 游戏初始化数据
    FISH_MSG_SHOT_BULLET = const.Message.ID_BASE_OUTER_GAME + 0x02           # 玩家射击
    FISH_MSG_NEXT_SCENE = const.Message.ID_BASE_OUTER_GAME + 0x03            # 下一个场景
    FISH_MSG_HIT_FISH = const.Message.ID_BASE_OUTER_GAME + 0x04              # 玩家炮弹击中鱼
    FISH_MSG_MOVE_BARREL = const.Message.ID_BASE_OUTER_GAME + 0x05           # 玩家移动炮筒
    FISH_MSG_SWITCH_BARREL = const.Message.ID_BASE_OUTER_GAME + 0x06         # 改变炮筒
    FISH_MSG_SKILL_SUPER_WEAPON = const.Message.ID_BASE_OUTER_GAME + 0x07    # 超级武器
    FISH_MSG_UNLOCK_BARREL = const.Message.ID_BASE_OUTER_GAME + 0x08         # 解锁炮筒
    FISH_MSG_SKILL_LOCK = const.Message.ID_BASE_OUTER_GAME + 0x09            # 锁定攻击
    FISH_MSG_CATCH_FISH = const.Message.ID_BASE_OUTER_GAME + 0x0A            # 玩家捕获鱼
    FISH_MSG_SKILL_VIOLENT = const.Message.ID_BASE_OUTER_GAME + 0x0B         # 狂暴
    FISH_MSG_EXP_UPGRADE = const.Message.ID_BASE_OUTER_GAME + 0x0C           # exp等级升级
    FISH_MSG_SKILL_FREEZE = const.Message.ID_BASE_OUTER_GAME + 0x0D          # 冰冻
    FISH_MSG_LOCK_FISH = const.Message.ID_BASE_OUTER_GAME + 0x0E             # 锁定攻击
    FISH_MSG_REPORT_FISHS = const.Message.ID_BASE_OUTER_GAME + 0x0F          # 上报辐射到的鱼
    FISH_MSG_SKILL_PORTAL = const.Message.ID_BASE_OUTER_GAME + 0x10          # 神秘传送门
    FISH_MSG_DELTA_SCENE = const.Message.ID_BASE_OUTER_GAME + 0x11           # 场景增量内容
    FISH_MSG_BANKRUPT = const.Message.ID_BASE_OUTER_GAME + 0x12              # 破产
    # FISH_MSG_LED = const.Message.ID_BASE_OUTER_GAME + 0x23                   # 游戏内广播
    # FISH_MSG_CALL_FISH = const.Message.ID_BASE_OUTER_GAME + 0x24             # 召唤鱼
    # FISH_MSG_FISH_ATTACK = const.Message.ID_BASE_OUTER_GAME + 0x25           # 小红鱼攻击
    # FISH_MSG_RED_DRAGON_END = const.Message.ID_BASE_OUTER_GAME + 0x26        # 红鱼任务结束
    # FISH_MSG_RANK_CHANGE = const.Message.ID_BASE_OUTER_GAME + 0x27           # 赏金任务信息变化
    # FISH_MSG_BOUNTY_END = const.Message.ID_BASE_OUTER_GAME + 0x28            # 赏金任务结束


class Enum(const.Enum):
    join_table_failed_error_state = 1                # 错误的状态
    join_table_failed_already_full = 2               # 人数已满
    join_table_failed_already_join = 3               # 该用户已经加入table
    join_table_failed_limit_min = 4                  # 低于最低限制
    join_table_failed_limit_max = 5                  # 高于最高限制

    sit_down_failed_error_state = 1                  # 错误的状态
    sit_down_failed_error_seat_id = 2                # 错误的seat id
    sit_down_failed_error_not_join = 3               # 用户不在桌子中
    sit_down_failed_error_identity = 4               # 用户身份错误
    sit_down_failed_not_free = 5                     # 不是free状态
    sit_down_failed_other_here = 6                   # 座位已经有人

    ready_failed_error_state = 1                     # 错误的状态
    ready_failed_error_not_join = 2                  # 用户不在桌子中
    ready_failed_error_identity = 3                  # 用户身份错误
    ready_failed_not_sit_down = 6                    # 该用户没有坐下

    leave_table_failed_not_join = 1                  # 没有加入
    leave_table_failed_error_identity = 2            # 错误的身份

    kick_reason_unknown = 0                          # 未知
    kick_reason_no_ready = 2                         # 指定时间内不ready
    kick_reason_limit_min = 3                        # 低于最低限制
    kick_reason_limit_max = 4                        # 高于最高限制

    quick_start_failed_barrel_small = 1
    quick_start_failed_barrel_big = 2
    quick_start_failed_diamond_lack = 3
    quick_start_failed_match_free = 4
    quick_start_failed_match_end = 5
    quick_start_failed_match_limit = 6

    task_state_free = 0
    task_state_pre = 1
    task_state_ing = 2
    task_state_clear = 3

    play_mode_common = 1                             # 不带红龙和悬赏任务
    play_mode_task = 2                               # 带红龙和悬赏任务
