# -*- coding: utf-8 -*-

"""Конфигурация проекта"""

import os

CSRF_ENABLED = True
SECRET_KEY = '1+$VEPUx@pTtn@s$$$$$woRt'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = ['c', 'cs', 'cpp', 'css', 'html', 'java', 'js', 'py']
ALLOWED_LANGUAGES = [
    {
        "id": 1,
        "name": 'C',
        "extension": 'c',
        "type": 'text/x-csrc'
    },
    {
        "id": 2,
        "name": 'C#',
        "extension": 'cs',
        "type": 'text/x-csharp'
    },
    {
        "id": 3,
        "name": 'C++',
        "extension": 'cpp',
        "type": 'text/x-c++src'
        },
    {
        "id": 4,
        "name": 'CSS',
        "extension": 'css',
        "type": 'text/css'
    },
    {
        "id": 5,
        "name": 'HTML',
        "extension": 'html',
        "type": 'text/html'
    },
    {
        "id": 6,
        "name": 'Java',
        "extension": 'java',
        "type": 'text/x-java'
    },
    {
        "id": 7,
        "name": 'JavaScript',
        "extension": 'js',
        "type": 'text/javascript'
    },
    {
        "id": 8,
        "name": 'Python',
        "extension": 'py',
        "type": 'text/x-python'
    }
]
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SOCKET_MODE = os.environ['SOCKET_MODE']
RECAPTCHA_ENABLED = True
RECAPTCHA_SITE_KEY = "6Lf1eCUUAAAAANoxJbNS7FJMKrFiuQdpKsjzbTQP"
RECAPTCHA_SECRET_KEY = "6Lf1eCUUAAAAAOe7N9op8i9KvY2zCYbgVHNZGNBX"
RECAPTCHA_THEME = "dark"
RECAPTCHA_TYPE = "image"
RECAPTCHA_SIZE = "compact"
RECAPTCHA_RTABINDEX = 10
