# -*- coding: utf-8 -*-

"""Функции пользователя"""

import cgi
from flask import session, request
from flask_wtf import csrf


class User(object):
    """Модель пользователя
    """

    @staticmethod
    def login(username):
        """Авторизация пользователя

        :param username: Имя пользователя
        """
        session['login'] = cgi.escape(username)

    @staticmethod
    def get_login():
        """Получение имени пользователя

        :return: Имя пользователя
        """
        if 'login' not in session:
            User.login(u'Пользователь')
        return session['login']

    @staticmethod
    def check_csrf():
        """Проверка на валидность csrf-ключа"""
        csrf.validate_csrf(request.headers['X-Csrf-Token'])
