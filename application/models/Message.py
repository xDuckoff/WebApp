# -*- coding: utf-8 -*-

"""Функции работы с сообщениями"""

import re
import cgi
import time
from markdown import markdown
from application.models import User
from application import app, db, socketio


class Message(db.Model):
    """Модель сообщений в чате

    :param content:  исходное содержание сообщения
    :param chat_link:  ссылка на чат, которому принадлежит сообщение
    :param message_type: тип сообщения: системное или пользовательское
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    author = db.Column(db.String(256))
    type = db.Column(db.String(3))
    chat_link = db.Column(db.Integer, db.ForeignKey('chat.id'))
    chat = db.relationship('Chat', backref=db.backref('messages', lazy='dynamic'))
    message_create_time = db.Column(db.Integer)
    message_remove_time = db.Column(db.Integer)

    def __init__(self, content, chat_link, message_type):
        self.content = Message.markdown_decode(content)
        self.author = User.get_login()
        self.chat_link = chat_link
        self.type = message_type
        self.message_create_time = int(time.time())
        self.message_remove_time = None

    @staticmethod
    def send(chat_id, text, message_type):
        """Отправляет сообщение в базу для сохранения

        :param chat_id: Номер чата
        :param text: Содержание сообщения
        :param message_type: Тип сообщения
        :return: Объект созданного сообщения
        """
        if len(text) > 1000 or not text:
            raise OverflowError
        message = Message(text, chat_id, message_type)
        db.session.add(message)
        db.session.commit()
        if app.config['SOCKET_MODE'] == 'True':
            socketio.emit('message', message.get_info(), room=str(chat_id), broadcast=True)
        return message

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

    @staticmethod
    def markdown_decode(text):
        """Преобразование текста в HTML в соответствии с синтаксисом Markdown

        :param text: исходный текст
        :return: преобразовнный в HTML текст
        """
        text = Message.escape(text)
        text = markdown(text)
        return text

    def get_info(self):
        """Получение форматированного сообщения в виде словаря

        :return: Информация о сообщении
        """
        if self.type == "usr":
            if self.author == User.get_login():
                client_type = "mine"
            else:
                client_type = "others"
        else:
            client_type = "sys"
        return {
            'id': self.id,
            'message': self.content,
            'plain_message': self.plain(),
            'author': self.author,
            'type': client_type
        }
