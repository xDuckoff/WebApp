# -*- coding: utf-8 -*-
from application import app, db, socketio
from application.models import Message


class Code(db.Model):
    """Модель исходного кода в чате

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
    def send(chat_id, text, username, parent=None, cname=u'Начальная версия'):
        """Отправление кода на сервер

        :param chat_id: Номер чата
        :param text: Код
        :param username: Имя пользователя
        :param parent: Место в дереве коммитов
        :param cname: Комметарий к коду
        :return: Сообщение о коммите и номере кода
        """
        code_to_send = Code(text, username, chat_id, parent, cname)
        db.session.add(code_to_send)
        db.session.commit()
        code_id_in_chat = u"undefined"
        Message.send(chat_id, u"Изменение кода " + code_id_in_chat + u" : '" + unicode(cname) + u"'", 'sys')
        if app.config['SOCKET_MODE'] == 'True':
            socketio.emit('commit', room=str(chat_id), broadcast=True)
        return code_to_send.id

    @staticmethod
    def get(id):
        """Функция передаёт код с сервера пользователю

        :param id: идентификатор исходного кода
        :return: Автор и код
        """
        code = Code.query.get(id)
        return {
            "author": code.author,
            "code": code.content
        }
