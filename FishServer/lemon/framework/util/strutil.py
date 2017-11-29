#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-16

import urllib


class Strutil(object):
    def __init__(self):
        int62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.__int62dictint__ = {}
        self.__int62dictstr__ = {}
        for i, v in enumerate(int62):
            self.__int62dictint__[i] = v
            self.__int62dictstr__[v] = i

    def to_str62(self, int10, slenfix=0):
        if int10 <= 0:
            s62 = '0'
        else:
            s62 = ''
            while int10 > 0:
                c = self.__int62dictint__[int10 % 62]
                int10 /= 62
                s62 = c + s62

        if slenfix > 0:
            while len(s62) < slenfix:
                s62 = '0' + s62
            if len(s62) > slenfix:
                s62 = s62[-slenfix:]
        return s62

    def to_int10(self, str62):
        int10 = 0
        slen = len(str62)
        for x in xrange(slen):
            m = self.__int62dictstr__[str62[x]]
            if m > 0:
                for _ in xrange(slen - x - 1):
                    m *= 62
            int10 = m + int10
        return int10

    def url_encode(self, query, doseq=0):
        return urllib.urlencode(query, doseq)


Strutil = Strutil()

if __name__ == '__main__':
    print Strutil.to_int10('ZZZ')
    print Strutil.to_str62(238327)
    print Strutil.to_str62(0, 3)
    print Strutil.to_str62(238328, 3)
    print Strutil.to_str62(1447726879)
    print Strutil.to_str62(0)
