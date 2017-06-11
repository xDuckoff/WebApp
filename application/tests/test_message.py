# -*- coding: utf-8 -*-

"""Тесты методов сообщений"""

from base_test_model import *
from application import app, db, socketio
from application.models import Message, Chat
from mock import patch


class TestMessageModel(BaseTestModel):

    def setUp(self):
        BaseTestModel.setUp(self)
        self.chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
        self.message = Message.send(self.chat_id, MESSAGE, MESSAGE_TYPE, USERNAME)

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

    def test_message_sending(self):
        message = Message.send(self.chat_id, MESSAGE, MESSAGE_TYPE, USERNAME)
        self.assertIsInstance(message, Message)
        self.assertEqual(message.content, Message.markdown_decode(MESSAGE))
        self.assertEqual(message.author, USERNAME)
        self.assertEqual(message.chat_link, self.chat_id)
        self.assertEqual(message.type, MESSAGE_TYPE)

    def test_send_message_with_empty_content(self):
        empty_content = ""
        with self.assertRaises(OverflowError):
            Message.send(self.chat_id, empty_content, MESSAGE_TYPE, USERNAME)

    def test_send_message_with_long_content(self):
        long_content = "*" * 1001
        with self.assertRaises(OverflowError):
            Message.send(self.chat_id, long_content, MESSAGE_TYPE, USERNAME)

    def test_socket_emit_when_message_sending(self):
        with patch.object(socketio, 'emit') as socketio_emit:
            Message.send(self.chat_id, MESSAGE, MESSAGE_TYPE, USERNAME)
        socketio_emit.assert_called()

    def test_socket_not_emit_when_message_sending_and_app_not_in_socket(self):
        with patch.object(socketio, 'emit') as socketio_emit:
            app.config['SOCKET_MODE'] = 'False'
            Message.send(self.chat_id, MESSAGE, MESSAGE_TYPE, USERNAME)
        socketio_emit.assert_not_called()

    def test_message_translate(self):
        translated_message = self.message.translate()
        self.assertEqual(translated_message.get('no'), CORRECT_MESSAGE)

    def test_message_plain(self):
        self.assertEqual(self.message.plain(), PLAIN_MESSAGE)

    def test_message_escape(self):
        self.assertEqual(Message.escape(self.message.content), MESSAGE_ESCAPE)

    def test_get_info_format_output(self):
        message_info = self.message.get_info(USERNAME)
        self.assertIsInstance(message_info, dict)
        self.assertEqual(message_info.get('message'), CORRECT_MESSAGE)
        self.assertEqual(message_info.get('plain_message'), PLAIN_MESSAGE)
        self.assertEqual(message_info.get('author'), USERNAME)

    def test_get_info_should_mine_type(self):
        message_info = self.message.get_info(USERNAME)
        self.assertEqual(message_info.get('type'), 'mine')

    def test_get_info_should_others_type(self):
        other_user = "SOME_LOGIN"
        message_info = self.message.get_info(other_user)
        self.assertEqual(message_info.get('type'), 'others')

    def test_get_info_should_system_type(self):
        system_message_type = 'sys'
        other_message = Message.send(self.chat_id, MESSAGE, system_message_type, USERNAME)
        message_info = other_message.get_info(USERNAME)
        self.assertEqual(message_info.get('type'), system_message_type)
