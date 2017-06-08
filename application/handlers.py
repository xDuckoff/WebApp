# -*- coding: utf-8 -*-

"""Обработчики функций"""

from flask import redirect, session, request
from flask_wtf import csrf
from wtforms.validators import ValidationError
from json import dumps
from functools import wraps


def login_required(func):
    """Проверка на регистрацию"""
    @wraps(func)
    def login_check(*args, **kwargs):
        if 'login' not in session:
            return redirect('/')
        return func(*args, **kwargs)
    return login_check


def csrf_required(func):
    """Проверка csrf-ключа"""
    @wraps(func)
    def csrf_check(*args, **kwargs):
        try:
            csrf.validate_csrf(request.headers['X-Csrf-Token'])
        except ValidationError:
            return dumps({"success": False, "error": "Security error"}), 403
        except KeyError:
            return dumps({"success": False, "error": "Security error"}), 403
        return func(*args, **kwargs)
    return csrf_check
