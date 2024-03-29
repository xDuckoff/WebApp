# -*- coding: utf-8 -*-

"""Тесты роутов"""

from flask import json
from base import BaseApiTest
from application import app
from application.models import Chat, Message, Code


class TestApiChatPath(BaseApiTest):
    PATH = "/api/chat"

    @staticmethod
    def __create_chats(count):
        langs = app.config['ALLOWED_LANGUAGES']
        for i in xrange(count):
            Chat.create('Chat name', 'Chat code', langs[i % len(langs)]['type'])

    def test_status_chat_path(self):
        response = self.app.get(self.PATH)
        self.assertEqual(response.status_code, 200)

    def test_format_chat_path(self):
        response = self.app.get(self.PATH)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_content_chat_path(self):
        CHAT_COUNT = 5
        self.__create_chats(CHAT_COUNT)
        response = self.app.get(self.PATH)
        data = json.loads(response.data)
        self.assertEqual(len(data), CHAT_COUNT)

    def test_limit_param(self):
        CHAT_COUNT = 6
        LIMIT_PARAM = 5
        self.__create_chats(CHAT_COUNT)
        response = self.app.get(self.PATH, query_string=dict(limit=LIMIT_PARAM))
        data = json.loads(response.data)
        self.assertEqual(len(data), LIMIT_PARAM)

    def test_page_param(self):
        CHAT_COUNT = 6
        LIMIT_PARAM = 5
        PAGE = 2
        self.__create_chats(CHAT_COUNT)
        response = self.app.get(self.PATH, query_string=dict(limit=LIMIT_PARAM, page=PAGE))
        data = json.loads(response.data)
        self.assertEqual(len(data), CHAT_COUNT - LIMIT_PARAM)


class TestApiUserPath(BaseApiTest):
    PATH = "/api/user"

    def test_status_user_get_path(self):
        response = self.app.get(self.PATH)
        self.assertEqual(response.status_code, 200)

    def test_format_user_get_path(self):
        response = self.app.get(self.PATH)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)

    def test_has_user_name_in_response(self):
        response = self.app.get(self.PATH)
        data = json.loads(response.data)
        self.assertIsNotNone(data.get('name'))

    def test_format_user_save_params(self):
        USER_NAME = 'user'
        PARAMS = dict(name=USER_NAME)
        response = self.app.put(self.PATH, data=json.dumps(PARAMS), content_type='application/json')
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertTrue(data.get('success'))
