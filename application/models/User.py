# -*- coding: utf-8 -*-

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
    def join_chat(chat_id):
        """Присоединяет пользователя к чату

        :param chat_id: Id чата
        :return: True, если пользователь присоединился к чату, False, если он уже был присоединён
        """
        if 'joined_chats' not in session:
            session['joined_chats'] = []
        if chat_id not in session['joined_chats']:
            session['joined_chats'].append(chat_id)
            session.modified = True
            return True
        return False

    @staticmethod
    def check_csrf():
        csrf.validate_csrf(request.headers['X-Csrf-Token'])
