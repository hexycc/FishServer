#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-18

import re
from binascii import b2a_hex
from binascii import a2b_hex
from Crypto.Cipher import AES
from framework.util.tool import Algorithm


class Entity(object):
    key = 'YZd7SB2yiFBbga5a'
    mode = AES.MODE_CBC

    @classmethod
    def encrypt(cls, text):
        cryptor = AES.new(cls.key, cls.mode, b'0000000000000000')
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            text += ('\0' * add)
        elif count > length:
            add = (length - (count % length))
            text += ('\0' * add)
        ciphertext = cryptor.encrypt(text)
        return b2a_hex(ciphertext)

    @classmethod
    def decrypt(cls, text):
        cryptor = AES.new(cls.key, cls.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

    @classmethod
    def logined(cls, request):
        try:
            if request.getSession().isLogined():
                return True
        except:
            pass
        return False

    @classmethod
    def checkDeviceID(cls, strDeviceID):
        if len(strDeviceID) < 1:
            return False
        return True

    @classmethod
    def checkUserName(cls, strUser):
        if len(strUser) == 0:
            return False
        if strUser.find("select") >= 0:
            return False
        return True

    @classmethod
    def checkPassword(cls, strPass):
        if len(strPass) < 6:
            return False
        strValid = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~!@#$%^&*()_+-=[]{}"
        for c in strPass:
            if c not in strValid:
                return False
        return True

    @classmethod
    def checkNick(cls, nick):
        if len(nick) == 0:
            return False
        if nick.find('select') >= 0:
            return False
        return True

    @classmethod
    def checkEmail(cls, strEmail):
        if len(strEmail) == 0:
            return True
        if strEmail.find("select") >= 0:
            return False
        return re.match(r"^[a-zA-Z0-9]+[a-zA-Z0-9_\.\-]*[a-zA-Z0-9]+@([a-zA-Z0-9]+\.)+[a-zA-Z]{2,}$", strEmail,
                        re.VERBOSE)

    @classmethod
    def checkMobile(cls, strMobile):
        return bool(re.match(r"(1)(\d{10})$", strMobile, re.VERBOSE))

    @classmethod
    def encodePassword(cls, user, passwd):
        if isinstance(user, unicode):
            user = user.encode('utf-8')
        return Algorithm.md5_encode(str(user) + str(passwd))


Entity = Entity()
