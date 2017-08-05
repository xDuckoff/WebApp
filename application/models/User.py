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

    @staticmethod
    def set_access_key(chat_id, access_key):
        """Установка ключа доступа для чата
        
        :param chat_id: Чат
        :param access_key: Ключ доступа
        """
        session["access_keys"][chat_id] = access_key
        session.modified = True

    @staticmethod
    def get_access_key(chat_id):
        """Получение ключа доступа для чата

        :param chat_id: Чат
        :return: Ключ доступа
        """
        if "access_keys" not in session:
            session["access_keys"] = {}
        return session["access_keys"].get(chat_id, '')
