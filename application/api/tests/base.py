# -*- coding: utf-8 -*-

"""Стандартный класс тестов"""

import unittest
import os
from mock import Mock
from application import app, db
from application.models import User


class BaseApiTest(unittest.TestCase):
    USERNAME = 'Bot'
    CHAT_ACCESS_KEY = 'secret_password'

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['TEST_DATABASE_URL']
        db.create_all()
        app.config['SOCKET_MODE'] = 'True'
        app.config['WTF_CSRF_ENABLED'] = False
        self.__mockUser()
        self.app = app.test_client()

    def __mockUser(self):
        self.real = User
        self.real.get_access_key = Mock()
        self.real.get_access_key.return_value = BaseApiTest.CHAT_ACCESS_KEY
        self.real.get_login = Mock()
        self.real.get_login.return_value = BaseApiTest.USERNAME
        self.real.register_message = Mock()
        self.real.has_message = Mock()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
