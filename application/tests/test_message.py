# -*- coding: utf-8 -*-

"""Тесты методов сообщений"""

from base_test_model import *
from application import db
from application.models import Message, Chat


class TestMessageModel(BaseTestModel):

    def setUp(self):
        BaseTestModel.setUp(self)
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
        self.message = Message.send(chat_id, MESSAGE, 'usr', USERNAME)

    def test_available_message(self):
        self.assertTrue(hasattr(Message, "id"))
        self.assertTrue(hasattr(Message, "content"))
        self.assertTrue(hasattr(Message, "author"))
        self.assertTrue(hasattr(Message, "chat_link"))
        self.assertTrue(hasattr(Message, "type"))

    def test_type_model_message(self):
        self.assertIsInstance(Message.id.type, db.Integer)
        self.assertIsInstance(Message.content.type, db.Text)
        self.assertIsInstance(Message.author.type, db.String)
        self.assertIsInstance(Message.chat_link.type, db.Integer)
        self.assertIsInstance(Message.type.type, db.String)

    def test_message_translate(self):
        translated_message = self.message.translate()
        self.assertEqual(translated_message.get('no'), CORRECT_MESSAGE)

    def test_message_plain(self):
        self.assertEqual(self.message.plain(), PLAIN_MESSAGE)

    def test_message_escape(self):
        self.assertEqual(Message.escape(self.message.content), MESSAGE_ESCAPE)

    def test_message_get_info(self):
        message_info = self.message.get_info(USERNAME)
        self.assertEqual(message_info.get('message'), CORRECT_MESSAGE)
        self.assertEqual(message_info.get('plain_message'), PLAIN_MESSAGE)
        self.assertEqual(message_info.get('author'), USERNAME)
        self.assertEqual(message_info.get('type'), 'mine')
