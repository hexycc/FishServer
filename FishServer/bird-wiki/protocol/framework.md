#### 消息定义

```
ID_REQ = 0x01000000        # 请求
ID_ACK = 0x02000000        # 应答
ID_NTF = 0x04000000        # 通知
ID_CMD = 0x08000000        # 命令

# 框架内部消息
ID_BASE_INNER_SYSTEM = 0x00001000
MSG_INNER_ROBOT_JOIN = (ID_BASE_INNER_SYSTEM + 0x01)           # 机器人加入
MSG_INNER_ROBOT_LEAVE = (ID_BASE_INNER_SYSTEM + 0x02)          # 机器人离开
MSG_INNER_BROKEN = (ID_BASE_INNER_SYSTEM + 0x03)               # 前端断线
MSG_INNER_BI_REPORT = (ID_BASE_INNER_SYSTEM + 0x07)            # 数据统计上报
MSG_INNER_SERVER_REGISTER = (ID_BASE_INNER_SYSTEM + 0x08)      # 服务器注册
ID_BASE_INNER_SYSTEM_END = 0x00001FFF

# 服务器与客户端框架消息
ID_BASE_OUTER_SYSTEM = 0x00008000

# 服务器与客户端逻辑消息
ID_BASE_OUTER_GAME = 0x00010000

# 系统消息
MSG_SYS_HOLD = (ID_BASE_OUTER_SYSTEM + 0x64)                   # 保持连接
MSG_SYS_USER_INFO = (ID_BASE_OUTER_SYSTEM + 0x65)              # 玩家信息
MSG_SYS_GAME_INFO = (ID_BASE_OUTER_SYSTEM + 0x66)              # 游戏数据
MSG_SYS_QUICK_START = (ID_BASE_OUTER_SYSTEM + 0x67)            # 快速开始
MSG_SYS_JOIN_TABLE = (ID_BASE_OUTER_SYSTEM + 0x68)             # 进入桌子
MSG_SYS_SIT_DOWN = (ID_BASE_OUTER_SYSTEM + 0x69)               # 坐下
MSG_SYS_READY = (ID_BASE_OUTER_SYSTEM + 0x6A)                  # 准备
MSG_SYS_CANCEL_READY = (ID_BASE_OUTER_SYSTEM + 0x6B)           # 取消准备
MSG_SYS_STAND_UP = (ID_BASE_OUTER_SYSTEM + 0x6C)               # 站起
MSG_SYS_LEAVE_TABLE = (ID_BASE_OUTER_SYSTEM + 0x6D)            # 离开桌子
MSG_SYS_VIEWER_JOIN_TABLE = (ID_BASE_OUTER_SYSTEM + 0x6E)      # 旁观者加入桌子
MSG_SYS_VIEWER_LEAVE_TABLE = (ID_BASE_OUTER_SYSTEM + 0x6F)     # 旁观者离开桌子
MSG_SYS_FORCE_QUIT = (ID_BASE_OUTER_SYSTEM + 0x70)             # 强制退出,游戏中
MSG_SYS_TABLE_EVENT = (ID_BASE_OUTER_SYSTEM + 0x71)            # table event
MSG_SYS_BROADCAST = (ID_BASE_OUTER_SYSTEM + 0x72)              # 广播消息
MSG_SYS_MULTIPLE_LOGIN = (ID_BASE_OUTER_SYSTEM + 0x73)         # 重复登陆
MSG_SYS_FLUSH = (ID_BASE_OUTER_SYSTEM + 0x74)                  # 前端刷新
MSG_SYS_TRUSTEE = (ID_BASE_OUTER_SYSTEM + 0x75)                # 托管
MSG_SYS_ENTER_ROOM = (ID_BASE_OUTER_SYSTEM + 0x76)             # 进入房间
MSG_SYS_LEAVE_ROOM = (ID_BASE_OUTER_SYSTEM + 0x77)             # 离开房间
MSG_SYS_ROOM_EVENT = (ID_BASE_OUTER_SYSTEM + 0x78)             # 房间事件
MSG_SYS_TIMEOUT = (ID_BASE_OUTER_SYSTEM + 0x79)                # 超时
MSG_SYS_ROOM_LIST = (ID_BASE_OUTER_SYSTEM + 0x7A)              # 房间列表
MSG_SYS_BENEFIT = (ID_BASE_OUTER_SYSTEM + 0x7B)                # 救济金
MSG_SYS_RECONNECT = (ID_BASE_OUTER_SYSTEM + 0x7C)              # 断线重连

MSG_SYS_SERVER_INFO = (ID_BASE_OUTER_SYSTEM + 0x83)            # 服务器信息
MSG_SYS_LED = (ID_BASE_OUTER_SYSTEM + 0x84)                    # led信息
MSG_SYS_SERVER_TIME = (ID_BASE_OUTER_SYSTEM + 0x85)            # 服务器毫秒时间戳
MSG_SYS_BIND_GAME = (ID_BASE_OUTER_SYSTEM + 0x86)              # 绑定游戏
MSG_SYS_RANK_LIST = (ID_BASE_OUTER_SYSTEM + 0x87)              # 获取排行榜
MSG_SYS_SIGN_IN = (ID_BASE_OUTER_SYSTEM + 0x88)                # 签到
MSG_SYS_CONFIG = (ID_BASE_OUTER_SYSTEM + 0x89)                 # 获取配置
MSG_SYS_PROPS_LIST = (ID_BASE_OUTER_SYSTEM + 0x8A)             # 道具列表(背包)
MSG_SYS_USE_PROPS = (ID_BASE_OUTER_SYSTEM + 0x8B)              # 使用道具
MSG_SYS_RAFFLE = (ID_BASE_OUTER_SYSTEM + 0x8C)                 # 抽奖
MSG_SYS_TASK_LIST = (ID_BASE_OUTER_SYSTEM + 0x8D)              # 每日任务
MSG_SYS_CONSUME_TASK = (ID_BASE_OUTER_SYSTEM + 0x8E)           # 领取任务
MSG_SYS_PRESENT = (ID_BASE_OUTER_SYSTEM + 0x8F)                # 赠送
MSG_SYS_INNER_BUY = (ID_BASE_OUTER_SYSTEM + 0x90)              # 内部购买(二级货币的消耗)
MSG_SYS_EXCHANGE = (ID_BASE_OUTER_SYSTEM + 0x91)               # 兑换(货币间兑换, 比如coupon兑换)
MSG_SYS_CONSUME_CDKEY = (ID_BASE_OUTER_SYSTEM + 0x92)          # 兑换码(比如活动送兑换码)
MSG_SYS_ACTIVITY_LIST = (ID_BASE_OUTER_SYSTEM + 0x93)          # 活动列表
MSG_SYS_CONSUME_ACTIVITY = (ID_BASE_OUTER_SYSTEM + 0x94)       # 领取活动
MSG_SYS_HISTORY = (ID_BASE_OUTER_SYSTEM + 0x95)                # 记录
MSG_SYS_SHARE_INFO = (ID_BASE_OUTER_SYSTEM + 0x96)             # 获取分享模块信息
MSG_SYS_SHARE = (ID_BASE_OUTER_SYSTEM + 0x97)                  # 分享
MSG_SYS_BIND_INVITER = (ID_BASE_OUTER_SYSTEM + 0x98)           # 绑定邀请人
MSG_SYS_INVITE_INFO = (ID_BASE_OUTER_SYSTEM + 0x99)            # 获取分享奖励信息(好友达成条件)
MSG_SYS_INVITE_REWARD = (ID_BASE_OUTER_SYSTEM + 0x9A)          # 领取分享奖励（好友达成条件）

MSG_SYS_GROUP_BUY_INFO = (ID_BASE_OUTER_SYSTEM + 0x9B)         # 获取团购信息
MSG_SYS_GROUP_BUY_REWARD = (ID_BASE_OUTER_SYSTEM + 0x9C)       # 获取团购奖励
MSG_SYS_MARK_STATE = (ID_BASE_OUTER_SYSTEM + 0x9D)             # 红点标记信息
MSG_SYS_UP_BARREL = (ID_BASE_OUTER_SYSTEM + 0x9E)              # 强化炮
MSG_SYS_RESOLVE_STONE = (ID_BASE_OUTER_SYSTEM + 0x9F)          # 分解强化石
MSG_SYS_POKE_MOLE = (ID_BASE_OUTER_SYSTEM + 0xA0)              # 打地鼠
MSG_SYS_POKE_MOLE_CHANGE = (ID_BASE_OUTER_SYSTEM + 0xA1)       # 打地鼠换场景
MSG_SYS_POKE_MOLE_INFO = (ID_BASE_OUTER_SYSTEM + 0xA2)         # 打地鼠信息
MSG_SYS_POKE_MOLE_OL = (ID_BASE_OUTER_SYSTEM + 0xA3)           # 在线人数
MSG_SYS_QUICK_TABLE_INFO = (ID_BASE_OUTER_SYSTEM + 0xA4)       # 获取桌子信息
MSG_SYS_SWITCH_INFO = (ID_BASE_OUTER_SYSTEM + 0xA5)            # 获取SDK信息

MSG_SYS_AWARD_LIST = (ID_BASE_OUTER_SYSTEM + 0xA6)             # 获取奖励列表
MSG_SYS_CONSUME_AWARD = (ID_BASE_OUTER_SYSTEM + 0xA7)          # 领取奖励

MSG_SYS_MATCH_ENTRY = (ID_BASE_OUTER_SYSTEM + 0x1F00)          # 比赛概览
MSG_SYS_MATCH_RESULT = (ID_BASE_OUTER_SYSTEM + 0x1F01)         # 比赛结算

# 小游戏消息区段
ID_BASE_MINI_GAME = 0x00020000
ID_BASE_MINI_GAME_END = 0x0002FFFF
```

#### 枚举定义

```
# 登陆
login_success = 0                    # 成功
login_failed_unknown = -1            # 未知错误
login_failed_low_version = -2        # client版本过低, 必须升级
login_failed_forbidden = -3          # 账号限制
login_failed_id = -4                 # 错误的user id
login_failed_key = -5                # 错误的session key
login_failed_multi = -6              # 多点登陆

# 加入桌子
join_table_success = 0               # 成功
join_table_reconnect = -1            # 断线重连
join_table_failed_unknown = -2       # 未知错误
join_table_failed_id = -3            # 错误的table id
join_table_failed_multi = -4         # 在其他桌子未离开
join_table_failed_getout = -5        # 上局逃跑，游戏未结束

# 旁观者加入桌子
viewer_join_table_success = 0            # 成功
viewer_join_table_failed_unknown = -1    # 未知错误
viewer_join_table_failed_id = -2         # 错误的table id
viewer_join_table_failed_multi = -3      # 在其他桌子未离开

# 离开桌子
leave_table_success = 0                  # 成功
leave_table_failed_unknown = -1          # 未知错误
leave_table_failed_id = -2               # 错误的table id
leave_table_failed_playing = -3          # 游戏中

# 强制退出
force_quit_success = 0                   # 成功
force_quit_failed_unknown = -1           # 未知错误
force_quit_failed_id = -2                # 错误的table id

# 旁观者退出
viewer_leave_table_success = 0           # 成功
viewer_leave_table_failed_unknown = -1   # 未知错误
viewer_leave_table_failed_id = -2        # 错误的table id

# 广播
broadcast_success = 0                    # 成功
broadcast_failed_unknown = -1            # 未知错误
broadcast_failed_id = -2                 # 错误的table id

# 刷新
flush_success = 0                        # 成功
flush_failed_unknown = -1                # 未知错误
flush_failed_id = -2                     # 错误的table id

# 托管
trustee_success = 0                      # 成功
trustee_failed_unknown = -1              # 未知错误
trustee_failed_id = -2                   # 错误的table id

# 超时
timeout_success = 0                      # 成功
timeout_failed_unknown = -1              # 未知错误
timeout_failed_id = -2                   # 错误的table id

# 坐下
sit_down_success = 0                     # 成功
sit_down_failed_unknown = -1             # 未知错误
sit_down_failed_id = -2                  # 错误的table id

# 准备
ready_success = 0                        # 成功
ready_failed_unknown = -1                # 未知错误
ready_failed_id = -2                     # 错误的table id

# 快速开始
quick_start_success = 0
quick_start_failed_unknown = -1
quick_start_failed_chip_small = -2
quick_start_failed_chip_big = -3
quick_start_failed_multi = -4

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

# 玩家身份
identity_type_unknown = 0
identity_type_player = 1
identity_type_viewer = 2
identity_type_robot = 3
```

#### 心跳

```
{
    "cmd": MSG_SYS_HOLD | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_HOLD | ID_ACK,
    "param": {
    }
}
```

#### 玩家信息

```
{
    "cmd": MSG_SYS_USER_INFO | ID_REQ,
    "param": {
        "userId": 9527,
        "gameId": 1,
        "session": "xxxxxxxx"
    }
}
```

```
{
    "cmd": MSG_SYS_USER_INFO | ID_ACK,
    "param": {
        "nick": "MI 4",
        "sex": 1,
        "avatar": "22",
    }
}
```

#### 游戏数据

```
{
    "cmd": MSG_SYS_GAME_INFO | ID_REQ,
    "param": {
        "gameId": 1
    }
}
```

```
{
    "cmd": MSG_SYS_GAME_INFO | ID_ACK,
    "param": {
        "exp": 1,
        "play": 1,
        "win": 1,
        "draw": 1,
        "lose": 1,
        "broken": 1,
        "getout": 1,
        // game own alone
    }
}
```

#### 快速开始

```
{
    "cmd": MSG_SYS_QUICK_START | ID_REQ,
    "param": {
        "gameId": 1，
        "roomType": 201     // 房间类型, 可以无
    }
}
```

```
{
    "cmd": MSG_SYS_QUICK_START | ID_ACK,
    "param": {
        "roomId": 101,
        "tableId": 1001,
        "seatId": 1,
    }
}
```

#### 加入桌子

```
{
    "cmd": MSG_SYS_JOIN_TABLE | ID_REQ,
    "param": {
        "gameId": 1,
        "roomId": 101,
        "tableId": 1001,     // 桌子id
        "seatId": 1,         // 如果发送就直接坐下, 否则需要单独发送sit请求
    }
}
```

```
{
    "cmd": MSG_SYS_JOIN_TABLE | ID_ACK,
    "param": {
    }
}
```

#### 坐下

```
{
    "cmd": MSG_SYS_SIT_DOWN | ID_REQ,
    "param": {
        "seatId": 1     // 座位id
    }
}
```

```
{
    "cmd": MSG_SYS_SIT_DOWN | ID_ACK,
    "param": {
    }
}
```

#### 准备

```
{
    "cmd": MSG_SYS_READY | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_READY | ID_ACK,
    "param": {
    }
}
```

#### 取消准备

```
{
    "cmd": MSG_SYS_CANCEL_READY | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_CANCEL_READY | ID_ACK,
    "param": {
    }
}
```

#### 站起

```
{
    "cmd": MSG_SYS_STAND_UP | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_STAND_UP | ID_ACK,
    "param": {
    }
}
```

#### 离开桌子

```
{
    "cmd": MSG_SYS_LEAVE_TABLE | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_LEAVE_TABLE | ID_ACK,
    "param": {
    }
}
```

#### 旁观者加入桌子

```
{
    "cmd": MSG_SYS_VIEWER_JOIN_TABLE | ID_REQ,
    "param": {
        "gameId": 1,
        "roomId": 101,
        "tableId": 1001,     // 桌子id
        "seatId": 1          // 座位id
    }
}
```

```
{
    "cmd": MSG_SYS_VIEWER_JOIN_TABLE | ID_ACK,
    "param": {
    }
}
```

#### 旁观者离开桌子

```
{
    "cmd": MSG_SYS_VIEWER_LEAVE_TABLE | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_VIEWER_LEAVE_TABLE | ID_ACK,
    "param": {
    }
}
```

#### 游戏中强制退出

```
{
    "cmd": MSG_SYS_FORCE_QUIT | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_FORCE_QUIT | ID_ACK,
    "param": {
    }
}
```

#### table event

```
{
    "cmd": MSG_SYS_TABLE_EVENT | ID_NTF,
    "param": {
        "event": [{}...]
    }
}
```

```
// table_event_join_table
{
    "type": table_event_join_table,
    "userId": 20002
}

// table_event_sit_down
{
    "type": table_event_sit_down,
    "userId": 20002,
    "seatId": 1
}

// table_event_leave_table
{
    "type": table_event_leave_table,
    "userId": 20002
}

// table_event_offline
{
    "type": table_event_offline,
    "userId": 20002
}

// table_event_game_info
{
    "type": table_event_game_info,
    "userId": 20002,
    "gameInfo": {
        //same to game_info ack
    }
}

// table_event_user_info
{
    "type": table_event_user_info,
    "userId": 20002,
    "userInfo": {
        //same to user_info ack
    }
}

// table_event_table_info
{
    "type": table_event_table_info,
    "tableInfo": {
        {
            "userId": 20005,
            "identity": identity_type_player,
            "state": user_state_playing,
            "seatId": 1                     // 如果没坐下没有该字段
        },
        // ...
    }
}
```

```
// join_table 通知加入者桌面信息及其他人信息
{
    "cmd": MSG_SYS_TABLE_EVENT | ID_NTF,
    "param": {
        "event": [
            // table_event_table_info
            // table_event_user_info
            // table_event_game_info
            // other table_event_user_info and table_event_game_info
        ]
    }
}
```

```
// join_table 通知所有人(包括自己)加入及信息
{
    "cmd": MSG_SYS_TABLE_EVENT | ID_NTF,
    "param": {
        "event": [
            // table_event_join_table
            // table_event_user_info
            // table_event_game_info
        ]
    }
}
```

```
// sit_down 通知所有人(包括自己)坐下
{
    "cmd": MSG_SYS_TABLE_EVENT | ID_NTF,
    "param": {
        "event": [
            // table_event_sit_down
        ]
    }
}
```

```
// leave 通知其他人(不包括自己)离开
{
    "cmd": MSG_SYS_TABLE_EVENT | ID_NTF,
    "param": {
        "event": [
            // table_event_leave_table
        ]
    }
}
```

```
// offline 通知其他人(不包括自己)断线
{
    "cmd": MSG_SYS_TABLE_EVENT | ID_NTF,
    "param": {
        "event": [
            // table_event_offline
        ]
    }
}
```

#### 广播消息

```
{
    "cmd": MSG_SYS_BROADCAST | ID_REQ,
    "param": {
        // 消息内容客户端自定义
    }
}
```

```
{
    "cmd": MSG_SYS_BROADCAST | ID_ACK,
    "param": {
        // 消息内容客户端自定义
    }
}
```

#### 重复登陆

```
{
    "cmd": MSG_SYS_MULTIPLE_LOGIN | ID_NTF,
    "param": {
    }
}
```

#### 托管

```
{
    "cmd": MSG_SYS_TRUSTEE | ID_REQ,
    "param": {
        "trustee": 0    // 0为取消托管， 1为进入托管
    }
}
```

```
{
    "cmd": MSG_SYS_TRUSTEE | ID_ACK,
    "param": {
    }
}
```

#### 进入房间

```
{
    "cmd": MSG_SYS_ENTER_ROOM | ID_REQ,
    "param": {
        "roomId": 100
    }
}
```

#### 离开房间

```
{
    "cmd": MSG_SYS_LEAVE_ROOM | ID_REQ,
    "param": {
        "roomId": 100
    }
}
```

#### 房间事件

```
{
    "cmd": MSG_SYS_ROOM_EVENT | ID_NTF,
    "param": {
        "event": [{}...]
    }
}
```

#### 超时

```
{
    "cmd": MSG_SYS_TIMEOUT | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_TIMEOUT | ID_ACK,
    "param": {
    }
}
```

#### 房间列表

```
{
    "cmd": MSG_SYS_ROOM_LIST | ID_REQ,
    "param": {
        "gameId": 1,
        "match": 1          // 需要比赛信息, 发此字段
    }
}
```

```
{
    "cmd": MSG_SYS_ROOM_LIST | ID_ACK,
    "param": {
        "room_list": [
            {
                "room_type": 201,
                "room_name": "新手场",
                "room_fee": 0,
                "base_point": 10,
                "chip_min": 1000,
                "chip_max": 100000,
            },
            // ...
            {
                "room_type": 211,
                "room_name": "大奖赛",
                "room_fee": 0,
                "base_point": 10,
                "chip_min": 1000,
                "chip_max": 100000,
            }
        ]
    }
}
```

#### 救济金

```
{
    "cmd": MSG_SYS_BENEFIT | ID_NTF,
    "param": {
        "which": 1,
        "total": 3,
        "reward": 1000,
        "chip": 99990
    }
}
```

#### 服务器信息

```
{
    "cmd": MSG_SYS_SERVER_INFO | ID_REQ,
    "param": {
        "gameId": 1
    }
}
```

```
{
    "cmd": MSG_SYS_SERVER_INFO | ID_ACK,
    "param": {
        "gameId": 1,
        "online": 10000,        // 在线人数
        "list": [[201, 100], [202, 500], [203, 600]]
    }
}
```

#### led信息

```
{
    "cmd": MSG_SYS_LED | ID_REQ,
    "param": {
        "gameId": 1，
        "last_ts": 1448102068   // 接受到的最后一条led的时间, 可以没有
    }
}
```

```
{
    "cmd": MSG_SYS_LED | ID_ACK,
    "param": {
        "global": {"ts": 1333333333, "list": ["我是led"]}，
        "game": {"ts": 1333333333, "list": ["我是led"]}
    }
}
```

```
{
    "cmd": MSG_SYS_LED | ID_NTF,
    "param": {
        "global": {"ts": 1333333333, "list": ["我是led"]}，
        "game": {"ts": 1333333333, "list": ["我是led"]}
    }
}
```

#### 服务器时间

```
{
    "cmd": MSG_SYS_SERVER_TIME | ID_REQ,
    "param": {
        "ts": 1448267793206     // 客户端毫秒时间戳
    }
}
```

```
{
    "cmd": MSG_SYS_SERVER_TIME | ID_ACK,
    "param": {
        "cts": 1448267793206     // 客户端毫秒时间戳
        "sts": 1448267793308     // 服务器毫秒时间戳
    }
}
```

#### 绑定游戏

```
{
    "cmd": MSG_SYS_BIND_GAME | ID_REQ,
    "param": {
        "gameId": 2     // 客户端切换游戏
    }
}
```

```
{
    "cmd": MSG_SYS_BIND_GAME | ID_ACK,
    "param": {
        "gameId": 2
    }
}
```
