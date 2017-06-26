# -*- coding: utf-8 -*-

"""FlaskWTF и Session Формы"""

from wtforms import StringField, FileField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from application import app


class LoginForm(FlaskForm):
    """Данный класс содержит имя пользователя для сессии"""
    login = StringField('login', validators=[DataRequired()])


class CreateChatForm(FlaskForm):
    """Создаёт чат"""
    name = StringField('name', validators=[DataRequired()])
    code_type = StringField('codetype', validators=[DataRequired()])
    file = FileField('file')
    code = StringField('code', default='')

    def is_file_valid(self):
        """Проверка на валидный файл для создания чата"""
        return self.file.data and '.' in self.file.data.filename and \
               self.file.data.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


class FindChatForm(FlaskForm):
    """Поиск чата"""
    chat_title = StringField('chat_title', default='')


class FeedbackForm(FlaskForm):
    """данные для Feedback"""
    name = StringField('name')
    email = StringField('email')
    text = StringField('text')
