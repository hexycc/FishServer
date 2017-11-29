#### 消息

消息类型分为三大类, 请求(req), 应答(ack)和通知(ntf). 

```
ID_REQ = 0x01000000        # 请求
ID_ACK = 0x02000000        # 应答
ID_NTF = 0x04000000        # 通知
```

消息功能上分为通用消息和游戏消息, 系统消息为框架所用, 所有游戏继承; 游戏消息为每个游戏自己定义, 理论上可以重复定义.

#### 格式

消息格式为: <消息头><body>, body目前采用json字符串. 整个消息格式为: <4位消息标识><4位消息长度><4位消息序列><body>.

1. 消息标识: 消息传输中必须已经和消息类型进行`|`运算, 是上面三类消息中的一种
2. 消息长度: 代表body的长度
3. 消息序列: 暂时没有使用, 理论上为递增整数, 服务器ack时会带上客户端req中的消息序列号
4. body: json字符串

双方通过cmd来表示消息含义, body来提供必要的参数交互, body对应json object结构pack后的字符串, 如果error中有错误, 表示请求出错, 具体含义参考下面应答中的说明.

#### 请求

请求类消息(req)一般为客户端发起, 服务器一般回复对应的ack, 根据设计不是每次都会有ack.

```
{
    "cmd": XXX_MSG_ID | ID_REQ,     // 对应cmd
    "param": {                      // 对应body
        // some params
    }
}
```

#### 应答

应答类消息(ack)一般为服务器回复客户端的请求.

```
// success
{
    "cmd": XXX_MSG_ID | ID_ACK,
    "param": {
        // some param
    }
}
// error
{
    "cmd": XXX_MSG_ID | ID_ACK,
    "param": {
        "error": XXX_INT_CODE,     // int 类型的错误码
        "desc": "error desc"       // str 类型的错误描述, 不一定有
        // maybe some param
    }
}
```

#### 通知

通知类消息(ntf)一般为服务器主动推送的消息, 理论上来讲服务器会在客户端需要知道某些事件的时候进行主动推送, 客户端不应该对推送做过多的预期.

```
{
    "cmd": XXX_MSG_ID | ID_NTF,
    "param": {
        // some param
    }
}
```
