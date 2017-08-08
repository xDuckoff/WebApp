# -*- coding: utf-8 -*-

"""Функции работы с сообщениями"""

import re
from application.models import User, MarkdownMixin
from application import app, db, socketio


class Message(db.Model):
    """Модель сообщений в чате

    :param content:  исходное содержание сообщения
    :param chat_link:  ссылка на чат, которому принадлежит сообщение
    :param message_type: тип сообщения: системное или пользовательское
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    author = db.Column(db.Text)
    type = db.Column(db.String(3))
    chat_link = db.Column(db.Integer, db.ForeignKey('chat.id'))
    chat = db.relationship('Chat', backref=db.backref('messages', lazy='dynamic'))

    def __init__(self, content, chat_link, message_type):
        self.content = MarkdownMixin.decode(content)
        self.author = User.get_login()
        self.chat_link = chat_link
        self.type = message_type

    @staticmethod
    def send(chat_id, text, message_type):
        """Отправляет сообщение в базу для сохранения

        :param chat_id: Номер чата
        :param text: Содержание сообщения
        :param message_type: Тип сообщения
        :return: Объект созданного сообщения
        """
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
