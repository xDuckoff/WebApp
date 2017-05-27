# -*- coding: utf-8 -*-

import unittest
import os
from application import app
import flask_migrate
from application import chat
from application.forms import login_user
from flask.sessions import SessionInterface
from flask import session

"""
Файл содержит тесты роутов
"""

PATH_TO_DATABASE = "/tmp/db-test.sqlite"

LOGOUT = "/logout"
INDEX = "/"
CHAT = "/chat/1"


class TestMainPage(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + PATH_TO_DATABASE
        self.app = app.test_client()
        with app.app_context():
            flask_migrate.upgrade() 

    def tearDown(self):
        os.remove(os.path.join(PATH_TO_DATABASE))

    def test_should_logout_page_be_exist(self):
        response = self.app.get(LOGOUT)
        self.assertEqual(response.status_code, 302)

    def test_should_index_page_be_exist(self):
        response = self.app.get(INDEX)
        self.assertEqual(response.status_code, 200)

    def test_should_chat_page_not_be_exist_without_login(self):
        chat.create_chat("NAME", "CODE", "B++", "NICKNAME")
        response = self.app.get(CHAT)
        self.assertEqual(response.status_code, 302)
