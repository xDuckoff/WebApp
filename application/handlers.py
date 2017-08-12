# -*- coding: utf-8 -*-

"""Обработчики функций"""

from json import dumps
from functools import wraps
from wtforms.validators import ValidationError
from application.models import User, Chat
from application.forms import ChatForm
from flask import request


def csrf_required(func):
    """Проверка csrf-ключа"""
    @wraps(func)
    def csrf_check(*args, **kwargs):
        """Функция возвращает ошибку, если csrf-ключ невалиден"""
        try:
            User.check_csrf()
        except ValidationError:
            return dumps({"success": False, "error": "Security error"}), 403
        except KeyError:
            return dumps({"success": False, "error": "Security error"}), 403
        return func(*args, **kwargs)
    return csrf_check


def access_required(func):
    """Проверка наличия доступа к чату"""
    @wraps(func)
    def access_check(*args, **kwargs):
        """Функция возвращает ошибку, если ключ доступа к чату невалиден"""
        if request.method == "POST":
            chat_form = ChatForm()
        else:
            chat_form = ChatForm(request.args)
        chat_id = chat_form.chat.data
        chat = Chat.get(chat_id)
        if chat.is_access_key_valid(User.get_access_key(chat_id)):
            return func(*args, **kwargs)
        return dumps({"success": False, "error": "Access error"}), 403
    return access_check


def form_required(form_class):
    """Проверка валидности формы"""
    def decorator(func):
        """Декоратор"""
        @wraps(func)
        def chat_check(*args, **kwargs):
            """Функция возвращает ошибку, если форма невалидна"""
            if request.method == "POST":
                form = form_class()
            else:
                form = form_class(request.args)
                form.csrf_token.process_data(request.headers['X-Csrf-Token'])
            if form.validate():
                return func(*args, **kwargs)
            return dumps({"success": False, "error": "Invalid arguments"}), 400
        return chat_check
    return decorator
