# -*- coding: utf-8 -*-

"""FlaskWTF и Session Формы"""

from wtforms import StringField, FileField, IntegerField, validators, ValidationError
from flask_wtf import FlaskForm
from application import app
from application.models import Chat


class LoginForm(FlaskForm):
    """Данный класс содержит имя пользователя для сессии"""
    login = StringField('login', validators=[validators.DataRequired()])


class CreateChatForm(FlaskForm):
    """Создаёт чат"""
    name = StringField('name', validators=[validators.DataRequired()])
    code_type = StringField('codetype')
    file = FileField('file')
    code = StringField('code', default='')
    access_key = StringField('access_key', default='')

    def is_file_valid(self):
        """Проверка на валидный файл для создания чата"""
        return self.file.data and '.' in self.file.data.filename and \
               self.file.data.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


class FindChatForm(FlaskForm):
    """Поиск чата"""
    chat_title = StringField('chat_title', default='')


def chat_required(form, field):
    if not Chat.get(field.data):
        raise ValidationError


class ChatForm(FlaskForm):
    """Базовый класс для форм в чате"""
    chat = IntegerField('chat', validators=[validators.DataRequired(), chat_required])


class AuthChatForm(ChatForm):
    """Форма авторизации в чате"""
    password = StringField('password')


class SendMessageForm(ChatForm):
    """Форма отправки сообщений"""
    message = StringField('message', validators=[validators.DataRequired(), validators.Length(min=1, max=1000)])
