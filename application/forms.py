# -*- coding: utf-8 -*-

"""FlaskWTF и Session Формы"""

from wtforms import StringField, FileField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    """Данный класс содержит имя пользователя для сессии"""
    login = StringField('login', validators=[DataRequired()])


class CreateChatForm(FlaskForm):
    """Создаёт чат"""
    name = StringField('name', validators=[DataRequired()])
    code_type = StringField('codetype', validators=[DataRequired()])
    file = FileField('file')
    code = StringField('code')
