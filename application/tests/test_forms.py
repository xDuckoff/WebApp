# -*- coding: utf-8 -*-

"""Тесты форм"""

from base_test_model import *
from application.forms import LoginForm, CreateChatForm, FindChatForm, AuthChatForm, ChatForm, \
    SendMessageForm, GetTreeForm, GetMessagesForm, SendCodeForm, GetCodeForm
from wtforms import StringField, FileField, IntegerField


class TestLoginForm(BaseTestModel):

    def test_available_login_form(self):
        self.assertTrue(hasattr(LoginForm, "login"))

    def test_type_login_form(self):
        self.assertIs(LoginForm.login.field_class, StringField)


class TestCreateChatForm(BaseTestModel):

    def test_available_create_chat_form(self):
        self.assertTrue(hasattr(CreateChatForm, "name"))
        self.assertTrue(hasattr(CreateChatForm, "code_type"))
        self.assertTrue(hasattr(CreateChatForm, "file"))
        self.assertTrue(hasattr(CreateChatForm, "code"))

    def test_type_create_chat_form(self):
        self.assertIs(CreateChatForm.name.field_class, StringField)
        self.assertIs(CreateChatForm.code_type.field_class, StringField)
        self.assertIs(CreateChatForm.file.field_class, FileField)
        self.assertIs(CreateChatForm.code.field_class, StringField)


class TestFindChatForm(BaseTestModel):

    def test_available_find_chat_form(self):
        self.assertTrue(hasattr(FindChatForm, "chat_title"))

    def test_type_find_chat_form(self):
        self.assertIs(FindChatForm.chat_title.field_class, StringField)


class TestAuthChatForm(BaseTestModel):

    def test_available_find_chat_form(self):
        self.assertTrue(hasattr(AuthChatForm, "password"))

    def test_type_find_chat_form(self):
        self.assertIs(AuthChatForm.password.field_class, StringField)


class TestChatForm(BaseTestModel):

    def test_available_chat_form(self):
        self.assertTrue(hasattr(ChatForm, "chat"))

    def test_type_chat_form(self):
        self.assertIs(ChatForm.chat.field_class, IntegerField)


class TestSendMessageForm(BaseTestModel):

    def test_available_send_message_form(self):
        self.assertTrue(hasattr(SendMessageForm, "chat"))
        self.assertTrue(hasattr(SendMessageForm, "message"))

    def test_type_send_message_form(self):
        self.assertIs(SendMessageForm.chat.field_class, IntegerField)
        self.assertIs(SendMessageForm.message.field_class, StringField)


class TestGetTreeForm(BaseTestModel):

    def test_available_get_tree_form(self):
        self.assertTrue(hasattr(GetTreeForm, "chat"))

    def test_type_get_tree_form(self):
        self.assertIs(GetTreeForm.chat.field_class, IntegerField)


class TestGetMessagesForm(BaseTestModel):

    def test_available_get_messages_form(self):
        self.assertTrue(hasattr(GetMessagesForm, "chat"))
        self.assertTrue(hasattr(GetMessagesForm, "last_message_id"))

    def test_type_get_messages_form(self):
        self.assertIs(GetMessagesForm.chat.field_class, IntegerField)
        self.assertIs(GetMessagesForm.last_message_id.field_class, IntegerField)


class TestSendCodeForm(BaseTestModel):

    def test_available_get_tree_form(self):
        self.assertTrue(hasattr(SendCodeForm, "chat"))
        self.assertTrue(hasattr(SendCodeForm, "code"))
        self.assertTrue(hasattr(SendCodeForm, "parent"))
        self.assertTrue(hasattr(SendCodeForm, "message"))

    def test_type_get_tree_form(self):
        self.assertIs(SendCodeForm.chat.field_class, IntegerField)
        self.assertIs(SendCodeForm.code.field_class, StringField)
        self.assertIs(SendCodeForm.parent.field_class, IntegerField)
        self.assertIs(SendCodeForm.message.field_class, StringField)


class TestGetCodeForm(BaseTestModel):

    def test_available_get_tree_form(self):
        self.assertTrue(hasattr(GetCodeForm, "index"))

    def test_type_get_tree_form(self):
        self.assertIs(GetCodeForm.index.field_class, IntegerField)
