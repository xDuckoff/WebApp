# -*- coding: utf-8 -*-

"""Тесты роутов"""

from base_test_model import *
from application import app
from application.models import Chat, Message, Code
from mock import Mock
from os import system

MAIN_PAGE_URL = "/"
LOGOUT_PAGE_URL = "/logout"
DOCS_PAGE_URL = '/documentation/index.html'
TREE_PAGE_URL = '/tree?chat={chat_id}'
CHAT_PAGE_URL = "/chat/{chat_id}"
CHAT_GET_INFO_PAGE_URL = '/get_chat_info?chat={chat_id}'
CHAT_JOIN_PAGE_URL = '/join_chat?chat={chat_id}'
CODE_SEND_PAGE_URL = '/send_code?chat={chat_id}&code={code}&parent={parent}&cname={cname}'
CODE_GET_PAGE_URL = '/get_code?index={code_id}'
MESSAGES_GET_PAGE_URL = '/get_messages?chat_id={chat_id}'
MESSAGES_GET_LAST_PAGE_URL = '/get_messages?chat_id={chat_id}&last_message_id={last_message_id}'
MESSAGE_SEND_PAGE_URL = '/send_message?chat={chat_id}&message={message}'


class BaseTestPages(BaseTestModel):

    def setUp(self):
        BaseTestModel.setUp(self)
        self.app = app.test_client()


class TestMainPages(BaseTestPages):

    def test_logout(self):
        self.real.logout = Mock()
        response = self.app.get(LOGOUT_PAGE_URL)
        self.assertEqual(response.status_code, 302)

    def test_index_page(self):
        response = self.app.get(MAIN_PAGE_URL)
        self.assertEqual(response.status_code, 200)


class TestChatPage(BaseTestPages):

    def test_access_chat_page_with_login(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        chat_page_url = CHAT_PAGE_URL.format(chat_id=chat_id)
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 200)

    def test_deny_chat_page_without_login(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        chat_page_url = CHAT_PAGE_URL.format(chat_id=chat_id)
        self.real.is_logined.return_value = False
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 302)

    def test_uncreated_chat_page_not_be_exist(self):
        chat_page_url = CHAT_PAGE_URL.format(chat_id=1)
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 302)

    def test_join_in_correct_chat(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        response = self.app.get(CHAT_JOIN_PAGE_URL.format(chat_id=chat_id))
        self.assertEqual(response.status_code, 200)


class TestMessagePage(BaseTestPages):

    def test_get_messages(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        response = self.app.get(MESSAGES_GET_PAGE_URL.format(chat_id=chat_id))
        self.assertEqual(response.status_code, 200)

    def test_get_last_messages(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        last_message = Message.send(chat_id, MESSAGE, MESSAGE_TYPE)
        url = MESSAGES_GET_LAST_PAGE_URL.format(chat_id=chat_id, last_message_id=last_message.id)
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

    def test_deny_get_last_messages_without_login(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        last_message = Message.send(chat_id, MESSAGE, MESSAGE_TYPE)
        url = MESSAGES_GET_LAST_PAGE_URL.format(chat_id=chat_id, last_message_id=last_message.id)
        self.real.is_logined.return_value = False
        response = self.app.get(url)
        self.assertEqual(response.status_code, 302)

    def test_send_message_without_sockets(self):
        app.config['SOCKET_MODE'] = 'False'
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        response = self.app.get(MESSAGE_SEND_PAGE_URL.format(chat_id=chat_id, message=MESSAGE))
        self.assertEqual(response.status_code, 200)

    def test_get_tree(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        response = self.app.get(TREE_PAGE_URL.format(chat_id=chat_id))
        self.assertEqual(response.status_code, 200)


class TestCodePage(BaseTestPages):

    def test_send_code(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        send_code_format_values = {
            "chat_id": chat_id,
            "code": CODE,
            "parent": 1,
            "cname": COMMIT_MESSAGE
        }
        send_code_url = CODE_SEND_PAGE_URL.format(**send_code_format_values)
        response = self.app.get(send_code_url)
        self.assertEqual(response.status_code, 200)

    def test_get_code(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        code_id = Code.send(chat_id, CODE, 1, COMMIT_MESSAGE)
        response = self.app.get(CODE_GET_PAGE_URL.format(code_id=code_id))
        self.assertEqual(response.status_code, 200)
