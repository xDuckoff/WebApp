# -*- coding: utf-8 -*-

"""Тесты методов чата"""

from base_test_model import *
from application import db
from application.models import Message, Chat, Code


class TestChatModel(BaseTestModel):

    def setUp(self):
        BaseTestModel.setUp(self)
        self.chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)

    def test_available_chat(self):
        self.assertTrue(hasattr(Chat, "id"))
        self.assertTrue(hasattr(Chat, "name"))

    def test_type_model_chat(self):
        self.assertIsInstance(Chat.id.type, db.Integer)
        self.assertIsInstance(Chat.name.type, db.String)

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

    def test_was_chat_created(self):
        self.assertTrue(Chat.was_created(str(self.chat_id)))
        self.assertFalse(Chat.was_created(str(self.chat_id + 1)))

    def test_chat_has_message(self):
        chat = Chat.get(self.chat_id)
        message_id = Message.send(self.chat_id, MESSAGE, 'usr', USERNAME).id - 1
        self.assertTrue(chat.has_message(str(message_id)))
        self.assertFalse(chat.has_message(str(message_id + 1)))

    def test_chat_has_code(self):
        chat = Chat.get(self.chat_id)
        code_id = Code.send(self.chat_id, CODE, USERNAME, PARENT_CODE_ID, COMMIT_MESSAGE) - 1
        self.assertTrue(chat.has_message(str(code_id)))
        self.assertFalse(chat.has_message(str(code_id + 1)))

    def test_find_chat(self):
        self.assertGreaterEqual(len(Chat.find(CHAT_NAME)), 1)
        self.assertGreaterEqual(len(Chat.find(str(self.chat_id))), 1)
        self.assertGreaterEqual(len(Chat.find()), 1)
