# -*- coding: utf-8 -*-

"""Тесты роутов"""

from base_test_model import BaseTestModel
from application import app
from application.models import Chat


class TestPages(BaseTestModel):
    MAIN_PAGE_URL = "/"
    CHAT_PAGE_URL = "/chat/{chat_id}"
    LOGOUT_PAGE_URL = "/logout"

    def setUp(self):
        BaseTestModel.setUp(self)
        self.app = app.test_client()

    def test_should_logout_page_be_exist(self):
        response = self.app.get(TestPages.LOGOUT_PAGE_URL)
        self.assertEqual(response.status_code, 302)

    def test_should_index_page_be_exist(self):
        response = self.app.get(TestPages.MAIN_PAGE_URL)
        self.assertEqual(response.status_code, 200)

    def test_should_chat_page_not_be_exist_without_login(self):
        chat_id = Chat.create("NAME", "CODE", "B++", "NICKNAME")
        chat_page_url = TestPages.CHAT_PAGE_URL.format(chat_id=chat_id)
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 302)
