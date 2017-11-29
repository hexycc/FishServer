#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-10-26

from framework.private.service import Service
from framework.private.protocols import GameInnerServerProtocol
from framework.private.protocols import EntityInnerProtocol
from framework.private.protocols import QuickInnerProtocol
from framework.private.protocols import ConnectInnerProtocol
from framework.private.protocols import ConnectOuterProtocol
from framework.private.protocols import SdkHttpFactory
from framework.private.protocols import GameHttpFactory
from framework.private.protocols import InnerHttpProtocol
from framework.private.protocols import ShellHttpFactory
from framework.private.protocols import InnerShellProtocol


def run_as_game():
    service = Service(innerProtocol=GameInnerServerProtocol)
    service.start()


def run_as_entity():
    service = Service(innerProtocol=EntityInnerProtocol)
    service.start()


def run_as_quick():
    service = Service(innerProtocol=QuickInnerProtocol)
    service.start()


def run_as_connect():
    service = Service(innerProtocol=ConnectInnerProtocol, outerProtocol=ConnectOuterProtocol)
    service.start()


def run_as_sdk():
    service = Service(httpFactory=SdkHttpFactory)
    service.start()


def run_as_http():
    service = Service(innerProtocol=InnerHttpProtocol, httpFactory=GameHttpFactory)
    service.start()


def run_as_shell():
    service = Service(innerProtocol=InnerShellProtocol, httpFactory=ShellHttpFactory)
    service.start()
