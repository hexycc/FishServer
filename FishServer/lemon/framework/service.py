#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-03-01


def run():
    from twisted.internet import epollreactor

    epollreactor.install()

    from framework.context import Context

    Context.Global.load_static_data()
    Context.Global.dump_static_info()

    proc_key = Context.Global.proc_key()
    log_path = Context.Global.log_path()
    bi_log_path = Context.Global.bi_log_path()
    from framework import init_log
    init_log(log_path, bi_log_path)
    Context.Log.info('service init with', log_path, proc_key)

    server_type = Context.Global.process_type()
    pid = Context.Global.process_id()
    Context.Log.info('service run', server_type, pid)

    startup = None
    exec 'from private.servers import run_as_%s as startup' % server_type
    startup()


if __name__ == '__main__':
    run()
