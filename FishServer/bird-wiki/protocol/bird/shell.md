#### 概要

`/v1/shell/query/overview`

```
{
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg=="
}
```

```
{
    'total': {
        'user.count': 100,                              // 累计玩家数
        'pay.user.count': 10,                           // 累计付费玩家
        'pay.total': 1000                               // 累计收入
    },
    'today': {
        'new.user.count': 11,                           // 当日新用户
        'login.user.count': 19,                         // 当日活跃用户
        'pay.total': 11,                                // 当日收入
        'out.chip.pump': 111111,                        // 当日抽水
        'out.chip': 11111,                              // 当日金币消耗
        'in.chip': 111111,                              // 当日金币产出
        'out.diamond': 1111,                            // 当日钻石消耗
        'in.diamond': 111,                              // 当日钻石产出
        'fall.egg': 100,                                // 当日egg掉落统计
        'shot.times': 444444,                           // 当日发炮统计
        'pool.chip': [1, 0, 0, 2],                      // 当日奖池统计
        'red.pool.chip': 11111,                         // 当日红龙奖池统计
        'carrying.volume': 111111,                      // 当日金币携带量
        'login.carrying.volume': 1111,                  // 昨日活跃用户金币携带量
        'online': [10, 11, 1, 5]                        // 在线
    }
}
```

#### 数据查询

`/v1/shell/query/summary`

```
{
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "start": "2016-03-29",
    "end": "2016-03-29",
}
```

```
{
    "2016-03-29": {
        "qifan": {
            "new.device.count": 0,          // 新增设备数量
            "new.user.count": 2,            // 新增用户数量
            "login.user.count": 5,          // 活跃用户数量
            "new.pay.user.count": 0,        // 新增付费用户数量
            "new.pay.user.pay_total": 0,    // 新增用户付费总额
            "pay.user.count": 0,            // 付费用户数量
            "pay.user.pay_total": 0,        // 付费总量
            "user.pay.times": 0             // 付费次数
        },
        "360": {
            "new.device.count": 0,          // 新增设备数量
            "new.user.count": 2,            // 新增用户数量
            "login.user.count": 5,          // 活跃用户数量
            "new.pay.user.count": 0,        // 新增付费用户数量
            "new.pay.user.pay_total": 0,    // 新增用户付费总额
            "pay.user.count": 0,            // 付费用户数量
            "pay.user.pay_total": 0,        // 付费总量
            "user.pay.times": 0             // 付费次数
        }
    }
}
```

#### 销售明细

`/v1/shell/query/pay/detail`

```
{
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "start": "2016-03-21",
    "end": "2016-03-22",
}
```

```
{
    "2016-03-21": {
        "product_100632": 0,        // 12金币
        "product_100633": 0,        // 28金币
        "product_100634": 0,        // 50金币
        "product_100635": 0,        // 108金币
        "product_100636": 0,        // 328金币
        "product_100637": 0,        // 618金币
        "product_100638": 0,        // 12钻石
        "product_100639": 0,        // 28钻石
        "product_100640": 0,        // 50钻石
        "product_100641": 0,        // 108钻石
        "product_100642": 0,        // 328钻石
        "product_100630": 0,        // 月卡(贵族)
        "product_100631": 0,        // 首冲
        "product_100646": 0,        // 公益礼包
        "product_100668": 0         // 6元首冲
        "product_100710": 0,        // 团购
    }
}
```

#### 抽水

`/v1/shell/query/chip/pump`

```
{
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "start": "2016-03-23",
    "end": "2016-03-24",
}
```

```
{
    "2016-03-23": [0, 0, 0, 1],
    "2016-03-24": [59, 0, 0, 2]
}
```

#### 金币消耗

`/v1/shell/query/chip/consume`

```
{
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "start": "2016-03-23",
    "end": "2016-03-24",
}
```

```
{
    "2016-03-23": [0, 0, 0, 0, 11, 12],    // 初, 中, 高, 大奖赛, 龙虎斗, 百人牛牛
    "2016-03-24": [92, 0, 0, 0, 11, 12]
}
```

#### 金币产出

`/v1/shell/query/chip/produce`

```
{
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "start": "2016-03-24",
    "end": "2016-03-24",
}
```

```
{
    "2016-03-24": {
        "in.chip.signin.reward": 1000,          // 签到
        "in.chip.exp.upgrade": 450,             // 升级赠送
        "in.chip.game.startup": 300,            // 启动资金(新增用户)
        "in.chip.task.reward": 0,               // 任务奖励
        "in.chip.catch.bird": 350               // 掉落
        "in.chip.buy.product": 1000             // 充值
        "in.chip.entity.use": 1000              // 宝盒
        "in.chip.cdkey.reward": 1000            // cdkey
        "in.chip.unlock.barrel": 0,             // 解锁
        "in.chip.gm.reward": 0,                 // gm赠送
        "in.chip.bonus.raffle": 121212,         // 抽奖
        "in.chip.game.10002": 1000,             // 龙虎斗
        "in.chip.game.10003": 1200,             // 百人牛牛
    }
}
```

#### 钻石消耗

`/v1/shell/query/diamond/consume`

```
{
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "start": "2016-03-24",
    "end": "2016-03-24",
}
```

```
{
    "2016-03-24": {
        "total": 12121212,                  // 总数
        "out.diamond.buy.201": 199,         // 锁定
        "out.diamond.buy.202": 199,         // 冰冻
        "out.diamond.buy.203": 199,         // 狂暴(嗜血)
        "out.diamond.buy.204": 199,         // 超级武器
        "out.diamond.buy.205": 199,         // 传送门
        "out.diamond.unlock.barrel": 50     // 解锁
    }
}
```

#### 钻石产出

`/v1/shell/query/diamond/produce`

```
{
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "start": "2016-03-24",
    "end": "2016-03-24",
}
```

```
{
    "2016-03-24": {
        "total": 12121212,                     // 总数
        "in.diamond.exp.upgrade": 100,         // 升级奖励
        "in.diamond.bird.fall": 1000,          // 掉落
        "in.diamond.buy.product": 1000,        // 充值
        "in.diamond.cdkey.reward": 1000,       // cdkey
        "in.diamond.task.reward": 0,           // 任务奖励
        "in.diamond.gm.reward": 0,             // gm赠送
    }
}
```

#### egg掉落

`/v1/shell/query/props/egg/fall`

```
{
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "start": "2016-03-28",
    "end": "2016-03-28",
}
```

```
{
    "2016-03-28": {
        "fall": [1, 5, 4],                     // 铜银金
        "get": 0                               // 获得人数
    }
}
```

#### 发炮统计

`/v1/shell/query/shot`

```
{
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "start": "2016-03-28",
    "end": "2016-03-28",
}
```

```
{
    "2016-03-28": [752,3438,36,23]
}
```

#### 携带量

`/v1/shell/query/chip/carrying`

```
{
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "start": "2016-03-28",
    "end": "2016-03-28",
}
```

```
{
    "2016-03-28": {
        "carrying": 100,            // 活跃携带量
        "total": 1200               // 总携带量
    }
}
```

#### 用户查询

`/v1/shell/query/user/info`

```
{
    "userId": 20002,
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg=="
}
```

```
{
    "createTime": "2016-03-24 20:15:22",        // 注册时间
    "deviceId": "DEVID1458821722462",           // 设备号
    "phone": "13716800217",                     // 手机号
    "pay_total": 0,                             // 充值金额
    "out_chip": 100000,                         // 总金币消耗
    "in_chip": 100000,                          // 总金币获得
    "session_login": "2016-03-24 20:20:07",     // 最近登录时间
    "level": 2,                                 // 等级
    "vip_level": 0,                             // vip等级
    "barrel_multiple": 5                        // 炮倍数
    "chip": 1831,                               // 携带金币数量
    "diamond": 0,                               // 携带钻石数量
    "egg": [1, 20, 0, 1],                       // 宝盒数量: 铜, 银, 金, 彩
    "channel": "qifan"                          // 渠道
}
```

#### 赠送金币

`/v1/shell/gm/reward/chip`

```
{
    "userId": 20002,
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "chip": 1000,               // 增加金币数量
}
```

```
{
    "chip": 2831,               // 操作后金币数量
    "delta": 1000               // 增加金币数量
}
```

#### 赠送钻石

`/v1/shell/gm/reward/diamond`

```
{
    "userId": 20002,
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "diamond": 1000,            // 增加钻石数量
}
```

```
{
    "diamond": 1001,            // 操作后钻石数量
    "delta": 1000               // 增加钻石数量
}
```

#### 赠送vip

`/v1/shell/gm/reward/vip`

```
{
    "userId": 20002,
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "rmb": 100,                // 增加充值金额
}
```

```
{
    "level": 1,                // 操作后vip等级
    "pay_total": 100           // 操作后充值总额
}
```

#### 赠送月卡

`/v1/shell/gm/reward/card`

```
{
    "userId": 20002,
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "days": 30,                // 增加天数
}
```

```
{
    "days": 30,                // 剩余天数(包括今天)
}
```

#### 赠送egg

`/v1/shell/gm/reward/egg`

```
{
    "userId": 20002,
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "id": 212,                // 道具id (211: 铜蛋, 212: 银蛋, 213: 金蛋, 214: 彩蛋)
    "count": 2,               // 赠送数量
}
```

```
{
    "delta": 2,               // 赠送数量
    "id": 212,                // 道具id
    "count": 4                // 操作后道具总数
}
```

#### 冻结账号

`/v1/shell/gm/account/lock`

```
{
    "userId": 20194,
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "days": 10,               // 冻结天数(包括今天), 不传为解除冻结
}
```

```
{
    "end_ts":1459958400       // 解封时间
}
```

#### 封停账号

`/v1/shell/gm/account/disable`

```
{
    "userId": 20194,
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "disable": 1            // 0表示解封， 其他表示封停
}
```

```
{
}
```

#### 上报在线人数

`/buniao/show_online/add`

```
{
    "gameId": 2,                     // 游戏id
    "online": [100, 12, 16, 11],     // 初，中，高，大奖赛
    "ts": 1459399095                 // unix 时间戳
}
```

#### 上报奖池

`/buniao/pond_stat/add`

```
{
    "gameId": 2,                         // 游戏id
    "pool": [1000, 121, -1116, 11],      // 初， 中，高，大奖赛
    "red.pool": 1111,                    // 红龙
    "ts": 1459399095                     // unix 时间戳
}
```

#### 奖池调控

`/v1/shell/gm/pool/pump`

```
{
    "gameId": 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "delta": 100,                // 变量
    "room_type": 201             // 初级场
}
```

```
{
    "delta": 100,                // 变量
    "room_type": 201,            // 初级场
    "pool": 55555,               // 操作后奖池
}
```

#### 兑换话费查询

`/v1/shell/query/history/phone`

```
{
    "gameId": 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "start": "2016-03-28",
    "end": "2016-03-28",
}
```

```
{
    "exchange": [
        {
            "uid": 20002,               // 用户id
            "ts": 1460025434,           // unix时间戳
            "count": 30,                // 数量
            "phone": 13716800217,       // 手机号码
            "state": 1                  // 0为兑换, 1为已兑换
            "seq": 111,                 // 透传参数
        }
        // ...
    ]
}
```

#### 兑换话费处理

`/v1/shell/gm/exchange/phone`

```
{
    "userId": 20002,
    "gameId": 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "seq": 111
}
```

```
{
}
```

#### 发送公告

`/v1/shell/gm/push/led`

```
{
    "gameId": 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "msg": "I am led"       # 默认时此字段不发
}
```

```
{
}
```

#### 升级

`/v1/shell/gm/version/upgrade`

```
{
    "gameId": 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "version": "1.0.2",             // 目标升级的版本
    "changelog": "dkjkjljllll",     // 升级描述
    "size": "12.5M",                // 大小
    "bytes": 131072100,             // 具体大小
    "md5": "kdkjdkjdkdjk",          // md5
    "url": "http://apk_down_url",   // 下载地址
    "channel": "qifan",             // 升级渠道, all表示所有渠道
    "platform": "android",          // 平台, android or ios
    "prompt": "1.0.1",              // 低于此版本提示升级
    "force": "1.0.0",               // 低于此版本强制升级
}
```

```
{
}
```

#### 微信-绑定

`/v1/shell/weixin/user/bind`

```
{
    "gameId": 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "username": "9527dd",            // 昵称(用户名)
    "password": "dseccd",            // 密码
    "ID": "111111111111111111",      // 身份证号码
    "openid": "wx4545dekjkjkjkjk"    // 微信openid
}
```

```
{
}
```

#### 微信-解绑

`/v1/shell/weixin/user/unbind`

```
{
    "gameId": 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "username": "9527dd",            // 昵称(用户名)
    "password": "dseccd",            // 密码
    "ID": "111111111111111111",      // 身份证号码
    "openid": "wx4545dekjkjkjkjk"    // 微信openid
}
```

```
{
}
```

#### 微信-修改密码

`/v1/shell/weixin/user/modify/password`

```
{
    "gameId": 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "username": "9527dd",            // 昵称(用户名)
    "password": "dseccd",            // 新密码
    "openid": "wx4545dekjkjkjkjk"    // 微信openid
}
```

```
{
}
```

#### 修改团购人数

`/v1/shell/gm/group_buy/modify_num`

```
{
    "gameId": 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "num": "11"    // 修改成的团购人数
}
```

```
{
}
```

#### 小黑屋

`/v1/shell/gm/account/block`

```
{
    "userId": 200002,
    "odds": 0.5,        // 降低的概率, 范围(0, 1]; 不传表示放出来
}
```

```
{
}
```

#### 抽奖

`/v1/shell/query/raffle`

```
{
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "start": "2016-03-24",
    "end": "2016-03-24",
}
```

```
{
    "2016-03-24": {
        "chip": 100,           // 金币
        "diamond": 1000,       // 钻石
        "coupon": 1000,        // 奖券
        "egg": [1, 2, 5, 0]    // 铜, 银, 金, 彩
    }
}
```

#### 大奖赛

`/v1/shell/query/room/211`

```
{
    "gameId: 2,
    "token": "aXh4b28ubWVAZ21haWwuY29tCg==",
    "start": "2016-03-24",
    "end": "2016-03-24",
}
```

```
{
    "2016-03-24": {
        "in.diamond": 0,               // 钻石产出
        "out.chip": 0,                 // 金币消耗
        "in.chip": 0,                  // 金币产出
        "props": [0, 0],               // 锁定， 狂暴
        "egg": [0, 0, 0, 0]            // 铜, 银, 金, 彩
    }
}
```
