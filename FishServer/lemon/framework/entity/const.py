#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-07-23


class Message(object):
    INNER_FLAG = 0x10000000    # 服务器内部消息标识
    MSG_MASK = 0x0FFFFFFF

    ID_REQ = 0x01000000        # 请求
    ID_ACK = 0x02000000        # 应答
    ID_NTF = 0x04000000        # 通知

    # 框架内部消息
    ID_BASE_INNER_SYSTEM = 0x00001000
    MSG_INNER_BROKEN = (ID_BASE_INNER_SYSTEM + 0x01)               # 前端断线
    ID_BASE_INNER_SYSTEM_END = 0x00001FFF

    # 游戏内部消息
    ID_BASE_INNER_GAME = 0x00002000
    MSG_INNER_TIMER = (ID_BASE_INNER_GAME + 0x01)                  # 定时器
    ID_BASE_INNER_GAME_END = 0x00002FFF

    # 服务器与客户端框架消息
    ID_BASE_OUTER_SYSTEM = 0x00004000
    ID_BASE_OUTER_SYSTEM_END = 0x00004FFF

    MSG_SYS_QUICK_START = (ID_BASE_OUTER_SYSTEM + 0x01)            # 快速开始
    MSG_SYS_JOIN_TABLE = (ID_BASE_OUTER_SYSTEM + 0x02)             # 进入桌子
    MSG_SYS_SIT_DOWN = (ID_BASE_OUTER_SYSTEM + 0x03)               # 坐下
    MSG_SYS_LEAVE_TABLE = (ID_BASE_OUTER_SYSTEM + 0x04)            # 离开桌子
    MSG_SYS_TABLE_EVENT = (ID_BASE_OUTER_SYSTEM + 0x05)            # table event
    MSG_SYS_HOLD = (ID_BASE_OUTER_SYSTEM + 0x11)                   # 保持连接
    MSG_SYS_MULTIPLE_LOGIN = (ID_BASE_OUTER_SYSTEM + 0x12)         # 重复登陆
    MSG_SYS_USER_INFO = (ID_BASE_OUTER_SYSTEM + 0x13)              # 玩家信息
    MSG_SYS_GAME_INFO = (ID_BASE_OUTER_SYSTEM + 0x14)              # 游戏数据
    MSG_SYS_ROOM_LIST = (ID_BASE_OUTER_SYSTEM + 0x15)              # 房间列表
    MSG_SYS_BIND_GAME = (ID_BASE_OUTER_SYSTEM + 0x16)              # 绑定游戏
    MSG_SYS_BENEFIT = (ID_BASE_OUTER_SYSTEM + 0x17)                # 救济金
    MSG_SYS_SERVER_INFO = (ID_BASE_OUTER_SYSTEM + 0x18)            # 服务器信息
    MSG_SYS_RANK_LIST = (ID_BASE_OUTER_SYSTEM + 0x19)              # 获取排行榜
    MSG_SYS_LED = (ID_BASE_OUTER_SYSTEM + 0x1A)                    # led信息
    MSG_SYS_RAFFLE = (ID_BASE_OUTER_SYSTEM + 0x1B)                 # 抽奖
    MSG_SYS_SIGN_IN = (ID_BASE_OUTER_SYSTEM + 0x1C)                # 签到
    MSG_SYS_PROPS_LIST = (ID_BASE_OUTER_SYSTEM + 0x1D)             # 道具列表(背包)
    MSG_SYS_USE_PROPS = (ID_BASE_OUTER_SYSTEM + 0x1E)              # 使用道具
    MSG_SYS_TASK_LIST = (ID_BASE_OUTER_SYSTEM + 0x1F)              # 每日任务
    MSG_SYS_PRESENT = (ID_BASE_OUTER_SYSTEM + 0x20)                # 赠送
    MSG_SYS_INNER_BUY = (ID_BASE_OUTER_SYSTEM + 0x21)              # 内部购买(二级货币的消耗)
    MSG_SYS_CONFIG = (ID_BASE_OUTER_SYSTEM + 0x22)                 # 获取配置
    MSG_SYS_EXCHANGE = (ID_BASE_OUTER_SYSTEM + 0x23)               # 兑换(货币间兑换, 比如coupon兑换)
    MSG_SYS_CONSUME_TASK = (ID_BASE_OUTER_SYSTEM + 0x24)           # 领取任务
    MSG_SYS_UP_BARREL = (ID_BASE_OUTER_SYSTEM + 0x25)              # 强化炮
    MSG_SYS_RESOLVE_STONE = (ID_BASE_OUTER_SYSTEM + 0x26)          # 分解强化石
    MSG_SYS_CONSUME_CDKEY = (ID_BASE_OUTER_SYSTEM + 0x27)

    # 服务器与客户端逻辑消息
    ID_BASE_OUTER_GAME = 0x00008000
    ID_BASE_OUTER_GAME_END = 0x00008FFF

    @classmethod
    def to_inner(cls, cmd):
        return cmd | cls.INNER_FLAG

    @classmethod
    def to_outer(cls, cmd):
        return cmd & cls.MSG_MASK

    @classmethod
    def is_inner(cls, cmd):
        return bool(cmd & cls.INNER_FLAG)

    @classmethod
    def is_game_server(cls, cmd):
        # 游戏逻辑
        cmd &= 0xF0FFFFFF
        if cls.ID_BASE_OUTER_GAME < cmd < cls.ID_BASE_OUTER_GAME_END:
            return True
        # 游戏框架
        if cls.MSG_SYS_JOIN_TABLE <= cmd <= cls.MSG_SYS_TABLE_EVENT:
            return True
        return False


class FlagType(object):
    flag_type_game = 1
    flag_type_connect = 2
    flag_type_quick = 3
    flag_type_entity = 4
    flag_type_sdk = 5
    flag_type_http = 6
    flag_type_shell = 7

    __cache_map = {}

    @classmethod
    def trans_server_type(cls, server_type):
        if not cls.__cache_map:
            cls.__make_cache()
        return cls.__cache_map.get(server_type, None)

    @classmethod
    def __make_cache(cls):
        for attr, v in cls.__dict__.iteritems():
            if attr.startswith('flag_type_'):
                cls.__cache_map[attr[len('flag_type_'):]] = v
                cls.__cache_map[v] = attr[len('flag_type_'):]


class Const(object):
    chip_operate_noop = 0
    chip_operate_zero = 1

    run_mode_online = 1
    run_mode_rc = 2
    run_mode_test = 3

    data_type_str = 0
    data_type_json = 1
    data_type_int = 2
    data_type_float = 3


class Enum(object):
    # 登陆
    login_success = 0                    # 成功
    login_failed_unknown = -1            # 未知错误
    login_failed_low_version = -2        # client版本过低, 必须升级
    login_failed_forbidden = -3          # 账号封停
    login_failed_freeze = -4             # 账号冻结
    login_failed_id = -5                 # 错误的user id
    login_failed_key = -6                # 错误的session key
    login_failed_multi = -7              # 多点登陆

    # 加入桌子
    join_table_success = 0               # 成功
    join_table_reconnect = -1            # 断线重连
    join_table_failed_unknown = -2       # 未知错误
    join_table_failed_id = -3            # 错误的table id
    join_table_failed_multi = -4         # 在其他桌子未离开
    join_table_failed_getout = -5        # 上局逃跑，游戏未结束

    # 离开桌子
    leave_table_success = 0                  # 成功
    leave_table_failed_unknown = -1          # 未知错误
    leave_table_failed_id = -2               # 错误的table id
    leave_table_failed_playing = -3          # 游戏中

    # 坐下
    sit_down_success = 0                     # 成功
    sit_down_failed_unknown = -1             # 未知错误
    sit_down_failed_id = -2                  # 错误的table id

    # 快速开始
    quick_start_success = 0
    quick_start_failed_unknown = -1
    quick_start_failed_chip_small = -2
    quick_start_failed_chip_big = -3
    quick_start_failed_multi = -4

    # 重连
    reconnect_success = 0
    reconnect_failed_unknown = -1
    reconnect_failed_id = -2
    reconnect_failed_state = -3

    # 桌子事件
    table_event_login = 0                        # 玩家登陆
    table_event_join_table = 1                   # 玩家加入桌子
    table_event_sit_down = 2                     # 玩家坐下
    table_event_stand_up = 3                     # 玩家站起
    table_event_ready = 4                        # 玩家ready
    table_event_cancel_ready = 5                 # 玩家取消ready
    table_event_leave_table = 6                  # 玩家离开桌子
    table_event_force_quit = 7                   # 玩家强退
    table_event_viewer_join_table = 8            # 旁观者进入
    table_event_viewer_leave_table = 9           # 旁观者退出
    table_event_kick_off = 10                    # 玩家被踢出
    table_event_offline = 11                     # 玩家断线
    table_event_reconnect = 12                   # 断线重连
    table_event_game_start = 13                  # 游戏开始
    table_event_game_end = 14                    # 游戏结束
    table_event_game_info = 15                   # 玩家gameinfo改变
    table_event_user_info = 16                   # 玩家userinfo改变
    table_event_table_info = 17                  # tableinfo改变
    table_event_broadcast = 18                   # 广播
    table_event_trustee = 19                     # 托管
    table_event_cancel_trustee = 20              # 取消托管

    # 玩家状态
    user_state_unknown = 0            # 未知
    user_state_getout = 1             # 离开了
    user_state_free = 2               # 在房间站立
    user_state_sit = 3                # 坐在椅子上
    user_state_ready = 4              # 同意游戏开始
    user_state_playing = 5            # 正在玩
    user_state_offline = 6            # 断线等待续玩
    user_state_lookon = 7             # 旁观
    user_state_trustee = 8            # 托管
    user_state_wait = 9               # 等待
    user_state_lose = 10              # 已经输了

    # 玩家身份
    identity_type_unknown = 0
    identity_type_player = 1
    identity_type_viewer = 2
    identity_type_robot = 3
