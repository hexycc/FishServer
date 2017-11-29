#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-02-28

from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory

from framework.context import Context
from framework.core.protocol.tcp.server import TcpClientFactory
from framework.entity.const import FlagType
from framework.entity.manager import TaskManager


class Service(object):
    def __init__(self, innerProtocol=None, outerProtocol=None, httpFactory=None):
        self.__heart_beat = 0
        self.gdata = Context.GData
        self.innerProtocol = innerProtocol
        self.outerProtocol = outerProtocol
        self.httpFactory = httpFactory

        self.log_path = Context.Global.log_path()
        self.proc_key = Context.Global.proc_key()

        datas = self.proc_key.split(':')
        self.redis_host = datas[0]
        self.redis_port = int(datas[1])
        self.redis_db = int(datas[2])
        self.listen_port = int(datas[3])
        self.server_id = int(datas[4])

    def start(self):
        Context.Log.info('service starting ...')

        Context.Log.info('InitParams log file     =', self.log_path)
        Context.Log.info('InitParams proc key     =', self.proc_key)
        Context.Log.info('InitParams redis host   =', self.redis_host)
        Context.Log.info('InitParams redis port   =', self.redis_port)
        Context.Log.info('InitParams redis db     =', self.redis_db)
        Context.Log.info('InitParams listen port  =', self.listen_port)
        Context.Log.info('InitParams server id    =', self.server_id)
        Context.Log.info('InitParams tcpProtocol  =', self.innerProtocol)
        Context.Log.info('InitParams udpProtocol  =', self.outerProtocol)
        Context.Log.info('InitParams httpFactory  =', self.httpFactory)

        Context.Log.info('init tasklet startup ...')
        try:
            TaskManager.add_simple_task(self.start_up)
            TaskManager.start_loop()
            Context.Log.info('service stop ...')
        except Exception, e:
            Context.Log.exception()

    def start_up(self):
        Context.Log.info('init tasklet run ...')
        params = {
            'redis.config': {
                'host': self.redis_host,
                'port': self.redis_port,
                'db': self.redis_db,
            }
        }
        from framework import init_context
        init_context(params['redis.config'])

        self.gdata.server = self
        self.gdata.server_id = self.server_id

        Context.GData.init_data()
        if Context.GData.server_type != FlagType.flag_type_sdk:
            from lemon import init_game
            init_game(Context.GData.server_type)

        if self.innerProtocol:
            self.connect_service()
            if Context.GData.server_type not in (FlagType.flag_type_http, FlagType.flag_type_shell):
                self.listen_inner_tcp(self.listen_port)

        if self.httpFactory:
            self.listen_http(self.listen_port)

        if self.outerProtocol:
            self.listen_tcp(self.listen_port + 1)

        key = 'script:%s:%s:%s' % (self.redis_host, self.redis_port, self.redis_db)
        Context.RedisConfig.hash_set(key, self.proc_key, Context.Time.current_time())
        TaskManager.set_interval(self.server_heart_beat, 3, 10)
        Context.Log.info('service start success ...')

    def connect_service(self):
        self_type = Context.GData.server_type
        for svr_id, svr_info in Context.GData.map_server_info.iteritems():
            if svr_info['type'] not in [self_type, FlagType.flag_type_http,
                                        FlagType.flag_type_shell, FlagType.flag_type_sdk]:
                factory = TcpClientFactory(svr_id, svr_info['host'], svr_info['port'])
                reactor.connectTCP(svr_info['host'], svr_info['port'], factory)

    def listen_inner_tcp(self, port):
        type_str = FlagType.trans_server_type(Context.GData.server_type)
        svr_info = Context.GData.server_info
        Context.Log.info(type_str, 'listen on port', port, 'with', self.innerProtocol)
        factory = ServerFactory()
        factory.protocol = self.innerProtocol
        reactor.listenTCP(port, factory, interface=svr_info['host'])

    def listen_tcp(self, port):
        type_str = FlagType.trans_server_type(Context.GData.server_type)
        Context.Log.info(type_str, 'listen on port', port, 'with', self.outerProtocol)
        factory = ServerFactory()
        factory.protocol = self.outerProtocol
        reactor.listenTCP(port, factory)

    def listen_http(self, port):
        type_str = FlagType.trans_server_type(Context.GData.server_type)
        Context.Log.info(type_str, 'listen on port', port, 'with', self.httpFactory)
        reactor.listenTCP(port, self.httpFactory())

    def server_heart_beat(self):
        self.__heart_beat += 1
        if self.innerProtocol:
            if getattr(self.innerProtocol, 'makeTasklet', None):
                t = self.innerProtocol().makeTasklet(0, None, None)
                if getattr(t, 'on_server_heart_beat', None):
                    TaskManager.add_task(t.on_server_heart_beat)
        TaskManager.add_simple_task(Context.Configure.reload)
