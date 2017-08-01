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
    def logout():
        """Деавторизация пользователя
        """
        session.clear()

    @staticmethod
    def get_login():
        """Получение имени пользователя

        :return: Имя пользователя или None, если оно отсутствует
        """
        return session.get('login')

    @staticmethod
    def is_logined():
        """Авторизован ли пользователь

        :return: True, если пользователь авторизован, False в противном случае.
        """
        return 'login' in session

    @staticmethod
    def check_csrf():
        """Проверка на валидность csrf-ключа"""
        csrf.validate_csrf(request.headers['X-Csrf-Token'])
