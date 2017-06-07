# -*- coding: utf-8 -*-
"""
Тесты моделей данных
"""

import unittest
import os
from application import app, db
from application.models import Message, Code, Chat


class BaseTestModel(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['TEST_DATABASE_URL']
        app.config['TEST_MODE'] = True
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestChatModel(BaseTestModel):

    def test_available_chat(self):
        chat = Chat("some", "P++")
        self.assertTrue(hasattr(chat, "id"))
        self.assertTrue(hasattr(chat, "name"))

    def test_type_model_chat(self):
        self.assertIsInstance(Chat.id.type, db.Integer)
        self.assertIsInstance(Chat.name.type, db.String)


class TestMessageModel(BaseTestModel):

    def test_available_message(self):
        message = Message("content", "author", 1, "sys")
        self.assertTrue(hasattr(message, "id"))
        self.assertTrue(hasattr(message, "content"))
        self.assertTrue(hasattr(message, "author"))
        self.assertTrue(hasattr(message, "chat_link"))
        self.assertTrue(hasattr(message, "type"))

    def test_type_model_message(self):
        self.assertIsInstance(Message.id.type, db.Integer)
        self.assertIsInstance(Message.content.type, db.Text)
        self.assertIsInstance(Message.author.type, db.String)
        self.assertIsInstance(Message.chat_link.type, db.Integer)
        self.assertIsInstance(Message.type.type, db.String)


class TestCodeModel(BaseTestModel):

    def test_available_code(self):
        code = Code("content", "author", 1, None)
        self.assertTrue(hasattr(code, "id"))
        self.assertTrue(hasattr(code, "content"))
        self.assertTrue(hasattr(code, "author"))
        self.assertTrue(hasattr(code, "message"))
        self.assertTrue(hasattr(code, "chat_link"))
        self.assertTrue(hasattr(code, "parent_link"))

    def test_type_model_code(self):
        self.assertIsInstance(Code.id.type, db.Integer)
        self.assertIsInstance(Code.content.type, db.Text)
        self.assertIsInstance(Code.author.type, db.String)
        self.assertIsInstance(Code.message.type, db.String)
        self.assertIsInstance(Code.chat_link.type, db.Integer)
        self.assertIsInstance(Code.parent_link.type, db.Integer)


