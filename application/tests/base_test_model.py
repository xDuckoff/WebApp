# -*- coding: utf-8 -*-

"""Стандартный класс тестов"""

import unittest
import os
from application import app, db
from mock import Mock
from application.models import User

USERNAME = 'Bot'
CHAT_NAME = 'Test Chat'
CHAT_CODE = 'Test Code'
CHAT_ACCESS_KEY = 'secret_password'
CHAT_INCORRECT_ACCESS_KEY = 'password'
MESSAGE = 'Hello, I am **Bot**!'
CORRECT_MESSAGE = '<p>Hello, I am <strong>Bot</strong>!</p>'
PLAIN_MESSAGE = 'Hello, I am Bot !'
CODE = 'from test import test'
CODE_TYPE = "Test++"
PARENT_CODE_ID = None
COMMIT_MESSAGE = "Tester commit"
START_COMMIT_MESSAGE = u'Начальная версия'
NODE_MARKUP = "<div class=\"commit_node circle unchosen\" data-id=\"{id}\">{id}</div>"
MESSAGE_ESCAPE = """&lt;p&gt;Hello, I am &lt;strong&gt;Bot&lt;/strong&gt;!&lt;/p&gt;"""
MESSAGE_TYPE = 'usr'
MESSAGE_SYSTEM_TYPE = 'sys'


class BaseTestModel(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['TEST_DATABASE_URL']
        db.create_all()
        app.config['SOCKET_MODE'] = 'True'
        self.real = User
        self.real.check_csrf = Mock()
        self.real.get_access_key = Mock()
        self.real.get_access_key.return_value = CHAT_ACCESS_KEY
        self.real.get_login = Mock()
        self.real.get_login.return_value = USERNAME

    def tearDown(self):
        db.session.remove()
        db.drop_all()
