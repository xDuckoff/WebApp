# -*- coding: utf-8 -*-

from application import db


class Code(db.Model):
    """Модель исходного кода в чате

    Variables:
        id {[type]} -- идентификатор
        content {[type]} -- содержимое исходного кода
        author {[type]} -- автор кода
        chat_link {[type]} -- ссылка на чат, к которому принадлежит данных код
        parent {[type]} -- ссылка на родителя, от которого образовался данных код
        message {[type]} -- сообщение-описание редакции исходного кода
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    author = db.Column(db.String(256))
    message = db.Column(db.String(256))
    chat_link = db.Column(db.Integer, db.ForeignKey('chat.id'))
    parent_link = db.Column(db.Integer, db.ForeignKey('code.id'), nullable=True)

    chat = db.relationship('Chat', backref=db.backref('codes'))
    children = db.relationship('Code')

    def __init__(self, content, author, chat_link, parent_link, message=u'Начальная версия'):
        """Конструктор исходного кода"""

        self.content = content
        self.author = author
        self.chat_link = chat_link
        self.parent_link = parent_link
        self.message = message
