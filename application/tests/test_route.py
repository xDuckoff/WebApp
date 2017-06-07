# -*- coding: utf-8 -*-
"""
Тесты роутов
"""

import unittest
import os
from application import app, db, chat


class TestPages(unittest.TestCase):
    MAIN_PAGE_URL = "/"
    CHAT_PAGE_URL = "/chat/{chat_id}"
    LOGOUT_PAGE_URL = "/logout"

    def setUp(self):
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['TEST_DATABASE_URL']
        app.config['TEST_MODE'] = True
        db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        db.drop_all()

    def test_should_logout_page_be_exist(self):
        response = self.app.get(TestPages.LOGOUT_PAGE_URL)
        self.assertEqual(response.status_code, 302)

    def test_should_index_page_be_exist(self):
        response = self.app.get(TestPages.MAIN_PAGE_URL)
        self.assertEqual(response.status_code, 200)

    def test_should_chat_page_not_be_exist_without_login(self):
        chat_id = chat.create_chat("NAME", "CODE", "B++", "NICKNAME")
        chat_page_url = TestPages.CHAT_PAGE_URL.format(chat_id=chat_id)
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 302)
