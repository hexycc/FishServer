#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-02-13

import socket
import struct

from twisted.internet.protocol import Protocol

from framework.util.log import Logger


class BasicTcpProtocol(Protocol):
    def __init__(self):
        self.peer_host = ''
        self.peer_port = ''

    @property
    def peer_key(self):
        return 'TCP:%s:%s' % (self.peer_host, self.peer_port)

    def connectionMade(self):
        self.peer_host = str(self.transport.getPeer().host)
        self.peer_port = str(self.transport.getPeer().port)
        self.transport.setTcpNoDelay(1)
        self.transport.setTcpKeepAlive(1)
        try:
            sock = self.transport.getHandle()
            sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 30)
            sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 10)
            sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 180)
        except Exception, e:
            Logger.exception('not support TCP_KEEPIDLE')

    def sendMsg(self, cmd, data):
        try:
            Logger.debug_network('==== SEND TCP TO %s:' % self.peer_key, '%08X' % cmd, repr(data))
            if self.transport and self.connected:
                header = struct.pack('II', cmd, len(data))
                self.transport.write(header + data)
                return True
            else:
                Logger.error('==== ERROR: cannot connected !! protocol =', self, '%08X' % cmd, repr(data))
        except Exception, e:
            Logger.exception(data)

        return False
