# -*- coding: utf-8 -*-

"""Тесты роутов"""

from base_test_model import BaseTestModel
from application import app
from application.models import Chat, User
from mock import Mock

MAIN_PAGE_URL = "/"
CHAT_PAGE_URL = "/chat/{chat_id}"
LOGOUT_PAGE_URL = "/logout"
JOIN_CHAT_PAGE_URL = '/join_chat'

CHAT_NAME = 'Test Chat'
CHAT_CODE = 'Test Code'
CODE_TYPE = "Test++"
USERNAME = 'Bot'


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

    def test_should_logout_page_be_exist(self):
        real = User
        real.logout = Mock()
        response = self.app.get(LOGOUT_PAGE_URL)
        self.assertEqual(response.status_code, 302)

    def test_should_index_page_be_exist(self):
        response = self.app.get(MAIN_PAGE_URL)
        self.assertEqual(response.status_code, 200)

    def test_should_chat_page_be_exist_with_login(self):
        TestPages.set_login(True)
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
        chat_page_url = CHAT_PAGE_URL.format(chat_id=chat_id)
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 200)
        TestPages.set_login(False)
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 302)

    def test_should_uncreated_chat_page_not_be_exist(self):
        TestPages.set_login(True)
        chat_page_url = CHAT_PAGE_URL.format(chat_id=1)
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 302)

    def test_join_in_correct_chat(self):
        TestPages.set_login(True)
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)
        response = self.app.get(JOIN_CHAT_PAGE_URL + '?chat={chat_id}'.format(chat_id=chat_id))
        self.assertEqual(response.status_code, 200)
