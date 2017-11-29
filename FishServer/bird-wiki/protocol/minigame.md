#### 注册服务器

```
{
    "cmd": MSG_INNER_SERVER_REGISTER | ID_REQ,
    "param": {
        "gameId": 10002,
        "ts": 1469095485,
        "sign": "ddw51215421dd2"    // md5("gameId=%d&token=%s&ts=%d")
    }
}
```

```
{
    "cmd": MSG_INNER_SERVER_REGISTER | ID_ACK,
    "param": {
        "http": "http://192.168.1.35:9006"  // http地址
    }
}
```

#### 获取用户信息

`/v1/game/third/user/info`

```
{
    "gameId": 2,
    "ts": 1469095485,
    "sign": "ddw51215421dd2"    // md5("gameId=%d&token=%s&ts=%d")
    "appId": 10002,             // 小游戏id
    "userId": 20006,
}
```

```
{
    "nick": "9527",
    "chip": 12121,
    "pay_total": 618,           // 今日充值
    "vip": 2,                   // vip等级
    "chip_pool": 45421445       // 奖池
}
```

#### 获取用户道具

`/v1/game/third/props/info`

```
{
    "gameId": 2,
    "ts": 1469095485,
    "sign": "ddw51215421dd2"    // md5("gameId=%d&token=%s&ts=%d")
    "appId": 10002,             // 小游戏id
    "userId": 20006,
    "pid": 213                  // 指定获取道具(可以是数组)， 不传获取全部
}
```

```
{
    "props": [[213, 5]]         // 道具列表
}
```


#### 修改金币

`/v1/game/third/incr/chip`

```
{
    "gameId": 2,
    "ts": 1469095485,
    "sign": "ddw51215421dd2"    // md5("gameId=%d&token=%s&ts=%d")
    "appId": 10002,             // 小游戏id
    "userId": 20006,
    "delta":: -111,             // 金币变量 
}
```

```
{
    "chip": 1515                // 剩余金币
}
```

#### 修改道具

`/v1/game/third/incr/props`

```
{
    "gameId": 2,
    "ts": 1469095485,
    "sign": "ddw51215421dd2"    // md5("gameId=%d&token=%s&ts=%d")
    "appId": 10002,             // 小游戏id
    "userId": 20006,
    "delta":: [213, -4],        // 道具变化
}
```

```
{
    "props": [[213, 1]]         // 剩余道具
}
```

#### 全局锁定

`/v1/game/third/playing/lock`

```
{
    "gameId": 2,
    "ts": 1469095485,
    "sign": "ddw51215421dd2"    // md5("gameId=%d&token=%s&ts=%d")
    "appId": 10002,             // 小游戏id
    "userId": 20002,
    "time": 120                 // 锁定120s，120s后自动解锁
}
```

```
{
}
```

#### 解除锁定

`/v1/game/third/playing/unlock`

```
{
    "gameId": 2,
    "ts": 1469095485,
    "sign": "ddw51215421dd2"    // md5("gameId=%d&token=%s&ts=%d")
    "appId": 10002,             // 小游戏id
    "userId": 20002,
}
```

```
{
}
```

#### 查询锁定

`/v1/game/third/playing/query`

```
{
    "gameId": 2,
    "ts": 1469095485,
    "sign": "ddw51215421dd2"    // md5("gameId=%d&token=%s&ts=%d")
    "appId": 10002,             // 小游戏id
    "userId": 20002,
}
```

```
{
    "gameId": 10003,           // 当前拥有锁的游戏id, 没有被锁定没有此字段
}
```
