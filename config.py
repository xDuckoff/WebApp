# -*- coding: utf-8 -*-

"""Конфигурация проекта"""

import os

CSRF_ENABLED = True
SECRET_KEY = '1+$VEPUx@pTtn@s$$$$$woRt'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = ['c', 'cs', 'cpp', 'css', 'html', 'java', 'js', 'py']
ALLOWED_LANGUAGES = ['C', 'C#', 'C++', 'CSS', 'HTML', 'Java', 'JavaScript', 'Python']
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SOCKET_MODE = os.environ['SOCKET_MODE']
