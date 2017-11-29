#### 捕鸟消息

```
BIRD_MSG_BOARD_INFO = const.Message.ID_BASE_OUTER_GAME + 0x01            # 桌面信息, 游戏初始化数据
BIRD_MSG_SHOT_BULLET = const.Message.ID_BASE_OUTER_GAME + 0x02           # 玩家射击
BIRD_MSG_MOVE_BARREL = const.Message.ID_BASE_OUTER_GAME + 0x03           # 玩家移动炮筒
BIRD_MSG_HIT_BIRD = const.Message.ID_BASE_OUTER_GAME + 0x04              # 玩家炮弹击中鸟
BIRD_MSG_CATCH_BIRD = const.Message.ID_BASE_OUTER_GAME + 0x05            # 玩家捕获鸟
BIRD_MSG_NEXT_SCENE = const.Message.ID_BASE_OUTER_GAME + 0x06            # 下一个场景
BIRD_MSG_UNLOCK_BARREL = const.Message.ID_BASE_OUTER_GAME + 0x07         # 解锁炮筒
BIRD_MSG_SWITCH_BARREL = const.Message.ID_BASE_OUTER_GAME + 0x08         # 改变炮筒
BIRD_MSG_SKILL_LOCK = const.Message.ID_BASE_OUTER_GAME + 0x09            # 锁定攻击
BIRD_MSG_SKILL_FREEZE = const.Message.ID_BASE_OUTER_GAME + 0x0A          # 冰冻
BIRD_MSG_SKILL_VIOLENT = const.Message.ID_BASE_OUTER_GAME + 0x0B         # 狂暴
BIRD_MSG_SKILL_SUPER_WEAPON = const.Message.ID_BASE_OUTER_GAME + 0x0C    # 超级武器
BIRD_MSG_SKILL_PORTAL = const.Message.ID_BASE_OUTER_GAME + 0x0D          # 神秘传送门
BIRD_MSG_LOCK_BIRD = const.Message.ID_BASE_OUTER_GAME + 0x15             # 锁定攻击
BIRD_MSG_EXP_UPGRADE = const.Message.ID_BASE_OUTER_GAME + 0x1F           # exp等级升级
BIRD_MSG_DELTA_SCENE = const.Message.ID_BASE_OUTER_GAME + 0x20           # 场景增量内容
BIRD_MSG_BANKRUPT = const.Message.ID_BASE_OUTER_GAME + 0x21              # 破产
BIRD_MSG_REPORT_BIRDS = const.Message.ID_BASE_OUTER_GAME + 0x22          # 上报辐射到的鸟
BIRD_MSG_LED = const.Message.ID_BASE_OUTER_GAME + 0x23                   # 游戏内广播
BIRD_MSG_CALL_BIRD = const.Message.ID_BASE_OUTER_GAME + 0x24             # 召唤鸟
BIRD_MSG_BIRD_ATTACK = const.Message.ID_BASE_OUTER_GAME + 0x25           # 小红鸟攻击
BIRD_MSG_RED_DRAGON_END = const.Message.ID_BASE_OUTER_GAME + 0x26        # 红鸟任务结束
BIRD_MSG_RANK_CHANGE = const.Message.ID_BASE_OUTER_GAME + 0x27           # 赏金任务信息变化
BIRD_MSG_BOUNTY_END = const.Message.ID_BASE_OUTER_GAME + 0x28            # 赏金任务结束
```

#### 用户信息

```
{
    "cmd": MSG_SYS_GAME_INFO | ID_REQ,
    "param": {
        "gameId": 2
    }
}
```

```
{
    "cmd": MSG_SYS_GAME_INFO | ID_ACK,
    "param": {
        "chip": 55555,
        "diamond": 565,
        "exp": 1,
        "play": 1,
        "broken": 1,
        'barrel_level': 1,
        'skin_level': 1,
        "vip": 2,        // vip等级, 不是vip没有此字段
        "login": {
            "done": 1,   // 已领取, 未领取没有次字段
            "which": 2,  // 从0开始计数, 比如是2表示已经连续领取2天, 应该领取第3天
            "conf": [1000, 2000, 3000, 4000, 5000, 8000, 10000],
        },
        "exp_level": 2,  // exp等级
        "exp_diff": [5, 20],    // 当前级别和下一级别临界值(exp最高级时不发此字段)
        "card": {            // 非月卡用户无此字段
            "state": 1,      // 0表示未领取
            "left": 0        // 为剩余天数(不包含今天)
        },
        "activity": {
            "ver": 1,
            "tip": "有新活动啦! 快来参加吧",
            "list": [
                "你捕鸟我送礼",
                "新手保送100级"
            ]
        }
    }
}
```

#### 桌面信息

玩家进入桌子会请求桌面信息, 消息包含了地图数据, 桌面场景...

```
{
    "cmd": BIRD_MSG_BOARD_INFO | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": BIRD_MSG_BOARD_INFO | ID_ACK,
    "param": {
        "start": 1448267793206,     // 地图开始毫秒时间
        "end": 1448267993206,       // 地图结束毫秒时间
        "uptime": 555556,           // 距离start的毫秒间隔, 即已运行时间毫秒数
        "freeze": {
            "total": 111111,        // 已经完成的冰冻总时间
            "start": 454545,        // 还在进行中的冰冻开始时间(相对于场景start)
        },
        "board": [                  // 桌面数据
            {
                "u": 200001,   // 用户uid
                "a": 52,       // 炮筒角度
                "b": 12,       // 炮弹计数器
                "mt": 1,       // 炮筒倍数
                "lv": 2,       // 炮筒等级
                "s": 1511,     // 比赛: 积分
                "l": 111,      // 比赛：剩余子弹数
                "around": [    // 红龙任务周围鸟
                    {
                        "l": 0,
                        "i": 111,
                        "t": 302
                    }
                    // ...
                ],
                "prey": [[104, 2], [105, 2]]
            }
            // other用户
        ],
        "ranks": [20001, 20002],
        "map": {                    // 地图数据
            "img": "1",             // 背景图片
            "next_img": "2",        // 下一个场景图片
            "birds": [
                {
                    "t": 1,                              // 鸟的类型
                    "i": 9527,                           // 鸟的id
                    "n": 555560,                         // 鸟出现时间,距离开始时间
                    "s": 15,                             // 生存时间
                    "p": [1, x1, y1, x2, y2 ...]         // 轨迹类型, 轨迹关键点
                }
            ],
            "tide": {
                "type": 4,
                "info": [{"id":182,"type":101}, {"id":192,"type":102}],
                "in": 900,
                "show": 60,
                "img": "4"
            },
            "bounty": {
                "in": 600,
                "show": 180,
                "info": [[104, 2], [106, 2], [176, 1]]
            },
            "events": [
                {
                    "in": 1111,       // 出现时间
                    "type": 1,        // 类型(1:boss 2:鸟潮 3:特殊)
                    "show": 30        // 持续时间
                }
                // ....
            ]
        },
    }
}
```

```
{
    "cmd": BIRD_MSG_BOARD_INFO | ID_NTF,
    "param": {
        "start": 1448267793206,     // 地图开始毫秒时间
        "end": 1448267993206,       // 地图结束毫秒时间
        "uptime": 555556,           // 距离start的毫秒间隔, 即已运行时间毫秒数
        "board": [                  // 桌面数据
            {
                "u": 200001,   // 用户uid
                "a": 52,       // 炮筒角度
                "b": 12,       // 炮弹计数器
                "mt": 1,       // 炮筒倍数
                "lv": 2,       // 炮筒等级
            }
            // other用户
        ]
    }
}
```

#### 玩家射击

```
{
    "cmd": BIRD_MSG_SHOT_BULLET | ID_REQ,
    "param": {
        "b: 1110,                   // 子弹编号, 自己的子弹编号递增
        "a": 56,                    // 角度, 变化就发
    }
}
```

```
{
    "cmd": BIRD_MSG_SHOT_BULLET | ID_NTF,
    "param": {
        "u": 9527,             // 子弹射击者
        "b": 1110,             // 子弹编号, 自己的子弹编号递增
        "a": 56,               // 角度, 变化就发
        //"t": 1200,             // 地图开始时间到目前的毫秒数
        "c": 10000,            // 该玩家剩余金币数
        "l": 110,              // 比赛: 还剩子弹数量
    }
}
```

#### 玩家移动炮筒

玩家改变炮筒方向的时候发送, 服务器只管最后角度, 中间可以由客户端自己做补间动画

```
{
    "cmd": BIRD_MSG_MOVE_BARREL | ID_REQ,
    "param": {
        "a": 52,                // 炮筒移动后角度
        // maybe some param to animation
    }
}
```

```
{
    "cmd": BIRD_MSG_MOVE_BARREL | ID_NTF,
    "param": {
        "u": 9527,
        "a": 52,                // 炮筒移动后角度
        // maybe some param to animation
    }
}
```

#### 炮弹击中鸟

当玩家判断自己发射的子弹碰撞到鸟后, 发送此消息给服务器, 服务器根据概率计算鸟是否被捕获

```
{
    "cmd": BIRD_MSG_HIT_BIRD | ID_REQ,
    "param": {
        "b": 1110,                // 子弹编号
        "i": 5241,                // 鸟编号
    }
}
```

```
{
    "cmd": BIRD_MSG_HIT_BIRD | ID_ACK,      // 特殊鸟击中的时候会回复, 客户端收到后发送BIRD_MSG_REPORT_BIRDS
    "param": {
        "i": 5241,
        "t": 12121
    }
}
```

```
{
    "cmd": BIRD_MSG_HIT_BIRD | ID_NTF,
    "param": {
        "u": 9527,
        "b": 1110,                // 子弹编号
        "i": 5241,                // 鸟编号
    }
}
```

#### 玩家捕获鸟

鸟被捕获, 捕获者玩家获得奖励, 其他玩家也需要播动画

```
{
    "cmd": BIRD_MSG_CATCH_BIRD | ID_NTF,   
    "param": {
        "u": 20005        // userId
        "i": 12,          // 始作俑鸟
        "c": 1111,        // 最终金币
        "o": 44,          // 最终奖券
        "d": 4444,        // 最终钻石
        "s": 1212,        // 比赛：当前比赛分数
        "r": [            // 挂的鸟
            {
                "i": 12,
                "w": {
                    "c": 9527,        // 金币
                    "d": 12,          // 钻石
                    "o": 11,          // 兑换券
                    "p": [[205, 2], [201, 1],      // 道具
                },
            }
            // other
        ],
    }
}
```

#### 下一个场景

```
{
    "cmd": BIRD_MSG_NEXT_SCENE | ID_NTF,
    "param": {
        "start": 1448267793206,     // 地图开始毫秒时间
        "end": 1448267993206,       // 地图结束毫秒时间
        "uptime": 555556,           // 距离start的毫秒间隔, 即已运行时间毫秒数
        "map": {                    // 地图数据
            "img": "1",             // 背景图片
            "next_img": "2",        // 下一个场景图片
            "birds": [
                {
                    "t": 1,                              // 鸟的类型
                    "i": 9527,                             // 鸟的id
                    "n": 555560,                           // 鸟出现时间,距离开始时间
                    "s": 15,                             // 生存时间
                    "p": [1, x1, y1, x2, y2 ...]           // 轨迹类型, 轨迹关键点
                }
            ],
            "events": []            // 和broad_info中相同
        }
    }
}
```

#### 解锁炮筒

```
{
    "cmd": BIRD_MSG_UNLOCK_BARREL | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": BIRD_MSG_UNLOCK_BARREL | ID_ACK,
    "param": {
        "lv": 2,           // now barrel level
        "c": 121211,
        "d": 8522,
        "w": {
            "c": 9527,
            // ...
        },
    }
}
```

#### 切换炮筒

```
{
    "cmd": BIRD_MSG_SWITCH_BARREL | ID_REQ,
    "param": {
        "da": 1,      // 1 or -1
        "si": 1,      // which skin
        "lv": 10      // which level
    }
}
```

```
{
    "cmd": BIRD_MSG_SWITCH_BARREL | ID_NTF,
    "param": {
        "u": 20005          // userId
        "lv": 2,            // which level
        "mt": 2,            // what multiple
        "si": 1             // which skin
    }
}
```

#### 技能: 锁定攻击

```
{
    "cmd": BIRD_MSG_SKILL_LOCK | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": BIRD_MSG_SKILL_LOCK | ID_NTF,
    "param": {
        "u": 20005        // userId
        "ts": 1212121,    // uptime of lock
        "lt": 111,
    }
}
```

```
{
    "cmd": BIRD_MSG_LOCK_BIRD | ID_REQ,
    "param": {
        "i": 12      // which bird to lock
    }
}
```

```
{
    "cmd": BIRD_MSG_LOCK_BIRD | ID_NTF,
    "param": {
        "u": 20005        // userId
        "i": 12,          // which bird to lock
        "ts": 111111,
    }
}
```

#### 技能: 冰冻

```
{
    "cmd": BIRD_MSG_SKILL_FREEZE | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": BIRD_MSG_SKILL_FREEZE | ID_NTF,
    "param": {
        "u": 20005            // userId
        "ts": 1212121,        // uptime of freeze
        "lt": 111,            // 剩余冰冻个数
    }
}
```

#### 技能: 超级武器

```
{
    "cmd": BIRD_MSG_SKILL_SUPER_WEAPON | ID_REQ,
    "param": {
        "birds": [12, 15, 18...],       // 爆炸范围的鸟
        "pt": [x, y],                   // 炸弹放置位置
    }
}
```

```
{
    "cmd": BIRD_MSG_SKILL_SUPER_WEAPON | ID_NTF,
    "param": {
        "u": 20005        // userId
        "pt": [x, y],         // 炸弹放置位置
        "r": [          // 挂的鸟
            {
                "i": 12,
                "w": {
                    "c": 9527,                  // 金币
                    "d": 12,                    // 钻石
                    "p": [[205,2],[201,1]],     // 道具
                    "o": 11,                    // 兑换券
                },
            }
            // other
        ],
        "ts": 12455,          // 时间
        "lt": 111,
        "c": 888888,          // 最终金币
    }
}
```

#### 技能: 狂暴

```
{
    "cmd": BIRD_MSG_SKILL_VIOLENT | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": BIRD_MSG_SKILL_VIOLENT | ID_NTF,
    "param": {
        "u": 20005        // userId
        "ts": 1212121,
        "lt": 111,
    }
}
```

#### 技能: 神秘传送门

```
{
    "cmd": BIRD_MSG_SKILL_PORTAL | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": BIRD_MSG_SKILL_PORTAL | ID_NTF,
    "param": {
        "u": 20005        // userId
        "bird": {
            "t": 1,                              // 鸟的类型
            "i": 9527,                           // 鸟的id
            "n": 555560,                         // 鸟出现时间,距离开始时间
            "s": 15,                             // 生存时间
            "p": [1, x1, y1, x2, y2 ...]         // 轨迹类型, 轨迹关键点}
        }
        "ts": 1212121,
        "lt": 111,
    }
}
```

#### 签到奖励

```
{
    "cmd": MSG_SYS_SIGN_IN | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_SIGN_IN | ID_ACK,
    "param": {
        "chip": 95278,              // final chip
        "reward": {"chip": 800},    // 奖励
    }
}
```

#### 获取配置

```
{
    "cmd": MSG_SYS_CONFIG | ID_REQ,
    "param": {
        "which": ["vip", "shop", "raffle", "props", "barrel", "exchange", "benefit", "html", "share", "group_buy", "match"]
    }
}
```

```
{
    "cmd": MSG_SYS_CONFIG | ID_ACK,
    "param": {
        "vip": [
            {"pay": 20, "desc": u"签到翻倍奖励"},
            {"pay": 200, "desc": u"开启超级武器技能"},
            {"pay": 500, "desc": u"开启狂暴技能"},
            {"pay": 1000, "desc": u"充值额外返利10%"},
            {"pay": 2000, "desc": u"开启寒冰陷阱技能"},
            {"pay": 5000, "desc": u"充值额外返利20%"},
            {"pay": 10000, "desc": u"提高击杀几率"},
        ],
        "shop": {
            "chip": [
                {
                    "price": 618,
                    "desc": {"display": "加赠25%", "addition": 772500, "amount": 3090000},
                    "first": 1,
                    "id": "QF00200106"
                },
                {
                    "price": 328,
                    "desc": {"display": "加赠20%", "addition": 328000, "amount": 1640000},
                    "first": 1,
                    "id": "QF00200105"
                },
                {
                    "price": 108,
                    "desc": {"display": "加赠15%", "addition": 81000, "amount": 540000},
                    "first": 1,
                    "id": "QF00200104"
                },
                {
                    "price": 50,
                    "desc": {"display": "加赠10%", "addition": 33750, "amount": 337500},
                    "first": 1,
                    "id": "QF00200103"
                },
                {
                    "price": 28,
                    "desc": {"display": "加赠5%", "addition": 7000, "amount": 140000},
                    "first": 1,
                    "id": "QF00200102"
                },
                {
                    "price": 12,
                    "desc": {"display": "加赠5%", "addition": 3600, "amount": 72000},
                    "first": 1,
                    "id": "QF00200101"
                }
            ],
            "diamond": [
                {
                    "price": 328,
                    "desc": {"amount": 4100},
                    "id": "QF00200115"
                },
                {
                    "price": 108,
                    "desc": {"amount": 1296},
                    "id": "QF00200114"
                },
                {
                    "price": 50,
                    "desc": {"amount": 575},
                    "id": "QF00200113"
                },
                {
                    "price": 28,
                    "desc": {"amount": 308},
                    "id": "QF00200112"
                },
                {
                    "price": 12,
                    "desc": {"amount": 120},
                    "id": "QF00200111"
                }
            ],
            "card": {
                "price": 28,
                "content": {
                    "chip": 20000,
                    "diamond": 20,
                    "props": [
                        {"id": 201, "count": 5},
                        {"id": 202, "count": 2}
                    ]
                },
                "id": "QF00200121"
            },
            "first": {
                "price": 1,
                "worth": 18,
                "content": {
                    "diamond": 100,
                    "chip": 20,
                    "props": [
                        {"id": 201, "count": 5},
                        {"id": 202, "count": 2}
                    ]
                }
            },
            "love": {
                "price": 10,
                "content": {
                    "chip": 60000,
                    "props": [
                        {"id": 201, "count": 10},
                        {"id": 202, "count": 5}
                    ]
                },
                "list": ["100646", "100647", "100648", "100649", "100650",
                         "100651", "100652", "100653", "100654", "100655"]
            },
            "group": [
                {
                    "price": 10,
                    "week": 1,
                    "content": {
                        "chip": 60000,
                        "props": [
                            {"id": 201, "count": 10},
                            {"id": 202, "count": 5}
                        ]
                    },
                    'id': "QF00200111",
                },
                ],
            }
        }
        "raffle": {
            "config": [
                {
                    "id": 1,
                    "name": "普通抽奖",
                    "limit": 0,
                    "reward": [
                        {"coupon": 5},
                        {"diamond": 10},
                        {"diamond": 5},
                        {"chip": 600},
                        {"chip": 300},
                        {"chip": 100}
                    ]
                },
                {
                    "id": 2,
                    "name": "青铜抽奖",
                    "limit": 20000,
                    "reward": [
                        {"coupon": 15},
                        {"diamond": 100},
                        {"diamond": 50},
                        {"chip": 50000},
                        {"chip": 24000},
                        {"chip": 8000}
                    ]
                },
                {
                    "id": 3,
                    "name": "白银抽奖",
                    "limit": 100000,
                    "reward": [
                        {"coupon": 30},
                        {"diamond": 200},
                        {"props": {"id": 212, "count": 1}},
                        {"chip": 250000},
                        {"chip": 120000},
                        {"chip": 40000}
                    ]
                },
                {
                    "id": 4,
                    "name": "黄金抽奖",
                    "limit": 200000,
                    "reward": [
                        {"coupon": 70},
                        {"diamond": 400},
                        {"props": {"id": 213, "count": 1}},
                        {"chip": 500000},
                        {"chip": 240000},
                        {"chip": 80000}
                    ]
                },
                {
                    "id": 5,
                    "name": "白金抽奖",
                    "limit": 400000,
                    "reward": [
                        {"coupon": 150},
                        {"diamond": 800},
                        {"props": {"id": 214, "count": 1}},
                        {"chip": 1000000},
                        {"chip": 480000},
                        {"chip": 160000}
                    ]
                },
                {
                    "id": 6,
                    "name": "至尊抽奖",
                    "limit": 1200000,
                    "reward": [
                        {"coupon": 450},
                        {"diamond": 2400},
                        {"props": {"id": 214, "count": 3}},
                        {"chip": 3000000},
                        {"chip": 1440000},
                        {"chip": 480000}
                    ]
                }
            ],
            "pool": 0,
            "progress": [0, 5]
        }
        "props": [
            {
                "id": 201,
                "diamond": 200,
                "count": 100,
                "present": {"pay": 200},
                "desc": "看到大鸟别犹豫，立即使用锁定技能！要不就被别人抢走了"
            },
            {
                "id": 202,
                "diamond": 200,
                "count": 40,
                "present": {"pay": 200},
                "desc": "什么！鸟要逃走了？赶快使用全屏冰冻，瞬间为你冰冻10秒"
            },
            {
                "id": 203,
                "diamond": 200,
                "count": 10,
                "present": {"pay": 200},
                "use": {"vip": 3},
                "buy": {"vip": 3},
                "desc": "使用狂暴技能，立即获得双倍击杀概率"
            },
            {
                "id": 204,
                "diamond": 200,
                "count": 1,
                "present": {"pay": 200},
                "use": {"vip": 2},
                "buy": {"vip": 2},
                "desc": "发射一颗威力强大的超级武器，记得对准鸟多的地方扔哦！(对BOSS无效)"
            },
            {
                "id": 205,
                "diamond": 200,
                "count": 100,
                "present": {"pay": 200},
                "desc": "快快使用传送门，传送出一只神秘奖金鸟吧"
            },
            {
                "id": 211,
                "content": {"chip": 150000},
                "present": {"pay": 200},
                "desc": "价值30元的铜蛋，使用后可获得150000金币，可转赠好友!"
            },
            {
                "id": 212,
                "content": {"chip": 250000},
                "present": {"pay": 200},
                "desc": "价值50元的银蛋，使用后可获得250000金币，可转赠好友!"
            },
            {
                "id": 213,
                "content": {"chip": 500000},
                "present": {"pay": 200},
                "desc": "价值100元的金蛋，使用后可获得500000金币，可转赠好友!"
            },
            {
                "id": 214,
                "content": {"chip": 1000000},
                "present": {"pay": 200},
                "desc": "价值200元的彩蛋，使用后可获得1000000金币，可转赠好友!"
            }
        ],
        "unlock": [
            {
                "level": 2,
                "multiple": 2,
                "diamond": 2,
                "reward": {"chip": 100}
            },
            {
                "level": 3,
                "multiple": 3,
                "diamond": 2,
                "reward": {"chip": 100}
            },
            {
                "level": 4,
                "multiple": 4,
                "diamond": 3,
                "reward": {"chip": 150}
            },
            {
                "level": 5,
                "multiple": 5,
                "diamond": 3,
                "reward": {"chip": 150}
            },
            {
                "level": 6,
                "multiple": 6,
                "diamond": 5,
                "reward": {"chip": 200}
            }
        ],
        "exchange": [
            {
                "type": "phone",
                "desc": "30元话费",
                "cost": 300,
                "count": 30
            },
            {
                "type": "diamond",
                "desc": "300钻石",
                "cost": 300,
                "count": 300
            },
            {
                "type": "props",
                "desc": "金蛋",
                "cost": 300,
                "id": 213,
                "count": 1
            }
        ],
        "benefit": {
            "which": 1,     // 已经赠送次数
            "wait": 100,    // 还需要等待时间, 无此字段表示没有触发破产
            "conf": [
                {"chip": 2000, "wait": 30},
                {"chip": 2000, "wait": 120},
                {"chip": 2000, "wait": 300},
            ]
        },
        "group_buy": {
            "reward": {
                "1": {                                 // 需要的总购买人数:奖励内容(这个格式参考的等级奖励)
                    "diamond": 30,
                    "props": [{"id": 214, "count": 3}]
                },
                "50": {
                    "diamond": 30,
                    "props": [{"id": 214, "count": 3}]
                }
            },
            "start": "10:00:00",  // 开始时间
            "end": "12:00:00",    // 结束时间
        },
        "html": {
            "http_game": "http://192.168.1.35:9008",
            "activity": "http://192.168.1.35:9008/static/bird/android/qifan/activity",
            "rank": "http://192.168.1.35:9008/static/bird/android/qifan/rank",
            "history": "http://192.168.1.35:9008/static/bird/android/qifan/history"
        },
        "match": {
            "day": [
                {
                    "rank": [1, 1],
                    "reward": {
                        "props": [{"id": 214, "count": 40}]
                    }
                },
                {
                    "rank": [2, 2],
                    "reward": {
                        "props": [{"id": 214, "count": 20}]
                    }
                },
                {
                    "rank": [3, 3],
                    "reward": {
                        "props": [{"id": 214, "count": 10}]
                    }
                },
                {
                    "rank": [4, 10],
                    "reward": {
                        "props": [{"id": 214, "count": 5}]
                    }
                },
                {
                    "rank": [11, 50],
                    "reward": {
                        "props": [{"id": 213, "count": 5}]
                    }
                },
                {
                    "rank": [51, 100],
                    "reward": {
                        "props": [{"id": 213, "count": 3}]
                    }
                },
                {
                    "rank": [101, 200],
                    "reward": {
                        "props": [{"id": 212, "count": 3}]
                    }
                },
                {
                    "rank": [201, 300],
                    "reward": {
                        "props": [{"id": 211, "count": 3}]
                    }
                },
                {
                    "rank": [301, 500],
                    "reward": {
                        "props": [{"id": 211, "count": 2}]
                    }
                },
                {
                    "rank": [501, 1000],
                    "reward": {
                        "props": [{"id": 211, "count": 1}]
                    }
                }
            ],
            "week": {
                "rmb": 20000
            },
            "month": {
                "rmb": 80000
            }
        }
    }
}
```

#### exp等级升级

```
{
    "cmd": BIRD_MSG_EXP_UPGRADE | ID_NTF,
    "param": {
        "exp": 5,
        "lv": 2,
        "df": [5, 20],
        "c": 10164,         // final chip
        "d": 9527,          // final diamond
        "w": {
            "c": 9527,                      // 金币
            "d": 12,                        // 钻石
            "c": 11,                        // 兑换券
            "p": [[205, 1], [202, 2],       // 道具
        },
    }
}
```

#### 道具列表(背包)

```
{
    "cmd": MSG_SYS_PROPS_LIST | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_PROPS_LIST | ID_ACK,
    "param": {
        "c": 1986,             // 金币
        "d": 0,                // 钻石
        "o": 0,                // 兑换券
        "up": {                // exp升级奖励
            "c": 150,
            "d": 10,
            "p": [
                [201, 2],
                [202, 3]
            ]
        },
        "p": [                  // 道具, 没有道具无此字段
            [201, 2],
            [202, 3]
        ]
    }
}
```

#### 使用道具

```
{
    "cmd": MSG_SYS_USE_PROPS | ID_REQ,
    "param": {
        "id": 211,
        "count": 2,
    }
}
```

```
{
    "cmd": MSG_SYS_USE_PROPS | ID_ACK,
    "param": {
    }
}
```

#### 抽奖

```
{
    "cmd": MSG_SYS_RAFFLE | ID_REQ,
    "param": {
        "i": 1,
        "bt": 1,
    }
}
```

```
{
    "cmd": MSG_SYS_RAFFLE | ID_ACK,
    "param": {
        "i": 1,                 // 哪一个奖励, 从1开始
        "bt": 1,
        "c": 121211,
        "d": 8522,
        "w": {
            "c": 9527,          // 金币
            "d": 12,            // 钻石
            "p": [[205, 1]],    // 道具
            "o": 11,            // 兑换券
        },
    }
}
```

#### 获取每日任务

```
{
    "cmd": MSG_SYS_TASK_LIST | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_TASK_LIST | ID_ACK,
    "param": {
        "tasks": [
            {
                "id": 0,
                "type": 1,
                "total": 37,
                "desc": "击杀秃鹫37只",
                "bird_type": 111,
                "degree": 5,
                "count": 0
            },
            {
                "id": 1,
                "type": 1,
                "total": 25,
                "desc": "击杀苍鹰25只",
                "bird_type": 110,
                "degree": 5,
                "count": 0
            },
            {
                "id": 2,
                "type": 1,
                "total": 23,
                "desc": "击杀白鹭23只",
                "bird_type": 108,
                "degree": 5,
                "count": 0
            },
            {
                "id": 3,
                "type": 1,
                "total": 19,
                "desc": "击杀火烈鸟19只",
                "bird_type": 112,
                "degree": 5,
                "count": 0
            },
            {
                "id": 4,
                "type": 1,
                "total": 34,
                "desc": "击杀鸽子34只",
                "bird_type": 105,
                "degree": 5,
                "count": 0
            },
            {
                "id": 5,
                "type": 1,
                "total": 37,
                "desc": "击杀麻雀37只",
                "bird_type": 102,
                "degree": 5,
                "count": 0
            },
            {
                "id": 6,
                "type": 2,
                "total": 3,
                "desc": "击杀BOSS3只",
                "count": 0,
                "degree": 10
            },
            {
                "id": 7,
                "type": 3,
                "total": 3,
                "desc": "击杀奖金鸟3只",
                "count": 0,
                "degree": 10
            },
            {
                "id": 8,
                "type": 11,
                "total": 457,
                "desc": "赚取金币457",
                "count": 0,
                "degree": 10
            },
            {
                "id": 9,
                "type": 21,
                "desc": "每日登陆",
                "degree": 10,
                "done": 1
            }
        ],
        "reward": [
            {
                "degree": 50,
                "state": 0,
                "reward": {
                    "c": 4545
                }
            },
            {
                "degree": 80,
                "state": 0,
                "reward": {
                    "c": 4545
                }
            },
            {
                "degree": 100,
                "state": 0,
                "reward": {
                    "c": 4545
                }
            }
        ],
        "degree": 10
    }
}
```

#### 领取任务奖励

```
{
    "cmd": MSG_SYS_CONSUME_TASK | ID_REQ,
    "param": {
        "id": 1
    }
}
```

```
{
    "cmd": MSG_SYS_CONSUME_TASK | ID_ACK,
    "param": {
        "c": 121211,
        "d": 8522,
        "w": {
            "c": 9527,          // 金币
            "d": 12,            // 钻石
            "p": [[201, 2]],    // 道具
            "o": 11,            // 兑换券
        },
    }
}
```

#### 赠送道具

```
{
    "cmd": MSG_SYS_PRESENT | ID_REQ,
    "param": {
        "id": 201,          // 道具id
        "count": 8,         // 道具数量
        "ta": 121212        // 对方id
    }
}
```

```
{
    "cmd": MSG_SYS_PRESENT | ID_ACK,
    "param": {
        "id": 201,          // 道具id
        "count": 100        // 剩余道具数量
    }
}
```

#### 购买道具

```
{
    "cmd": MSG_SYS_INNER_BUY | ID_REQ,
    "param": {
        "id": 201,          // 道具id
        "count": 8          // 道具数量
    }
}
```

```
{
    "cmd": MSG_SYS_INNER_BUY | ID_ACK,
    "param": {
        "diamond": 11111,   // 剩余钻石
        "id": 201,          // 道具id
        "count": 100        // 剩余道具数量
    }
}
```

#### 兑换券

```
{
    "cmd": MSG_SYS_EXCHANGE | ID_REQ,
    "param": {
        "id": 0,                    // 配置对应下标
        "phone": 13800000000        // 如果是话费兑换, 有该字段
    }
}
```

```
{
    "cmd": MSG_SYS_EXCHANGE | ID_ACK,
    "param": {
        "coupon": 1212,     // 剩余兑换券
        // 如果是道具
        "id": 201,          // 道具id
        "count": 100        // 剩余道具数量
        // 如果是钻石
        "diamond": 1212,
    }
}
```

#### 场景增量内容

```
{
    "cmd": BIRD_MSG_DELTA_SCENE | ID_NTF,
    "param": {
        "birds": [],        // 和broad_info中一样
        "tide": {},         // 和broad_info中一样
        "bounty": {},       // 和broad_info中一样
        "uptime": 111,      // uptime 用不用无所谓
        "events": []        // 和broad_info中相同
    }
}
```

#### 破产

```
{
    "cmd": BIRD_MSG_BANKRUPT | ID_NTF,
    "param": {
        "userId": 20000,
        "wait": 111,     // 还要等待时间
        "which": 1       // 将要领取第几次
    }
}
```

#### 上报辐射到的鸟

```
{
    "cmd": BIRD_MSG_REPORT_BIRDS | ID_REQ,
    "param": {
        "bird": 11,                 // hit ack中的参数
        "ts": 1212121212,           // hit ack中的参数
        "birds": [12, 15...]        // 鸟的id
    }
}
```

#### 兑换码

```
{
    "cmd": MSG_SYS_CONSUME_CDKEY | ID_REQ,
    "param": {
        "code": "e12fbd7a1",
        "imei": "test",
    }
}
```

```
{
    "cmd": MSG_SYS_CONSUME_CDKEY | ID_ACK,
    "param": {
        "c": 121211,
        "d": 8522,
        "w": {
            "c": 9527,                      // 金币
            "d": 12,                        // 钻石
            "o": 11,                        // 兑换券
            "p": [[205, 1], [201, 1]],      // 道具
        }
    }
}
```

#### 活动列表

`/v1/game/activity_list`

```
{
    "cmd": MSG_SYS_ACTIVITY_LIST | ID_REQ,
    "param": {
        "userId": 20001,
        "gameId": 2,
        "session": "C95EEEC2007BAF6C78AD6A2A95CC487C",
    }
}
```

```
{
    "cmd": MSG_SYS_ACTIVITY_LIST | ID_ACK,
    "param": {
        "list": [
            {   // 你捕鸟我送礼
                "id": 100,
                "type": 100,
                "var": [1000, 100, 0],  // 打多少, 奖励, 已打
                "state": 0
            },
            {   // 新手保送100级
                "id": 200,
                "type": 200,
                "var": 1,       // 第几天
                "state": 0
            }，
            {   // 300倍炮领金蛋
                "id": 300,
                "type": 300,
                "state": 0
            },
            {   // 500倍炮领金蛋
                "id": 301,
                "type": 300,
                "state": 0
            },
            {   // 1000倍炮领金蛋
                "id": 302,
                "type": 300,
                "state": 0
            },
            {   // 免费道具助力新版
                "id": 310,
                "type": 310,
                "state": 1
            },
            {   // 免费道具助力新版
                "id": 311,
                "type": 310,
                "state": 1
            },
            {   // 免费道具助力新版
                "id": 312,
                "type": 310,
                "state": 1
            },
            {   // 每日首冲领好礼
                "id": 320,
                "type": 320,
                "state": 0
            },
            {   // 幸运转转乐
                "id": 330,
                "type": 330,
                "state": 1
            },
            {   // 终极BOSS送金蛋
                "id": 340,
                "type": 340,
                "state": 0
            }
        ]
    }
}
```

#### 领取活动奖励

`/v1/game/consume_activity`

```
{
    "cmd": MSG_SYS_CONSUME_ACTIVITY | ID_REQ,
    "param": {
        "userId": 20001,
        "gameId": 2,
        "session": "C95EEEC2007BAF6C78AD6A2A95CC487C",
        "id": 100
    }
}
```

```
{
    "cmd": MSG_SYS_CONSUME_ACTIVITY | ID_ACK,
    "param": {
        "id": 200,
        "reward": {"diamond": 30},
        "diamond": 98,
    }
}

{
    "cmd": MSG_SYS_CONSUME_ACTIVITY | ID_ACK,
    "param": {
        "id": 100,
        "reward": {"chip": 100},
        "chip": 1000100,
    }
}
```

#### 排行榜

`/v1/game/rank_list`

```
{
    "cmd": MSG_SYS_RANK_LIST | ID_REQ,
    "param": {
        "userId": 20001,
        "gameId": 2,
        "session": "C95EEEC2007BAF6C78AD6A2A95CC487C",
        "rank": ["chip", "exp", "egg"]     // 不发送表示获取全部, 指定获取哪些, 只获取单个可以不是数组
    }
}
```

```
{
    "cmd": MSG_SYS_RANK_LIST | ID_ACK,
    "param": {
        "chip": [
            "{\"uid\":25558,\"avatar\":\"25\",\"sex\":0,\"nick\":\"Win32\",\"vip\":0,\"chip\":10257,\"exp\":5}"
        ],
        "exp": [
            "{\"uid\":25558,\"avatar\":\"25\",\"sex\":0,\"nick\":\"Win32\",\"vip\":0,\"chip\":10257,\"exp\":5}"
        ],
        "egg": [
            "{\"uid\":25558,\"avatar\":\"25\",\"sex\":0,\"nick\":\"Win32\",\"vip\":0,\"chip\":10257,\"exp\":5,\"egg\":5}"
        ],
        "mine": {
            "chip": 3713,
            "exp": 0,
            "sex": 0,
            "nick": "test",
            "avatar": "27",
            "vip": 1,
            "egg": 5
        }
    }
}
```

#### 记录

`/v1/game/history`

```
{
    "cmd": MSG_SYS_HISTORY | ID_REQ,
    "param": {
        "userId": 20001,
        "gameId": 2,
        "session": "C95EEEC2007BAF6C78AD6A2A95CC487C",
    }
}
```

```
{
    "cmd": MSG_SYS_HISTORY | ID_ACK,
    "param": {
        "exchange": [
            {
                "ts": 1455759616,
                "desc": "300钻石",
                "cost": 300,
                "state": 1
            },
            {
                "ts": 1455698849,
                "desc": "30元话费",
                "cost": 300,
                "state": 0,
                "phone": 15811147233
            }
        ]
    }
}
```

#### 召唤小红鸟

```
{
    "cmd": BIRD_MSG_CALL_BIRD | ID_NTF,
    "param": {
        "u": 20002,         # 谁的周围出现小红龙
        "loc": 0,           # 小红龙的位置
        "bird": {           # 小红鸟
            "t": 302,
            "i": 111
        }
}
```

#### 小红鸟攻击

```
{
    "cmd": BIRD_MSG_BIRD_ATTACK | ID_NTF,
    "param": {
        "u": 20002,         # who
        "i": 111            # 哪只龙攻击
        "c": 205821,        # 剩余chip, miss时无此字段
        "t": 20000,         # 掉落金币量, miss时无此字段
        "bird": {           # 小红龙变金色， miss时无此字段
            "t": 303,
            "i": 112
        }
}
```

#### 红龙任务结束通知

```
{
    "cmd": BIRD_MSG_RED_DRAGON_END | ID_NTF,
    "param": {
        "fail": 1,              // 失败
        "return": [             // 失败返还金币
            {
                "u": 20001,         // userId
                "t": 40000,         // 返还金币
                "c": 500000,        // 剩余金币
            }
            // ...
        ]
    }
}
```

#### 赏金任务结束通知

```
{
    "cmd": BIRD_MSG_BOUNTY_END | ID_NTF,
    "param": {
        "c": 121211,
        "d": 8522,
        "w": {
            "c": 9527,          // 金币
            "d": 12,            // 钻石
            "p": [[201, 2]],    // 道具
            "o": 11,            // 兑换券
        }
    }
}
```

#### 赏金任务排名信息变化

```
{
    "cmd": BIRD_MSG_RANK_CHANGE | ID_NTF,
    "param": {
        "u": 20001,                     // who
        "dt": [[104, 2], [105, 2]],     // 最新捕获详情
        "rk": [20001, 20002...]         // 最新排名
    }
}
```

#### 获取领取信息

```
{
    "cmd": MSG_SYS_INVITE_INFO | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_INVITE_INFO | ID_ACK,
    "param": {
        "list": [
            {
                "uid": 20002,        // 被邀请者
                "multi": 123,        // 解锁炮倍
                "nick": "nick",      // 昵称
                "sex": 1,            // 性别
                "ids": [1, 2, 3]     // 已经领取的奖励id
            }
        ],
    }
}
```

#### 获取分享模块信息

```
{
    "cmd": MSG_SYS_SHARE_INFO | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_SHARE_INFO | ID_ACK,
    "param": {
        "invitee": [100001,100002],         // 被邀请者列表
        "last_ts": 111111111,               // 最后一次领取分享奖励的时间戳
        "invite_code": '111111111',         // 邀请码
        "inviter": 100001,                  // 邀请者
    }
}
```

#### 分享

```
{
    "cmd": MSG_SYS_SHARE | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_SHARE | ID_ACK,
    "param": {
    }
}

error code:
1 已经领取过
```

#### 绑定别人的分享

```
{
    "cmd": MSG_SYS_BIND_INVITER | ID_REQ,
    "param": {
        "invite_code": "123456"
    }
}
```

```
{
    "cmd": MSG_SYS_BIND_INVITER | ID_ACK,
    "param": {
    }
}

error code:
1 分享码错误
2 已经绑定
3 超出最大炮倍
```

#### 领取好友达成奖励

```
{
    "cmd": MSG_SYS_INVITE_REWARD | ID_REQ,
    "param": {
        "id": 123,          // 奖励的id
        "invitee": 10001    // 被邀请者uid
    }
}
```

```
{
    "cmd": MSG_SYS_INVITE_REWARD | ID_ACK,
    "param": {
    }
}

error code:
1 玩家ID错误
2 奖励ID错误
3 玩家条件未达成
4 已经领取
```

#### 获取团购模块信息

```
{
    "cmd": MSG_SYS_GROUP_BUY_INFO | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_GROUP_BUY_INFO | ID_ACK,
    "param": {
        "count": 1111,             // 已买总个数
        "buy_state": 1,            // 1 买 0未买
        "ids": [11,22],            // 已经领取的奖励id
    }
}
```

#### 领取团购奖励

```
{
    "cmd": MSG_SYS_GROUP_BUY_REWARD | ID_REQ,
    "param": {
        "id": 123,       // 奖励的id
    }
}
```


```
{
    "cmd": MSG_SYS_GROUP_BUY_REWARD | ID_ACK,
    "param": {
    }
}
```

#### 红点标记状态

```
{
    "cmd": MSG_SYS_MARK_STATE | ID_REQ,
    "param": {
        "mark_types": ["all", "group_buy"],       // 如果有all ，查询所有的，否则查询传入的。
    }
}
```


```
{
    "cmd": MSG_SYS_MARK_STATE | ID_ACK,
    "param": {
        "state": {"group_buy": 1,         // 1,标记红点(有需要领取等)  2:0无信息
        }
    }
}
```

#### 打地鼠

```
MSG_SYS_POKE_MOLE

请求 i 锤子id 1-8 在普通场景可以是1-6和8.金币潮是7
返回 c 砸中的金币数量  
     fc 金币剩余量
     co 掉落话费卷个数
     cf 玩家话费卷总个数
     mc 金币潮能量
     mh 雷神锤能量
error code:
  1 id error
  2 缺少金币
  3 雷神锤能量不足

```
#### 切换场景

```
MSG_SYS_POKE_MOLE_CHANGE

请求  s  场景id 1普通场景， 2金币潮
返回 空
error code:
1 id error
2 金币能量不足

```
#### 获取打地鼠基本信息

```
MSG_SYS_POKE_MOLE_INFO

请求 空
返回 s 场景id
     ts 如果在金币潮时间内，这个值不为空，指的是 金币潮开始时间
     cp 能量条的值
     hp 雷神锤能量条的值
```
