# -*- coding: utf-8 -*-

from application import db


class Message(db.Model):
    """Модель сообщений в чате

    :param id: идентификатор
    :param content:  исходное содержание сообщения
    :param content_ru:  содержание сообщения, переведенное на русский
    :param content_en:  содержание сообщения, переведнное на английский
    :param author:  автор сообщения
    :param type:  тип сообщения: обычное (`usr`), системное (`sys`)
    :param chat_link:  ссылка на чат, которому принадлежит сообщение
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    content_ru = db.Column(db.Text)
    content_en = db.Column(db.Text)
    author = db.Column(db.String(256))
    type = db.Column(db.String(3))
    chat_link = db.Column(db.Integer, db.ForeignKey('chat.id'))
    chat = db.relationship('Chat', backref=db.backref('messages'))

    def __init__(self, content, author, chat_link, type_code):
        self.content = content
        self.author = author
        self.chat_link = chat_link
        self.type = type_code
