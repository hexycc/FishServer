#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-02-13

import struct

from tcp import BasicTcpProtocol
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet.protocol import connectionDone
from twisted.protocols.basic import _PauseableMixin

from framework.context import Context
from framework.entity.const import Message
from framework.entity.manager import TaskManager
from framework.entity.msgpack import MsgPack
from framework.util.locker import Locker
from framework.util.log import Logger
from framework.util.tool import Time


class ServerTcpProtocol(BasicTcpProtocol, _PauseableMixin):
    def __init__(self):
        BasicTcpProtocol.__init__(self)
        self._data = ''
        self.access_ts = Time.current_ts()

    def dataReceived(self, data):
        self._data += data
        while len(self._data) > 8:
            cmd, msg_len = struct.unpack('II', self._data[:8])
            if msg_len > len(self._data) - 8:
                return
            body_data = self._data[8:8 + msg_len]
            self._data = self._data[8 + msg_len:]
            try:
                self.access_ts = Time.current_ts()
                tasklet = self.makeTasklet(cmd, body_data, self)
                TaskManager.add_task(tasklet.run, peer=self.peer_key)
            except Exception, e:
                Logger.exception(body_data)
                self.transport.loseConnection()
        TaskManager.schedule()
        return False

    def makeTasklet(self, cmd, raw, connection):
        raise NotImplementedError


class InnerServerProtocol(ServerTcpProtocol):
    @property
    def peer_key(self):
        return 'SERVER'


class OuterServerProtocol(ServerTcpProtocol):
    def __init__(self):
        ServerTcpProtocol.__init__(self)
        self.userId = 0
        self.gameId = 0
        self.room = None
        self.locker = Locker()

    @property
    def peer_key(self):
        return 'CLIENT[%s]' % self.userId

    def connectionLost(self, reason=connectionDone):
        try:
            Logger.info('ConnectionLost', 'userId =', self.userId)
            if self.userId > 0:
                msg = MsgPack(Message.MSG_INNER_BROKEN)
                if self.userId in Context.GData.map_client_connect:
                    del Context.GData.map_client_connect[self.userId]
                msg.set_param('userId', self.userId)
                if self.gameId > 0:
                    msg.set_param('gameId', self.gameId)
                tasklet = self.makeTasklet(Message.MSG_INNER_BROKEN, msg, self)
                TaskManager.add_task(tasklet.run)
            else:
                Logger.debug_network('empty user connection lost ... ')
        except Exception, e:
            Logger.exception()

    def terminate_connection(self):
        if self.userId > 0:
            if self.userId in Context.GData.map_client_connect:
                del Context.GData.map_client_connect[self.userId]
            msg = MsgPack(Message.MSG_INNER_BROKEN)
            msg.set_param('userId', self.userId)
            if self.gameId > 0:
                msg.set_param('gameId', self.gameId)
            tasklet = self.makeTasklet(Message.MSG_INNER_BROKEN, msg, self)
            TaskManager.run_task(tasklet)
            self.logout()
        self.transport.loseConnection()

    def has_login(self):
        return self.userId > 0

    def login(self, uid, gid):
        self.userId = uid
        self.gameId = gid

    def logout(self):
        self.userId = 0
        self.gameId = 0
        self.room = None

    def bind_game(self, gid, room=None):
        self.gameId = gid
        self.room = room


class TcpClientProtocol(BasicTcpProtocol):
    @property
    def peer_key(self):
        return 'SERVER[%s]' % self.factory.peer_server_id

    def connectionMade(self):
        BasicTcpProtocol.connectionMade(self)
        Logger.info('tcp client connect made', self.factory.peer_server_id)
        Context.GData.map_server_connect[self.factory.peer_server_id] = self


class TcpClientFactory(ReconnectingClientFactory):
    protocol = TcpClientProtocol
    maxDelay = 0.5
    initialDelay = 0.01

    def __init__(self, peer_server_id, peer_host, peer_port):
        self.peer_server_id = peer_server_id
        self.peer_host = peer_host
        self.peer_port = peer_port

    def buildProtocol(self, addr):
        self.resetDelay()
        return ReconnectingClientFactory.buildProtocol(self, addr)

    def clientConnectionFailed(self, connector, reason):
        Logger.error('tcp client connect failed', self.peer_server_id)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, unused_reason):
        Logger.info('tcp client connect lost', self.peer_server_id)
        ReconnectingClientFactory.clientConnectionLost(self, connector, unused_reason)
