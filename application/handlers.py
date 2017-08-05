# -*- coding: utf-8 -*-

"""Обработчики функций"""

from json import dumps
from functools import wraps
from wtforms.validators import ValidationError
from application.models import User, Chat
from flask import request


def csrf_required(func):
    """Проверка csrf-ключа"""
    @wraps(func)
    def csrf_check(*args, **kwargs):
        """Выдаёт ошибку, если пользователь не имеет валидного csrf-ключа"""
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
        """Выдаёт ошибку, если пользователь не имеет доступ к чату"""
        chat_id = request.args.get('chat', '')
        chat = Chat.get(chat_id)
        if chat.is_access_key_valid(User.get_access_key(chat_id)):
            return func(*args, **kwargs)
        return dumps({"success": False, "error": "Access error"}), 403
    return access_check
