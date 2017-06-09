# -*- coding: utf-8 -*-

"""Тесты основных функций чата"""

from base_test_model import BaseTestModel
from application import app
from application.models import Chat, Code, Message

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


class BaseChatFunctions(BaseTestModel):

    def setUp(self):
        BaseTestModel.setUp(self)
        app.config['SOCKET_MODE'] = 'False'
        self.chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)

    def test_create_chat(self):
        chat = Chat.get(self.chat_id)
        chat_info = chat.get_info()
        self.assertEquals(chat_info.get('name'), CHAT_NAME)
        self.assertEquals(chat_info.get('code_type'), CODE_TYPE)

    def test_get_messages(self):
        Message.send(self.chat_id, MESSAGE, 'usr', USERNAME)
        chat = Chat.get(self.chat_id)
        received_message = chat.get_messages(USERNAME)[-1]
        self.assertEquals(received_message.get('message'), CORRECT_MESSAGE)
        self.assertEquals(received_message.get('plain_message'), PLAIN_MESSAGE)
        self.assertEquals(received_message.get('type'), 'mine')
        self.assertEquals(received_message.get('author'), USERNAME)

    def test_code_sending(self):
        send_code_id = Code.send(self.chat_id, CODE, USERNAME, PARENT_CODE_ID, COMMIT_MESSAGE)
        sent_code = Code.get(send_code_id)
        self.assertEquals(sent_code.get('author'), USERNAME)
        self.assertEquals(sent_code.get('code'), CODE)


class BaseChatFunctionsWithSockets(BaseChatFunctions):

    def setUp(self):
        BaseTestModel.setUp(self)
        app.config['SOCKET_MODE'] = 'True'
        self.chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
