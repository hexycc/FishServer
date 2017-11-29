#### 捕鸟比赛消息

```
BIRD_MSG_COOK_TASK = const.Message.ID_BASE_OUTER_GAME + 0x29            # 厨师悬赏任务
BIRD_MSG_COOK_TASK_CHANGE = const.Message.ID_BASE_OUTER_GAME + 0x2A     # 厨师悬赏任务变换
BIRD_MSG_COOK_TASK_END = const.Message.ID_BASE_OUTER_GAME + 0x2B        # 厨师悬赏任务结束
BIRD_MSG_TASK_FINISH = const.Message.ID_BASE_OUTER_GAME + 0x2C          # 任务完成: 首次达到2400积分
```

#### 厨师悬赏任务开始

```
{
    "cmd": BIRD_MSG_COOK_TASK | ID_NTF,
    "param": {
        "score": 200,
        "in": 600,
        "show": 180,
        "info": [[104, 2], [106, 2], [176, 1]]
    }
}
```

#### 厨师悬赏任务信息变化

```
{
    "cmd": BIRD_MSG_COOK_TASK_CHANGE | ID_NTF,
    "param": {
        "dt": [[104, 2], [105, 2]],     // 最新捕获详情
    }
}
```

#### 厨师悬赏任务结束

```
{
    "cmd": BIRD_MSG_COOK_TASK_END | ID_NTF,
    "param": {
        "u": 20002,
        "s": 1212
    }
}

{
    "cmd": BIRD_MSG_COOK_TASK_END | ID_NTF,
    "param": {
        "fail": 1   // 失败
    }
}
```

#### 任务完成

```
{
    "cmd": BIRD_MSG_TASK_FINISH | ID_NTF,
    "param": {
        "id": 101,        // 首次达到2400积分获得100钻石
        "diamond": 5200,
        "reward": {"diamond": 200}
    }
}
```

#### 历史记录

`/v1/game/history`

```
{
    "cmd": MSG_SYS_HISTORY | ID_REQ,
    "param": {
        "which": "exchange"  // 兑换记录("exchange"), 名人堂("fame"), 我的荣誉("honor")
    }
}
```

```
{
    "cmd": MSG_SYS_HISTORY | ID_ACK,
    "param": {
        "fame": [
            {"tm": "11.02-11.08", "nick": "wan尼玛", "score": 8361, "level": 2},
            {"tm": "12.01-12.31", "nick": "papi酱", "score": 11111111, "level": 3}
        ],
        "honor": [
            {"rank": 202, "tm": "01.30", "reward": [211, 3]},
            {"rank": 202, "tm": "01.30", "reward": [211, 3]}
        ]
    }
}
```

#### 获取奖励列表

```
{
    "cmd": MSG_SYS_AWARD_LIST | ID_REQ,
    "param": {
        "list": ["match"]
    }
}
```

```
{
    "cmd": MSG_SYS_AWARD_LIST | ID_ACK,
    "param": {
        "match": [
            {
                "id": 1, 
                "type": 1,          // 1为直接领取, 2为填写信息
                "title": "日冠军06.11",
                "score": 1111,
                "desc": "获得奖励彩蛋*2"
            }
            {
                "id": 6,
                "type": 2,
                "title": "周冠军06.06-06.12",
                "score": 9999,
                "desc": "获得奖励10000元现金"
            }
            {
                "id": 8,
                "type": 2,
                "title": "月冠军06.01-06.30",
                "score": 9999,
                "desc": "获得奖励80000元现金"
            }
        ]
    }
}
```

#### 领取奖励

```
{
    "cmd": MSG_SYS_CONSUME_AWARD | ID_REQ,
    "param": {
        "id": 9527,
        "name": "张三",                   // 姓名
        "ID": "41212121212121212",       // 身份证
        "bank_no": "622221212121212",    // 银行卡
        "bank_addr": "中国银行北京分行"     // 开户行
    }
}
```

```
{
    "cmd": MSG_SYS_CONSUME_AWARD | ID_ACK,
    "param": {
        "id": 9527
        // reward 结构
    }
}
```

#### 排行榜

```
{
    "cmd": MSG_SYS_RANK_LIST | ID_REQ,
    "param": {
        "rank": ["day"]     // 指定获取哪些, 只获取单个可以不是数组
    }
}
```

```
{
    "cmd": MSG_SYS_RANK_LIST | ID_REQ,
    "param": {
        "day": [
            {
                "tm": "06.07",
                "list": [
                    "{\"uid\":25558,\"sex\":0,\"nick\":\"Win32\",\"vip\":0,\"score\":7581}"
                ],
                "mine": {"uid":25558,"sex":0,"nick":"Win32","vip":0,"score":7581}
            }
        ]
    }
}
```

#### 比赛概览

```
{
    "cmd": MSG_SYS_MATCH_ENTRY | ID_REQ,
    "param": {
    }
}
```

```
{
    "cmd": MSG_SYS_MATCH_ENTRY | ID_ACK,
    "param": {
        "month": 4545454,       // 月积分
        "score": 111,           // 日积分
        "rank": 12,             // 日排名
        "fee": 1,               // 报名费
        "state": 1,             // 0: 未开始 1: 进行中，需要报名 2: 续完
        "start": 12121212,      // 开始时间
        "end": 45454545,        // 结束时间
        "ts": 3563535,          // 当前时间
        "month_cp": {"score": 8888, "reward": {"rmb": 80000}, "nick": "土豪不差钱"},
        "week_cp": {"score": 6666, "reward": {"rmb": 20000}, "nick": "我要拿第一"},
        "list": [
            "{\"uid\":25558,\"sex\":0,\"nick\":\"Win32\",\"vip\":0,\"score\":7581}"
        }
    }
}
```

#### 比赛结算

```
{
    "cmd": MSG_SYS_MATCH_RESULT | ID_NTF,
    "param": {
        "score": 3333,
        "barrel": 13,
        "vip": 18,
        "final": 6666,
        "highest": 6666,
        "rank": 121,
        "fee": 3
    }
}
```
