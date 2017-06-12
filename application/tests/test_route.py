# -*- coding: utf-8 -*-

"""Тесты роутов"""

from base_test_model import *
from application import app
from application.models import Chat, Message, Code
from mock import Mock
from os import system


class TestPages(BaseTestModel):

    def setUp(self):
        BaseTestModel.setUp(self)
        self.app = app.test_client()

    def test_logout(self):
        self.real.logout = Mock()
        response = self.app.get(LOGOUT_PAGE_URL)
        self.assertEqual(response.status_code, 302)

    def test_index_page(self):
        response = self.app.get(MAIN_PAGE_URL)
        self.assertEqual(response.status_code, 200)

    def test_login_required(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        chat_page_url = CHAT_PAGE_URL.format(chat_id=chat_id)
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 200)
        self.real.is_logined.return_value = False
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 302)

    def test_uncreated_chat_page_not_be_exist(self):
        chat_page_url = CHAT_PAGE_URL.format(chat_id=1)
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 302)

    def test_join_in_correct_chat(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        response = self.app.get(JOIN_CHAT_PAGE_URL.format(chat_id=chat_id))
        self.assertEqual(response.status_code, 200)

    def test_get_tree(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        response = self.app.get(TREE_PAGE_URL.format(chat_id=chat_id))
        self.assertEqual(response.status_code, 200)

    def test_get_messages(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        response = self.app.get(GET_MESSAGES_PAGE_URL.format(chat_id=chat_id))
        self.assertEqual(response.status_code, 200)

    def test_translate_page(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        Message.send(chat_id, MESSAGE, 'usr')
        response = self.app.get(TRANSLATE_PAGE_URL.format(chat_id=chat_id, message_id=1))
        self.assertEqual(response.status_code, 200)

    def test_send_code(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        send_code_format_values = {
            "chat_id": chat_id,
            "code": CODE,
            "parent": 1,
            "cname": COMMIT_MESSAGE
        }
        send_code_url = SEND_CODE_PAGE_URL.format(**send_code_format_values)
        response = self.app.get(send_code_url)
        self.assertEqual(response.status_code, 200)

    def test_get_code(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        code_id = Code.send(chat_id, CODE, 1, COMMIT_MESSAGE)
        response = self.app.get(GET_CODE_PAGE_URL.format(code_id=code_id))
        self.assertEqual(response.status_code, 200)

    def test_send_message_without_sockets(self):
        app.config['SOCKET_MODE'] = 'False'
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        response = self.app.get(SEND_MESSAGE_PAGE_URL.format(chat_id=chat_id, message=MESSAGE))
        self.assertEqual(response.status_code, 200)

    def test_make_docs(self):
        system("cd docs; make html>/dev/null")
        response = self.app.get(DOCS_PAGE_URL)
        self.assertEqual(response.status_code, 200)
