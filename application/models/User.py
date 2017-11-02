# -*- coding: utf-8 -*-

"""Функции пользователя"""

import cgi
from flask import session


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
    def set_access_key(chat_id, access_key):
        """Установка ключа доступа для чата

        :param chat_id: Чат
        :param access_key: Ключ доступа
        """
        if "access_keys" not in session:
            session["access_keys"] = {}
        session["access_keys"][str(chat_id)] = access_key
        session.modified = True

    @staticmethod
    def get_access_key(chat_id):
        """Получение ключа доступа для чата

        :param chat_id: Чат
        :return: Ключ доступа
        """
        return session.get("access_keys", {}).get(str(chat_id), '')

    @staticmethod
    def register_message(message_id):
        """Регистрация в сессии, написанного пользователем сообщения

        :param message_id: идентификатор сообщения
        """
        if "messages" not in session:
            session["messages"] = []
        session["messages"].append(message_id)

    @staticmethod
    def has_message(message_id):
        """Проверка на авторство сообщения текущим пользователем

        :param message_id: идентификатор сообщения
        """
        return "messages" in session and message_id in session["messages"]

