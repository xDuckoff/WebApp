# -*- coding: utf-8 -*-

"""Тесты роутов"""

from base_test_model import BaseTestModel
from application import app
from application.models import Chat, User, Message, Code
from mock import Mock

MAIN_PAGE_URL = "/"
CHAT_PAGE_URL = "/chat/{chat_id}"
LOGOUT_PAGE_URL = "/logout"
JOIN_CHAT_PAGE_URL = '/join_chat?chat={chat_id}'
TREE_PAGE_URL = '/tree?chat={chat_id}'
GET_MESSAGES_PAGE_URL = '/tree?chat={chat_id}'
TRANSLATE_PAGE_URL = '/translate?chat={chat_id}&index={message_id}'
SEND_CODE_PAGE_URL = '/send_code?chat={chat_id}&code={code}&parent={parent}&cname={cname}'
GET_CODE_PAGE_URL = '/get_code?index={code_id}'
GET_CHAT_INFO_PAGE_URL = '/get_chat_info?chat={chat_id}'
SEND_MESSAGE_PAGE_URL = '/send_message?chat={chat_id}&message={message}'

CHAT_NAME = 'Test Chat'
CHAT_CODE = 'Test Code'
CODE_TYPE = "Test++"
USERNAME = 'Bot'
MESSAGE = 'Hello, I am **Bot**!'
CODE = 'from test import test'
COMMIT_MESSAGE = "Tester commit"


class TestPages(BaseTestModel):

    @staticmethod
    def set_login(value):
        real = User
        real.is_logined = Mock()
        real.is_logined.return_value = value

    def setUp(self):
        BaseTestModel.setUp(self)
        self.app = app.test_client()
        real = User
        real.check_csrf = Mock()
        real.get_login = Mock()
        real.get_login.return_value = USERNAME

    def test_logout(self):
        real = User
        real.logout = Mock()
        response = self.app.get(LOGOUT_PAGE_URL)
        self.assertEqual(response.status_code, 302)

    def test_index_page(self):
        response = self.app.get(MAIN_PAGE_URL)
        self.assertEqual(response.status_code, 200)

    def test_login_required(self):
        TestPages.set_login(True)
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
        chat_page_url = CHAT_PAGE_URL.format(chat_id=chat_id)
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 200)
        TestPages.set_login(False)
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 302)

    def test_uncreated_chat_page_not_be_exist(self):
        TestPages.set_login(True)
        chat_page_url = CHAT_PAGE_URL.format(chat_id=1)
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 302)

    def test_join_in_correct_chat(self):
        TestPages.set_login(True)
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
        response = self.app.get(JOIN_CHAT_PAGE_URL.format(chat_id=chat_id))
        self.assertEqual(response.status_code, 200)

    def test_get_tree(self):
        TestPages.set_login(True)
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
        response = self.app.get(TREE_PAGE_URL.format(chat_id=chat_id))
        self.assertEqual(response.status_code, 200)

    def test_get_messages(self):
        TestPages.set_login(True)
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
        response = self.app.get(GET_MESSAGES_PAGE_URL.format(chat_id=chat_id))
        self.assertEqual(response.status_code, 200)

    def test_translate_page(self):
        TestPages.set_login(True)
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
        Message.send(chat_id, MESSAGE, 'usr', USERNAME)
        response = self.app.get(TRANSLATE_PAGE_URL.format(chat_id=chat_id, message_id=1))
        self.assertEqual(response.status_code, 200)

    def test_send_code(self):
        TestPages.set_login(True)
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
        response = self.app.get(SEND_CODE_PAGE_URL.format(chat_id=chat_id, code=CODE, parent=1, cname=COMMIT_MESSAGE))
        self.assertEqual(response.status_code, 200)

    def test_get_code(self):
        TestPages.set_login(True)
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
        code_id = Code.send(chat_id, CODE, USERNAME, 1, COMMIT_MESSAGE)
        response = self.app.get(GET_CODE_PAGE_URL.format(code_id=code_id))
        self.assertEqual(response.status_code, 200)

    def test_send_message_without_sockets(self):
        TestPages.set_login(True)
        app.config['SOCKET_MODE'] = 'False'
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
        response = self.app.get(SEND_MESSAGE_PAGE_URL.format(chat_id=chat_id, message=MESSAGE))
        self.assertEqual(response.status_code, 200)
