# -*- coding: utf-8 -*-

from application import db

class Message(db.Model):
    """Модель сообщений в чате

    Variables:
        id {[type]} -- идентификатор
        content {[type]} -- исходное содержание сообщения
        content_ru {[type]} -- содержание сообщения, переведенное на русский
        content_en {[type]} -- содержание сообщения, переведнное на английский
        author {[type]} -- автор сообщения
        chat_link {[type]} -- ссылка на чат, которому принадлежит сообщение
        type {[type]} -- тип сообщения: обычное (`usr`), системное (`sys`)
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    content_ru = db.Column(db.Text)
    content_en = db.Column(db.Text)
    author = db.Column(db.String(256))
    type = db.Column(db.String(3))
    chat_link = db.Column(db.Integer, db.ForeignKey('chat.id'))
    chat = db.relationship('Chat',
        backref=db.backref('messages', lazy='dynamic'))

    def __init__(self, content, author, chat_link, type):
        """Конструктор сообщения

        Arguments:
            content {[type]} -- [description]
            author {[type]} -- [description]
            chat {[type]} -- [description]
            type {[type]} -- [description]
        """

        self.content = content
        self.author = author
        self.chat_link = chat_link
        self.type = type
