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
        chat_form = ChatForm()
        chat_id = chat_form.chat.data
        chat = Chat.get(chat_id)
        if chat.is_access_key_valid(User.get_access_key(chat_id)):
            return func(*args, **kwargs)
        return dumps({"success": False, "error": "Access error"}), 403
    return access_check


def form_required(form_class, post=False):
    """Проверка валидности формы"""
    def decorator(func):
        @wraps(func)
        def chat_check(*args, **kwargs):
            if post:
                form = form_class(request.form)
            else:
                form = form_class(request.args)
            if form.validate():
                return func(*args, **kwargs)
            return dumps({"success": False, "error": "Invalid arguments"}), 400
        return chat_check
    return decorator
