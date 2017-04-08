import unittest
from application import chat


USERNAME = 'Bot'
CHAT_NAME = 'Test Chat'
CHAT_CODE = 'Test Code'
TEST_MESSAGE = 'Hello, I am Bot!'
TEST_CODE = 'from test import test'
CHAT_ID = 0


class TestBaseChatFunctions(unittest.TestCase):

    def test_chat_creating(self):
        global CHAT_ID
        CHAT_ID = chat.create_chat(CHAT_NAME, CHAT_CODE, USERNAME)
        self.assertEquals(chat.get_chat_info(CHAT_ID), {'name': CHAT_NAME})
        self.assertEquals(chat.get_code(CHAT_ID, 0), {'author': USERNAME, 'code': CHAT_CODE})

    def test_message_sending(self):
        chat.send_message(CHAT_ID, TEST_MESSAGE, 'usr', USERNAME)
        self.assertEquals(chat.get_messages(CHAT_ID, USERNAME)[-1], {'message': TEST_MESSAGE, 'type': 'mine', 'author': USERNAME})

    def test_code_sending(self):
        chat.send_code(CHAT_ID, TEST_CODE, USERNAME)
        self.assertEquals(chat.get_code(CHAT_ID, 1), {"author": USERNAME, "code": TEST_CODE})


unittest.main()
