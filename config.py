# -*- coding: utf-8 -*-

"""Конфигурация проекта"""

import os

CSRF_ENABLED = True
SECRET_KEY = '1+$VEPUx@pTtn@s$$$$$woRt'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = ['c', 'cs', 'cpp', 'css', 'html', 'java', 'js', 'py']
SQLALCHEMY_TRACK_MODIFICATIONS = True
API_KEY = 'trnsl.1.1.20170509T105702Z.5fff1e2012a2821c.d9e228383bdb15f6648bf1a4960d7f40efe3fc43'
YA_TL_URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SOCKET_MODE = os.environ['SOCKET_MODE']
