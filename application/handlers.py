# -*- coding: utf-8 -*-

"""Обработчики функций"""

from json import dumps
from functools import wraps
from application.models import User, Chat
from application.forms import ChatForm
from flask import request


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
                if hasattr(form, 'csrf_token'):
                    csrf_token = request.headers.get('X-Csrf-Token', '')
                    form.csrf_token.process_data(csrf_token)
            if form.validate():
                return func(*args, **kwargs)
            return dumps({"success": False, "error": "Invalid arguments"}), 400
        return chat_check
    return decorator
