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
START_COMMIT_MESSAGE = u'Начальная версия'
NODE_MARKUP = "<div class=\"commit_node circle unchosen\" data-id=\"{id}\">{id}</div>"


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

    def test_find_chat(self):
        self.assertGreaterEqual(len(Chat.find(CHAT_NAME)), 1)
        self.assertGreaterEqual(len(Chat.find(str(self.chat_id))), 1)
        self.assertGreaterEqual(len(Chat.find()), 1)

    def test_get_root_in_chat(self):
        code = Code.get_root_in_chat(self.chat_id)
        self.assertEquals(code.author, USERNAME)
        self.assertEquals(code.content, CHAT_CODE)
        self.assertEquals(code.chat_link, self.chat_id)
        self.assertEquals(code.parent_link, None)
        self.assertEquals(code.message, START_COMMIT_MESSAGE)

    def test_get_commits_tree(self):
        tree = Code.get_commits_tree(self.chat_id)
        self.assertEqual(tree.get('text').get('name'), 1)
        self.assertEqual(tree.get('text').get('title'), START_COMMIT_MESSAGE)
        self.assertEqual(tree.get('children'), [])
        self.assertEqual(tree.get('innerHTML'), NODE_MARKUP.format(id=1))

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


class BaseChatFunctionsWithSockets(BaseChatFunctions):

    def setUp(self):
        BaseTestModel.setUp(self)
        app.config['SOCKET_MODE'] = 'True'
        self.chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
