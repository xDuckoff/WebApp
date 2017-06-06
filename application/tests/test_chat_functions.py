# -*- coding: utf-8 -*-
"""
Тесты функций чата без сокетов
"""

import unittest
import os
from application import app, db, chat
from application.chat.sockets import init_sockets

USERNAME = 'Bot'
CHAT_NAME = 'Test Chat'
CHAT_CODE = 'Test Code'
MESSAGE = 'Hello, I am <strong>Bot</strong>!'
PLAIN_MESSAGE = 'Hello, I am Bot !'
CODE = 'from test import test'
CODE_TYPE = "Test++"
PARENT_CODE_ID = None
COMMIT_MESSAGE = "Tester commit"


class BaseChatFunctions(unittest.TestCase):
    chat_id = None

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['TEST_DATABASE_URL']
        app.config['SOCKET_MODE'] = 'False'
        app.config['TEST_MODE'] = True
        db.create_all()
        self.chat_id = chat.create_chat(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_chat(self):
        chat_info = chat.get_chat_info(self.chat_id)
        self.assertEquals(chat_info.get('name'), CHAT_NAME)
        self.assertEquals(chat_info.get('code_type'), CODE_TYPE)

    def test_get_messages(self):
        chat.send_message(self.chat_id, MESSAGE, 'usr', USERNAME)
        received_message = chat.get_messages(self.chat_id, USERNAME)[-1]
        self.assertEquals(received_message.get('message'), MESSAGE)
        self.assertEquals(received_message.get('plain_message'), PLAIN_MESSAGE)
        self.assertEquals(received_message.get('type'), 'mine')
        self.assertEquals(received_message.get('author'), USERNAME)

    def test_code_sending(self):
        send_code_id = chat.send_code(self.chat_id, CODE, USERNAME, PARENT_CODE_ID, COMMIT_MESSAGE)
        sent_code = chat.get_code(send_code_id)
        self.assertEquals(sent_code.get('author'), USERNAME)
        self.assertEquals(sent_code.get('code'), CODE)


class BaseChatFunctionsWithSockets(BaseChatFunctions):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['TEST_DATABASE_URL']
        app.config['SOCKET_MODE'] = 'True'
        app.config['TEST_MODE'] = True
        init_sockets()
        db.create_all()
        self.chat_id = chat.create_chat(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
