# -*- coding: utf-8 -*-

"""Функции работы с сообщениями"""

import re
import cgi
from application import app, db, socketio
from markdown import markdown


class Message(db.Model):
    """Модель сообщений в чате

    :param content:  исходное содержание сообщения
    :param author:  автор сообщения
    :param chat_link:  ссылка на чат, которому принадлежит сообщение
    :param message_type: тип сообщения: системное или пользовательское
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    content_ru = db.Column(db.Text)
    content_en = db.Column(db.Text)
    author = db.Column(db.String(256))
    type = db.Column(db.String(3))
    chat_link = db.Column(db.Integer, db.ForeignKey('chat.id'))
    chat = db.relationship('Chat', backref=db.backref('messages'))


    def __init__(self, content, author, chat_link, message_type):
        content = Message.escape(content)
        content = markdown(content)
        self.content = content
        self.author = author
        self.chat_link = chat_link
        self.type = message_type


    @staticmethod
    def send(chat_id, text, message_type, username=u'Системное сообщение'):
        """Отправляет сообщение в базу для сохранения

        :param chat_id: Номер чата
        :param text: Содержание сообщения
        :param message_type: Тип сообщения
        :param username: Имя пользователя
        :return: Объект созданного сообщения
        """
        if len(text) > 1000 or not text:
            raise OverflowError
        message = Message(text, username, chat_id, message_type)
        db.session.add(message)
        db.session.commit()
        if app.config['SOCKET_MODE'] == 'True':
            socketio.emit('message', message.get_info(username), room=str(chat_id), broadcast=True)
        return message

    def translate(self):
        """Функция для перевода сообщений

        :return: Переведённое сообщение
        """
        return {
            "no": self.content,
            "ru": self.content_ru,
            "en": self.content_en
        }

    def plain(self):
        """Функция удаляет html-теги из текста

        :return: Текст без html-тегов
        """
        text = self.content
        text = re.sub(r'\<[^>]*>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    @staticmethod
    def escape(text):
        """Экранирование текста

        :param text: Исходный текст
        :return: Экранированный текст
        """
        text = text.replace('```', '`')
        parts = text.split('`')
        for i in range(0, len(parts), 2):
            parts[i] = cgi.escape(parts[i])
        return '`'.join(parts)

    def get_info(self, username):
        """Получение форматированного сообщения в виде словаря

        :param username: Имя пользователя
        :return: Информация о сообщении
        """
        if self.type == "usr":
            if self.author == username:
                client_type = "mine"
            else:
                client_type = "others"
        else:
            client_type = "sys"
        return {
            'message': self.content,
            'plain_message': self.plain(),
            'author': self.author,
            'type': client_type
        }
