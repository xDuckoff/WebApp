# -*- coding: utf-8 -*-

"""Стандартный класс тестов"""

import unittest
import os
from application import app, db


class BaseTestModel(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['TEST_DATABASE_URL']
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
