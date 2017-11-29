server配置文件唯一定义一组服务器, 以如下示例说明:

```
{
    "id": 1,
    "name": "ddz",
    "mode": 1,
    "corporation": "langang",
    "tcp.port": 9000,
    "http.sdk": "http://123.57.24.61",
    "servers": {
        "ddz-1": {"internet": "123.57.24.61", "intranet": "10.171.56.234"}
    },
    "config.file": "config/default.py",
    "exe": {
        "game": {
            "bin": "services/gamesvrd/gamesvrd",
            "so": {"game": "games/ddz/ddz-game/ddz-game.so"}
        },
        "quick": {"bin": "services/quicksvrd/quicksvrd"},
        "connect": {"bin": "services/connectsvrd/connectsvrd"},
        "entity": {
            "bin": "services/entitysvrd/entitysvrd",
            "so": {"entity": "games/ddz/ddz-entity/ddz-entity.so"}
        }
    },
    "process": [
        {"type": "game", "id": 20000, "server": "ddz-1", "desc": "game server"},
        {"type": "quick", "id": 20002, "server": "ddz-1", "desc": "quick start server"},
        {"type": "entity", "id": 20004, "server": "ddz-1", "desc": "entity server"},
        {"type": "connect", "id": 20006, "server": "ddz-1", "desc": "connect server"},
        {"type": "game", "id": 20008, "server": "ddz-1", "mode": "py",  "desc": "game server"},
        {"type": "stat", "id": 20010, "server": "ddz-1", "mode": "py",  "desc": "langang stat server"}
    ],
    "redis": {
        "config": {"host": "10.171.61.153", "port": 6379, "db": 0},
        "cluster": [
            {"host": "10.171.61.153", "port": 6380, "db": 0},
            {"host": "10.171.61.153", "port": 6381, "db": 0},
            {"host": "10.171.61.153", "port": 6382, "db": 0},
            {"host": "10.171.61.153", "port": 6383, "db": 0},
            {"host": "10.171.61.153", "port": 6384, "db": 0},
            {"host": "10.171.61.153", "port": 6385, "db": 0},
            {"host": "10.171.61.153", "port": 6386, "db": 0},
            {"host": "10.171.61.153", "port": 6387, "db": 0}
        ],
        "mix": {"host": "10.171.61.153", "port": 6400, "db": 0},
        "purchase": {"host": "10.171.61.153", "port": 6401, "db": 0},
        "stat": {"host": "10.171.61.153", "port": 6402, "db": 0},
        "cache": {"host": "10.171.61.153", "port": 6403, "db": 0}
    }
}
```

### 字段说明

1. id: 游戏id, 不需要修改
2. name: 游戏名称, 不需要修改
3. mode: 启动模式, 1为正式服, 2为提审服, 3为测试服
4. corporation: 公司名称, 不需要修改
5. tcp.port: 见process说明
6. http.sdk: sdk服务器对外的ip和端口
7. servers: 服务器ip(外网ip和内网ip), 用户process配置
8. config.file: 对应的游戏配置文件, 不用修改
9. exe: 进程类型对应的执行文件, 不用修改
10. process: 进程的配置, `id`字段表示serverId, 需要唯一; `type`表示进程的类型; `mode`默认启动文件是二进制, 如果为`py`表示是python程序; 每个进程的监听的port是启动的时候自动分配(累加2), 如当前配置就是[9000, 9002, 9004, 9006, 9008, 9010], 这些偶数端口用于间服务器内部通信, 成为对内端口, `connect`类型的进程会多监听一个端口, 用于client来连接, 称为对外的端口, 端口为对内端口加1, 对应上面配置就是9007(9006+1), 对外端口需要外网可以访问, 对内端口保证进程间可访问(使用内网ip)
11. redis: redis配置, 其中`config`和`cache`不需要备份, `cluster`对应用户数据, 按照userId的模分库, `mix`保存长久保存不需要分库的数据, `purchase`保存支付相关信息, `stat`统计相关信息, redis目前内网访问

### 注意

增加`game`进程的时候需要修改`config.file`中对应的文件房间配置
