# -*- coding: utf-8 -*-

"""Тесты методов сообщений"""

from base_test_model import *
from application import app, db, socketio
from application.models import Message, Chat, MarkdownMixin
from mock import patch


class TestMessageModel(BaseTestModel):

    def setUp(self):
        BaseTestModel.setUp(self)
        self.chat_id = Chat.create(CHAT_NAME)
        self.message = Message.send(self.chat_id, MESSAGE, MESSAGE_TYPE)

    def test_available_message(self):
        self.assertTrue(hasattr(Message, "id"))
        self.assertTrue(hasattr(Message, "content"))
        self.assertTrue(hasattr(Message, "author"))
        self.assertTrue(hasattr(Message, "chat_link"))
        self.assertTrue(hasattr(Message, "type"))
        self.assertTrue(hasattr(Message, "create_time"))
        self.assertTrue(hasattr(Message, "remove_time"))

    def test_type_model_message(self):
        self.assertIsInstance(Message.id.type, db.Integer)
        self.assertIsInstance(Message.content.type, db.Text)
        self.assertIsInstance(Message.author.type, db.String)
        self.assertIsInstance(Message.chat_link.type, db.Integer)
        self.assertIsInstance(Message.type.type, db.String)
        self.assertIsInstance(Message.remove_time.type, db.DateTime)
        self.assertIsInstance(Message.create_time.type, db.DateTime)

    def test_message_sending(self):
        message = Message.send(self.chat_id, MESSAGE, MESSAGE_TYPE)
        self.assertIsInstance(message, Message)
        self.assertEqual(message.content, MarkdownMixin.decode(MESSAGE))
        self.assertEqual(message.author, USERNAME)
        self.assertEqual(message.chat_link, self.chat_id)
        self.assertEqual(message.type, MESSAGE_TYPE)

    def test_socket_emit_when_message_sending(self):
        with patch.object(socketio, 'emit') as socketio_emit:
            Message.send(self.chat_id, MESSAGE, MESSAGE_TYPE)
        socketio_emit.assert_called()

    def test_socket_not_emit_when_message_sending_and_app_not_in_socket(self):
        with patch.object(socketio, 'emit') as socketio_emit:
            app.config['SOCKET_MODE'] = 'False'
            Message.send(self.chat_id, MESSAGE, MESSAGE_TYPE)
        socketio_emit.assert_not_called()

    def test_message_plain(self):
        self.assertEqual(self.message.plain(), PLAIN_MESSAGE)

    def test_get_info_format_output(self):
        message_info = self.message.get_info()
        self.assertIsInstance(message_info, dict)
        self.assertEqual(message_info.get('message'), CORRECT_MESSAGE)
        self.assertEqual(message_info.get('plain_message'), PLAIN_MESSAGE)
        self.assertEqual(message_info.get('author'), USERNAME)

    def test_get_info_should_mine_type(self):
        message_info = self.message.get_info()
        self.assertEqual(message_info.get('type'), 'mine')

    def test_get_info_should_others_type(self):
        other_user = "SOME_LOGIN"
        self.real.get_login.return_value = other_user
        message_info = self.message.get_info()
        self.assertEqual(message_info.get('type'), 'others')
        self.real.get_login.return_value = USERNAME

    def test_get_info_should_system_type(self):
        other_message = Message.send(self.chat_id, MESSAGE, MESSAGE_SYSTEM_TYPE)
        message_info = other_message.get_info()
        self.assertEqual(message_info.get('type'), MESSAGE_SYSTEM_TYPE)
