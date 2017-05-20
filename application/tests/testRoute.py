import unittest
import os
from application import app
import flask_migrate
from application import chat
from application.forms import login_user
from flask.sessions import SessionInterface
from flask import session

SOME_REQUEST_PATH = "/"
TEST_DB = 'test.sqlite'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class TestMainPage(unittest.TestCase):
    LOGOUT = "/logout"
    INDEX = "/"
    CHAT = "/chat/1"

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, TEST_DB)
        self.app = app.test_client()
        with app.app_context():
            flask_migrate.upgrade() 

    def tearDown(self):
        os.remove(os.path.join(BASE_DIR, TEST_DB))

    def test_should_logout_page_be_exist(self):
        response = self.app.get(self.LOGOUT)
        self.assertEqual(response.status_code, 302)

    def test_should_index_page_be_exist(self):
        response = self.app.get(self.INDEX)
        self.assertEqual(response.status_code, 200)

    def test_should_chat_page_not_be_exist_without_login(self):
        chat.create_chat("NAME", "CODE", "B++", "NICKNAME")
        response = self.app.get(self.CHAT)
        self.assertEqual(response.status_code, 302)
