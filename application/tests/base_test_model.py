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
MAIN_PAGE_URL = "/"
CHAT_PAGE_URL = "/chat/{chat_id}"
LOGOUT_PAGE_URL = "/logout"
JOIN_CHAT_PAGE_URL = '/join_chat?chat={chat_id}'
TREE_PAGE_URL = '/tree?chat={chat_id}'
GET_MESSAGES_PAGE_URL = '/tree?chat={chat_id}'
SEND_CODE_PAGE_URL = '/send_code?chat={chat_id}&code={code}&parent={parent}&cname={cname}'
GET_CODE_PAGE_URL = '/get_code?index={code_id}'
GET_CHAT_INFO_PAGE_URL = '/get_chat_info?chat={chat_id}'
SEND_MESSAGE_PAGE_URL = '/send_message?chat={chat_id}&message={message}'
DOCS_PAGE_URL = '/documentation/index.html'


class BaseTestModel(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['TEST_DATABASE_URL']
        db.create_all()
        app.config['SOCKET_MODE'] = 'True'
        self.real = User
        self.real.check_csrf = Mock()
        self.real.get_login = Mock()
        self.real.get_login.return_value = USERNAME
        self.real.is_logined = Mock()
        self.real.is_logined.return_value = True

    def tearDown(self):
        db.session.remove()
        db.drop_all()
