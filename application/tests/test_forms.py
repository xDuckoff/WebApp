# -*- coding: utf-8 -*-

"""Тесты форм"""

from base_test_model import BaseTestModel
from application.forms import LoginForm, CreateChatForm
from wtforms import StringField, FileField


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
