## 环境配置

### 系统

```
[mc@localhost ~]$ cat /etc/redhat-release 
CentOS release 6.6 (Final)
```
`CentOS release 6.5`也行, 根据系统调整`net.core.somaxconn`这个值

### 软件

#### 库

```
yum install epel -y
yum install -y nginx lrzsz git
gcc gcc-c++ python-devel uuid-devel libuuid-devel tcl lua-devel libevent-devel hiredis-devel ctags vim pcre-devel pcre-static zlib zlib-devel zlib-static
```

#### gcc

```
[mc@localhost ~]$ gcc -v
使用内建 specs。
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/local/libexec/gcc/x86_64-unknown-linux-gnu/4.9.2/lto-wrapper
目标：x86_64-unknown-linux-gnu
配置为：../gcc-4.9.2/configure --enable-checking=release --enable-languages=c,c++ --disable-multilib
线程模型：posix
gcc 版本 4.9.2 (GCC)
```

#### pypy

```
[mc@localhost ~]$ pypy
Python 2.7.9 (295ee98b69288471b0fcf2e0ede82ce5209eb90b, Jul 19 2015, 04:35:42)
[PyPy 2.6.0 with GCC 4.4.7 20120313 (Red Hat 4.4.7-11)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>>
```
请把编译后的`pypy`放到`/usr/local/bin/`下, 目录结构如下所示:
```
[ysl@localhost bin]$ pwd
/usr/local/bin/pypy-2.6.0/bin
[ysl@localhost bin]$ ll pypy
lrwxrwxrwx. 1 root root 6 Jul 20 10:00 pypy -> pypy-c
```
在`/etc/bashrc`中加入:
```
export PATH=/usr/local/bin/pypy-2.6.0/bin:$PATH
ulimit -c unlimited
export PYTHONPATH=$PYTHONPATH:~/bin/sdk:~/bin/script
```

#### pip

```
[root@localhost ~]# cd /usr/local/bin/pypy-2.6.0/bin
[root@localhost bin]# wget http://yisilong.qiniudn.com/script/get-pip.py
[root@localhost bin]# ./pypy get-pip.py
[root@localhost bin]# ./pip install -U pip
[root@localhost bin]# ./pip install pycrypto redis requests uwsgi web.py xmltodict twisted
```

#### log4cplus


修改`include/log4cplus/config.hxx`的109行,   `LOG4CPLUS_HAVE_RVALUE_REFS`修改为`LOG4CPLUS_HAVE_RVALUE_REFS_`,  默认编译安装

#### nginx

`nginx`是`yum`安装的, 你们随意:
```
[mc@localhost ~]$ nginx -V
nginx version: nginx/1.0.15
built by gcc 4.4.7 20120313 (Red Hat 4.4.7-11) (GCC) 
TLS SNI support enabled
configure arguments: --prefix=/usr/share/nginx --sbin-path=/usr/sbin/nginx --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --http-client-body-temp-path=/var/lib/nginx/tmp/client_body --http-proxy-temp-path=/var/lib/nginx/tmp/proxy --http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi --http-uwsgi-temp-path=/var/lib/nginx/tmp/uwsgi --http-scgi-temp-path=/var/lib/nginx/tmp/scgi --pid-path=/var/run/nginx.pid --lock-path=/var/lock/subsys/nginx --user=nginx --group=nginx --with-file-aio --with-ipv6 --with-http_ssl_module --with-http_realip_module --with-http_addition_module --with-http_xslt_module --with-http_image_filter_module --with-http_geoip_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_degradation_module --with-http_stub_status_module --with-http_perl_module --with-mail --with-mail_ssl_module --with-debug --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic' --with-ld-opt=-Wl,-E
```

## 服务器说明

### 概述

目前游戏服务器分为sdk, game和脚本三块.

1. sdk主要是处理登陆以及一系列http相关的请求 
2. game是tcp服务器, 与用户连接的是connect服务器, 后面隐藏game, quick, entity等服务器 
3. 机器人分配和异常回收是两个独立python脚本

sdk和game分别跑在两个账户sdk和game下, 启动等操作有脚本, 运行所需要的资源和程序会copy到~/bin下, 日志在~/log下, 按天滚动, uwsgi日志会按照100m滚动

sdk重启的时候需要重启nginx, 所以需要nginx对应的sudo权限

### 数据库

目前用户的数据全部存在redis中, 数据的备份依赖redis的落地, 建议主从结构, 从上开启aof和rdb双重备份, 这个看你们的需求了. redis使用账户redis启动, 日志相关的也在当前目录. 目前给redis分了13个进程, 便于后续扩展.
```
[mc@localhost ~]$ ps -ef | grep redis
redis     37328      1  0 Aug25 ?        00:40:12 /usr/local/bin/redis-server 172.31.95.15:6379               
redis     37332      1  0 Aug25 ?        00:41:16 /usr/local/bin/redis-server 172.31.95.15:6380               
redis     37336      1  0 Aug25 ?        00:41:09 /usr/local/bin/redis-server 172.31.95.15:6381               
redis     37340      1  0 Aug25 ?        00:41:05 /usr/local/bin/redis-server 172.31.95.15:6382               
redis     37344      1  0 Aug25 ?        00:41:15 /usr/local/bin/redis-server 172.31.95.15:6383               
redis     37348      1  0 Aug25 ?        00:41:16 /usr/local/bin/redis-server 172.31.95.15:6384               
redis     37352      1  0 Aug25 ?        00:41:10 /usr/local/bin/redis-server 172.31.95.15:6385               
redis     37356      1  0 Aug25 ?        00:41:14 /usr/local/bin/redis-server 172.31.95.15:6386               
redis     37360      1  0 Aug25 ?        00:41:16 /usr/local/bin/redis-server 172.31.95.15:6387               
redis     37364      1  0 Aug25 ?        00:40:20 /usr/local/bin/redis-server 172.31.95.15:6400               
redis     37368      1  0 Aug25 ?        00:40:18 /usr/local/bin/redis-server 172.31.95.15:6401               
redis     37372      1  0 Aug25 ?        00:44:29 /usr/local/bin/redis-server 172.31.95.15:6402               
redis     37376      1  0 Aug25 ?        00:58:29 /usr/local/bin/redis-server 172.31.95.15:6403
```
其中6379和6403不需要备份, redis相关脚本在`langang-ddz/script/tool`目录下. 

### 启动

游戏分为sdk和game两个模块, 需要分别启动.

#### sdk

sdk使用nginx+uwsgi+pypy结构, sdk负责登陆, 支付等一系列http相关请求处理. 
sdk使用账户sdk操作, 一般源码放在sdk的家目录下langang-ddz中.

可以在sdk家目录下创建启动(重启)脚本sdk.sh, 内容如下:
```
[sdk@iZ25jp8of0jZ ~]$ cat sdk.sh 
sh langang-ddz/script/sdk.sh -m langang-ddz/script/config/server/online-61.json
```
`online-61.json`文件是服务器配置文件, 所有的行为都依赖于它.  
启动后会创建log和bin文件夹, log为所有的日志目录, bin为copy的所有相关文件.

```
[sdk@iZ25jp8of0jZ ~]$ ls
bin  langang-ddz  log  sdk.sh
[sdk@iZ25jp8of0jZ bin]$ ls
nginx.conf  nginx.sh  output  script  sdk  shell  uwsgi.pid  uwsgi-sdk.sock  uwsgi-webpy.ini  webroot
[sdk@iZ25jp8of0jZ shell]$ ls
kill-sdk-ddz.sh  start-sdk-ddz.sh
```

1. ~/bin/shell中生成的脚本为对应的关闭和启动脚本,
2. output为启动时加载配置时生成的参数文件
3. script, sdk和webroot是copy的~/langang-ddz中的源文件, 就是运行的程序及资源
4. 其他的为配置或者运行的pid等相关文件和脚本

一般来说只需要执行sh sdk.sh就会完成所有的sdk启动(重启)工作, 因为要启动nginx所以sdk需要sudo权限

#### game

game为tcp模块, 处理游戏逻辑相关, 分为connect, quick, entity, game, stat, 脚本dispatch.py和monitor.py

1. connect: 连接, 和客户端连接, 相当于网关代理
2. quick: 分桌相关逻辑
3. entity: 业务逻辑
4. game: 游戏逻辑
5. stat: 与蓝港交互代理
6. dispatch.py: 机器人分配逻辑
7. monitor.py: 异常数据清理逻辑

game使用账户ddz操作, 一般源码放在ddz的家目录下langang-ddz中.

可以在ddz家目录下创建启动(重启)脚本,game.sh, 内容如下:
```
[ddz@iZ25jp8of0jZ ~]$ cat game.sh 
sh langang-ddz/script/game.sh -m langang-ddz/script/config/server/online-61.json
```
`online-61.json`文件是服务器配置文件, 所有的行为都依赖于它. 
启动后会创建log和bin文件夹, log为所有的日志目录, bin为copy的所有相关文件.

```
[ddz@iZ25jp8of0jZ ~]$ ls
bin  game.sh  langang-ddz  log
[ddz@iZ25jp8of0jZ ~]$ cd bin/
[ddz@iZ25jp8of0jZ bin]$ ls
connect-ddz-20006.conf  ddz-entity.so  ddz-match.so           entitysvrd           gamesvrd  quick-ddz-20002.conf  script  shell
connectsvrd             ddz-game.so    entity-ddz-20004.conf  game-ddz-20000.conf  output    quicksvrd             sdk     stat-ddz-20008.conf
[ddz@iZ25jp8of0jZ shell]$ ls
config-iptable.sh          kill-ddz-all.sh           kill-game-ddz-20000.sh   kill-stat-ddz-20008.sh  start-connect-ddz-20006.sh  start-ddz-dispatch.sh  start-entity-ddz-20004.sh  start-quick-ddz-20002.sh
kill-connect-ddz-20006.sh  kill-entity-ddz-20004.sh  kill-quick-ddz-20002.sh  redis-cache-clear.sh    start-ddz-all.sh            start-ddz-monitor.sh   start-game-ddz-20000.sh    start-stat-ddz-20008.sh
```

所有文件解释同sdk, 这里的shell分为每个进程的启动和关闭脚本, start-ddz-all.sh和kill-ddz-all.sh是处理所有相关进程, 如果在某个进程崩溃的时候可以在这里用start-*.sh启动对应的进程.

#### 在线人数

脚本在sdk或者game中的都可以找到`~/langang-ddz/script/tool/cron_mysql.py`. 加入cron定时更新到mysql. 运行实例,`pypy cron_mysql.py 127.0.0.1 6379 0 127.0.0.1 3306 root new-password hello`, 参数为别为: cache库对应的host, port, db 这三个参数可以在启动的配置文件中的配置redis.cache对应找到. 后面四个分别为mysql的host, port, user, passwd, dbname

## 网络权限

#### 蓝港服务器

sdk运行所在ip需要与访问蓝港的gateway, 目前配置是:
```
def langang_url():
    if Global.run_mode == 1:
        return 'http://59.151.49.45:8139/agip'
    elif Global.run_mode == 2:
        return 'http://59.151.49.45:8139/agip'
    else:
        return 'http://113.208.129.53:14594/agip'

def langang_gateway_id():
    if Global.run_mode == 1:
        return 138001
    elif Global.run_mode == 2:
        return 138999
    else:
        return 138999
```
run_mode 正式上线是1, 正式服测试(仿真)是2, 其他是3

#### 斗地主服务器

1. sdk运行环境需要开放端口80, 用于nginx
2. game运行环境需要开放端口connect进程监听地址, 用于客户端连接, 目前就一个进程, 端口是9007
3. sdk和game需要访问redis服务器, 建议内网ip访问
