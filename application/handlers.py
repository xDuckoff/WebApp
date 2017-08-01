# -*- coding: utf-8 -*-

"""Обработчики функций"""

from json import dumps
from functools import wraps
from wtforms.validators import ValidationError
from application.models import User


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
