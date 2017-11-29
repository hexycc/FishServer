#### 下单

`/v1/order/create`

```
{
    'gameId': 2,                    // 游戏id
    'channel': 'qifan',             // 渠道
    'platform': 'android',          // os
    'productId': 'QF00200105',      // 商品id
}
```

```
{
    'orderId': 'djkll1212dd',       // 单号
    'title': '328元金币',            // 商品名称
    'desc': '好爽呀, 加赠25%',        // 商品描述
    'cost': 30,                     // 总价
    'price': 30,                    // 商品单价
}
```

#### 查询订单

`/v1/order/deliver`

```
{
    'gameId': 2,                    // 游戏id
    'orders': ['QF00200105']        // 订单号
}
```

```
{
    'orders': [
        {'id': 'QF00200105', 'state': 6}
    ]
}
```

#### 升级

`/v1/upgrade/check`

```
{
    "gameId": 2,
    "version": "1.0.1",
    "channel": "qifan",
    "platform": "android"
}
```

```
{
    "upgrade": 0,                   // 0为不用升级, 1为提示升级, 2为必须升级
    "version": "1.0.2",             // 目标升级的版本
    "changelog": "dkjkjljllll",     // 升级描述
    "size": "12.5M",                // 大小
    "bytes": 131072100,             // 具体大小
    "md5": "kdkjdkjdkdjk",          // md5
    "url": "http://apk_down_url"    // 下载地址
}
```
