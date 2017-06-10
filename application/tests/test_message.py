# -*- coding: utf-8 -*-

"""Тесты сообщений"""

from base_test_model import BaseTestModel
from application.models import Message, Chat

USERNAME = 'Bot'
CHAT_NAME = 'Test Chat'
CHAT_CODE = 'Test Code'
CODE_TYPE = "Test++"
MESSAGE = 'Hello, I am **Bot**!'
CORRECT_MESSAGE = '<p>Hello, I am <strong>Bot</strong>!</p>'
PLAIN_MESSAGE = 'Hello, I am Bot !'
MESSAGE_ESCAPE = """&lt;p&gt;Hello, I am &lt;strong&gt;Bot&lt;/strong&gt;!&lt;/p&gt;"""


class TestMessage(BaseTestModel):

    def setUp(self):
        BaseTestModel.setUp(self)
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
        self.message = Message.send(chat_id, MESSAGE, 'usr', USERNAME)

    def test_translate(self):
        translated_message = self.message.translate()
        self.assertEqual(translated_message.get('no'), CORRECT_MESSAGE)

    def test_plain(self):
        self.assertEqual(self.message.plain(), PLAIN_MESSAGE)

    def test_escape(self):
        self.assertEqual(Message.escape(self.message.content), MESSAGE_ESCAPE)

    def test_get_info(self):
        message_info = self.message.get_info(USERNAME)
        self.assertEqual(message_info.get('message'), CORRECT_MESSAGE)
        self.assertEqual(message_info.get('plain_message'), PLAIN_MESSAGE)
        self.assertEqual(message_info.get('author'), USERNAME)
        self.assertEqual(message_info.get('type'), 'mine')
