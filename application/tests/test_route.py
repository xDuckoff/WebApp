# -*- coding: utf-8 -*-

"""Тесты роутов"""

from base_test_model import *
from application import app
from application.models import Chat, Message, Code

MAIN_PAGE_URL = "/"
FEEDBACK_PAGE_URL = "/feedback"
TREE_PAGE_URL = '/tree?chat={chat_id}'
CHAT_PAGE_URL = "/chat/{chat_id}"
SET_CHAT_NAME_PAGE_URL = "/set_chat_name"
CHAT_GET_INFO_PAGE_URL = '/get_chat_info?chat={chat_id}'
CODE_SEND_PAGE_URL = '/send_code'
CODE_GET_PAGE_URL = '/get_code?index={code_id}'
MESSAGES_GET_PAGE_URL = '/get_messages?chat={chat_id}'
MESSAGES_GET_LAST_PAGE_URL = '/get_messages?chat={chat_id}&last_message_id={last_message_id}'
MESSAGE_SEND_PAGE_URL = '/send_message'


class BaseTestPages(BaseTestModel):

    def setUp(self):
        BaseTestModel.setUp(self)
        self.app = app.test_client()


class TestMainPage(BaseTestPages):

    def test_index_page(self):
        response = self.app.get(MAIN_PAGE_URL)
        self.assertEqual(response.status_code, 200)


class TestFeedbackPage(BaseTestPages):

    def test_feedback_page(self):
        response = self.app.get(FEEDBACK_PAGE_URL)
        self.assertEqual(response.status_code, 200)


class TestChatPage(BaseTestPages):

    def test_access_chat_page(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        chat_page_url = CHAT_PAGE_URL.format(chat_id=chat_id)
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 200)

    def test_uncreated_chat_page_not_be_exist(self):
        chat_page_url = CHAT_PAGE_URL.format(chat_id=1)
        response = self.app.get(chat_page_url)
        self.assertEqual(response.status_code, 302)

    def test_set_chat_name(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        params = {
            "chat": chat_id,
            "name": MESSAGE
        }
        response = self.app.post(SET_CHAT_NAME_PAGE_URL, data=params)
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

    def test_send_message(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        params = {
            "chat": chat_id,
            "message": MESSAGE
        }
        response = self.app.post(MESSAGE_SEND_PAGE_URL, data=params)
        self.assertEqual(response.status_code, 200)

    def test_get_tree(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        response = self.app.get(TREE_PAGE_URL.format(chat_id=chat_id))
        self.assertEqual(response.status_code, 200)


class TestCodePage(BaseTestPages):

    def test_send_code(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        params = {
            "chat": chat_id,
            "code": CODE,
            "parent": 1,
            "cname": COMMIT_MESSAGE
        }
        response = self.app.post(CODE_SEND_PAGE_URL, data=params)
        self.assertEqual(response.status_code, 200)

    def test_get_code(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        code_id = Code.send(chat_id, CODE, 1, COMMIT_MESSAGE)
        response = self.app.get(CODE_GET_PAGE_URL.format(code_id=code_id))
        self.assertEqual(response.status_code, 200)


class TestHandlers(BaseTestPages):

    def test_access_required_handler(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, CHAT_ACCESS_KEY)
        self.real.get_access_key.return_value = CHAT_INCORRECT_ACCESS_KEY
        response = self.app.get(MESSAGES_GET_PAGE_URL.format(chat_id=chat_id))
        self.assertEqual(response.status_code, 403)
        self.real.get_access_key.return_value = CHAT_ACCESS_KEY
        response = self.app.get(MESSAGES_GET_PAGE_URL.format(chat_id=chat_id))
        self.assertEqual(response.status_code, 200)

    def test_form_required_handler(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)
        response = self.app.get(MESSAGES_GET_PAGE_URL.format(chat_id=chat_id))
        self.assertEqual(response.status_code, 200)
        response = self.app.get(MESSAGES_GET_PAGE_URL.format(chat_id=chat_id + 1))
        self.assertEqual(response.status_code, 400)
