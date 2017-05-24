# -*- coding: utf-8 -*-

from wtforms import StringField, FileField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf import FlaskForm
from flask.sessions import SessionInterface
from flask import session
from application import app
import cgi
from flask_wtf.csrf import validate_csrf

"""
Данный файл содержит все стороннние функции и классы проекта
"""

session_opts = {
    'session.url': '127.0.0.1:11211',
    'session.data_dir': './cache',
}


class LoginForm(FlaskForm):
    """
    Данный класс содержит имя пользователя для сессии
    """
    login = StringField('login', validators=[DataRequired()])


class BeakerSessionInterface(SessionInterface):
    """
    Данный класс содержит интерфейс сесии
    """
    def open_session(self, app, request):
        """
        Данная функция создаёт сессию для пользователя
        
        :param app: Приложения
        
        :param request: Запрос
        
        :return: Сессию
        """
        session = request.environ['beaker.session']
        return session

    def save_session(self, app, session, response):
        """
        Данная функция сохраняет сессию поьзователя
        
        :param app: Приложение
        
        :param session: Сессия
        
        :param response: Отклик сессии
        """
        session.save()


def login_user(login):
    """
    Данная функция залогинивает пользователя и создаёт сессию для него
    
    :param login: Имя пользователя
    """
    session['login'] = cgi.escape(login)
    session['joined_chats'] = []


def IsInSession():
    """
    Данная функция проверяет, существует находится ли пользователь в сессиии
    
    :return: Находится ли пользователь в сессии
    """
    return 'login' in session

def allowed_file(filename):
    """
    Данная функция проверяет, можно ли прикрепить файл с данным расширением
    :param filename: Имя файла
    
    :return: Находится ли тип файла в разрешённых
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

class CreateChatForm(FlaskForm):
    """
    Создаёт чат
    """
    name = StringField('name', validators=[DataRequired()])
    code_type = StringField('codetype', validators=[DataRequired()])
    file = FileField('file')
    code = StringField('code')

def csrf_check(headers):
    if 'X-Csrf-Token' not in headers:
        return False
    try:
        validate_csrf(headers['X-Csrf-Token'])
    except ValidationError:
        return False
    return True
