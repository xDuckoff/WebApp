import unittest
import os
import flask_migrate
from application import chat
from application import app

TEST_DB = 'test'
PATH_TO_DATABASE = os.path.join(os.path.abspath(os.path.curdir), TEST_DB + ".sqlite")

USERNAME = 'Bot'
CHAT_NAME = 'Test Chat'
CHAT_CODE = 'Test Code'
TEST_MESSAGE = 'Hello, I am Bot!'
TEST_CODE = 'from test import test'
CHAT_ID = 0


class TestBaseChatFunctions(unittest.TestCase):

    def setUp(self):
        global CHAT_ID
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + PATH_TO_DATABASE
        with app.app_context():
            flask_migrate.upgrade()
        CHAT_ID = chat.create_chat(CHAT_NAME, CHAT_CODE, USERNAME)
        self.assertEquals(chat.get_chat_info(CHAT_ID), {'name': CHAT_NAME})
        self.assertEquals(chat.get_code(CHAT_ID, 0), {'author': USERNAME, 'code': CHAT_CODE})

    def tearDown(self):
        os.remove(PATH_TO_DATABASE)

    def test_message_sending(self):
        chat.send_message(CHAT_ID, TEST_MESSAGE, 'usr', USERNAME)
        self.assertEquals(chat.get_messages(CHAT_ID, USERNAME)[-1], {'message': TEST_MESSAGE, 'type': 'mine', 'author': USERNAME})

    def test_code_sending(self):
        chat.send_code(CHAT_ID, TEST_CODE, USERNAME, 0)
        self.assertEquals(chat.get_code(CHAT_ID, 1), {"author": USERNAME, "code": TEST_CODE})
