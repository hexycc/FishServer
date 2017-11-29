#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-02-19

import urllib
from twisted.web import client
from framework.interface import IContext
from framework.util.log import Logger


class WebPage(IContext):
    def wait_for_page(self, url, postdata=None, query=None, method='POST', headers=None, cookies=None, timeout=6):
        try:
            tips = 'waitForPage' + repr(url[0:10])
        except Exception, e:
            tips = 'waitForPage-errtips'
        if isinstance(url, unicode):
            url = url.encode('utf8')
        if isinstance(query, dict):
            query = urllib.urlencode(query)
        if query:
            url += '?' + query
        if not headers:
            headers = {'Content-type': 'application/x-www-form-urlencoded'}
        if isinstance(postdata, dict):
            postdata = urllib.urlencode(postdata)
        Logger.info('---->', url, method, headers, repr(postdata), timeout)
        d = client.getPage(url, method=method, headers=headers, postdata=postdata, cookies=cookies, timeout=timeout)
        tasklet = self.ctx.tasklet()
        response = tasklet.wait_for_deferred(d, tips)
        Logger.info('<----', url, repr(response))
        return response

    def wait_for_json(self, url, postdata=None, query=None, method='POST', headers=None, cookies=None, timeout=6):
        response = self.wait_for_page(url, postdata, query, method, headers, cookies, timeout)
        return self.ctx.json_loads(response)


WebPage = WebPage()
