#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-02-26

import json
import functools

default_content_type = 'text/plain'


def set_default_content_type(content_type):
    global default_content_type
    default_content_type = content_type


def get_default_result():
    if default_content_type == 'json':
        return JsonResult
    elif default_content_type == 'html':
        return HtmlResult
    elif default_content_type == 'xml':
        return XmlResult
    elif default_content_type == 'text':
        return TextResult


class __Result(object):
    def __init__(self, result, header=None):
        if not isinstance(result, str):
            raise Exception(type(result))
        self.result = result
        self.header = []
        if isinstance(header, str):
            self.header.append(header)
        elif isinstance(header, list):
            self.header.extend(header)

    def add_header(self, line):
        self.header.append(line)

    def get_header(self):
        return self.header

    def get_content_type(self):
        return default_content_type

    def __str__(self):
        return self.result

    def __repr__(self):
        return '%s %s' % (self.get_content_type(), self.__str__())


class XmlResult(__Result):
    def get_content_type(self):
        return 'text/xml'


class TextResult(__Result):
    def get_content_type(self):
        return 'text/plain'


class HtmlResult(__Result):
    def get_content_type(self):
        return 'text/html'


class JsonResult(__Result):
    def __init__(self, result, header=None):
        if isinstance(result, (tuple, list, dict)):
            result = json.dumps(result, separators=(',', ':'))
        super(JsonResult, self).__init__(result, header)

    def get_content_type(self):
        return 'application/json'


def http_response_handle(response='json'):
    def outer_decorator_func(func):
        @functools.wraps(func)
        def inner_decorator_func(*args, **kwargs):
            result = func(*args, **kwargs)
            if response == 'json':
                return JsonResult(result)
            elif response == 'html':
                return HtmlResult(result)
            elif response == 'xml':
                return XmlResult(result)
            elif response == 'text':
                return TextResult(result)
            else:
                return get_default_result()(result)

        return inner_decorator_func

    return outer_decorator_func


def http_response(request, mo, code=None, content_type=None):
    body = str(mo)
    if not content_type:
        try:
            content_type = mo.get_content_type()
        except:
            content_type = default_content_type

    if code:
        request.setResponseCode(code)
    request.setHeader('Content-Type', '%s; charset=utf-8' % content_type)
    request.setHeader('Content-Length', str(len(body)))
    request.setHeader('Access-Control-Allow-Origin', request.get_origin())
    request.setHeader('Access-Control-Allow-Credentials', 'true')
    request.write(body)
    request.finish()
    return body, content_type


def http_response_500(request):
    return http_response(request, '{"error":500,"desc":"System Error"}', 500, 'application/json')


def http_response_404(request):
    return http_response(request, '{"error":404,"desc":"Not Found"}', 404, 'application/json')


def http_response_403(request):
    return http_response(request, '{"error":403,"desc":"Forbidden Access"}', 403, 'application/json')


__all__ = ['XmlResult', 'JsonResult', 'TextResult', 'HtmlResult', 'http_response_handle', 'http_response_500',
           'http_response_404', 'http_response_403']
