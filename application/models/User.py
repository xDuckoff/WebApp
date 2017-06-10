# -*- coding: utf-8 -*-

import cgi
from flask import session
from application.models import Message


class User:
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
        """Присоединяет пользователя к чату и отправляет сообщение о присоединении

        :param chat_id: Id чата
        """
        if 'joined_chats' not in session:
            session['joined_chats'] = []
        if chat_id not in session['joined_chats']:
            session['joined_chats'].append(chat_id)
            Message.send(chat_id, User.get_login() + u" присоединился", 'sys')
            session.modified = True
