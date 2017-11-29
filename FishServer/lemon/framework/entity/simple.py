#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-02-15

from framework.core.tasklet.tasklet import BasicTasklet


class SimpleTasklet(BasicTasklet):
    def __init__(self, start_routine):
        self.start_routine = start_routine

    def handle(self, *args, **kwargs):
        self.start_routine(*args, **kwargs)
