#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-09-23

from framework.entity import const


class Const(const.Const):
    # 通用错误
    E_USER_LOCKED = -100
    ES_USER_LOCKED = "user locked"
    E_NOT_LOGIN = -101
    ES_NOT_LOGIN = "not login"
    E_EXCEPTION = -102
    ES_EXCEPTION = "internal exception"
    E_BAD_URL = -103
    ES_BAD_URL = "bad url"
    E_BAD_REDIS = -104
    ES_BAD_REDIS = "bad redis"
    E_BAD_CONFIG = -105
    ES_BAD_CONFIG = "bad config"

    # 定义ID类型
    IDTYPE_ROBOT = 10          # 机器人
    IDTYPE_USERNAME = 11       # 用户名登陆
    IDTYPE_GUEST = 12          # 游客用户类型
    IDTYPE_MOBILE = 13         # 手机用户类型

    # 定义密码类型
    PASSWORD_TYPE_TEXT = 0
    PASSWORD_TYPE_MD5 = 1

    SEX_MAN = 0
    SEX_WOMAN = 1

    MAX_AVATAR_NUMBER = 2
    DEFAULT_AVATAR_MAN = ['1']
    DEFAULT_AVATAR_WOMAN = ['2']
    AVATAR_MAN = ['1']
    AVATAR_WOMAN = ['2']
