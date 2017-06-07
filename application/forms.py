# -*- coding: utf-8 -*-

"""FlaskWTF и Session Формы"""

from wtforms import StringField, FileField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask.sessions import SessionInterface


class LoginForm(FlaskForm):
    """Данный класс содержит имя пользователя для сессии"""
    login = StringField('login', validators=[DataRequired()])


class BeakerSessionInterface(SessionInterface):
    """Данный класс содержит интерфейс сесии"""

    def open_session(self, app, request):
        """Данная функция создаёт сессию для пользователя
        
        :param app: Приложения
        :param request: Запрос
        :return: Сессию
        """
        session = request.environ['beaker.session']
        return session

    def save_session(self, app, session, response):
        """Данная функция сохраняет сессию поьзователя

        :param app: Приложение
        :param session: Сессия
        :param response: Отклик сессии
        """
        session.save()


class CreateChatForm(FlaskForm):
    """Создаёт чат"""
    name = StringField('name', validators=[DataRequired()])
    code_type = StringField('codetype', validators=[DataRequired()])
    file = FileField('file')
    code = StringField('code')
