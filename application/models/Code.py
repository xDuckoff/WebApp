# -*- coding: utf-8 -*-
from application import db


class Code(db.Model):
    """Модель исходного кода в чате

    :param id: идентификатор
    :param content: содержимое исходного кода
    :param author: автор кода
    :param message: сообщение-описание редакции исходного кода
    :param chat_link: ссылка на чат, к которому принадлежит данных код
    :param parent_link: ссылка на родителя, от которого образовался данных код
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

        self.content = content
        self.author = author
        self.chat_link = chat_link
        self.parent_link = parent_link
        self.message = message

    @staticmethod
    def get_root_in_chat(chat_id):
        """Получение родительского кода в чате

        :param chat_id: идентификатор чата, в котором и необходимо проводить поиск
        :return: объект Code, который не имеет родителей
        """
        return Code.query.filter_by(chat_link=chat_id, parent_link=None).first()
