# -*- coding: utf-8 -*-

"""Функции работы с кодом и деревом коммитов"""

from application import app, db, socketio
from application.models import Message, User, MarkdownMixin


class Code(db.Model):
    """Модель исходного кода в чате

    :param content: содержимое исходного кода
    :param author: автор кода
    :param message: сообщение-описание редакции исходного кода
    :param number: номер коммита, порядковый в рамках одного чата
    :param chat_link: ссылка на чат, к которому принадлежит данных код
    :param parent_link: ссылка на родителя, от которого образовался данных код
    :param create_time: время создания кода
    :param remove_time: время удаления кода, если значение не равно null
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    author = db.Column(db.Text)
    message = db.Column(db.Text)
    number = db.Column(db.Integer, nullable=True)
    chat_link = db.Column(db.Integer, db.ForeignKey('chat.id'))
    parent_link = db.Column(db.Integer, db.ForeignKey('code.id'), nullable=True)
    create_time = db.Column(db.DateTime, nullable=False, default=db.func.now())
    remove_time = db.Column(db.DateTime)
    chat = db.relationship('Chat', backref=db.backref('codes'))
    children = db.relationship('Code')

    NODE_MARKUP = "<div class=\"commit_node circle unchosen\" data-id=\"{id}\">{number}</div>"
    SYS_MESSAGE_ADD_TEMPLATE = u'Новое изменение {number} : {message}'

    def __init__(self, **params):
        self.content = params.get('content', "")
        self.author = User.get_login()
        self.chat_link = params.get('chat_link')
        self.parent_link = params.get('parent_link')
        self.message = MarkdownMixin.decode(params.get('message'))
        self.number = Code.get_count_in_chat(params.get('chat_link')) + 1

    @staticmethod
    def send(chat_id, code_text, parent, message):
        """Отправление кода на сервер

        :param chat_id: Номер чата
        :param code_text: Код
        :param parent: Место в дереве коммитов
        :param message: Комметарий к коду
        :return: Сообщение о коммите и номере кода
        """
        code_params = {
            "content": code_text,
            "message": message,
            "chat_link": chat_id,
            "parent_link": parent
        }
        code_to_send = Code(**code_params)
        db.session.add(code_to_send)
        db.session.commit()
        message_text = Code.SYS_MESSAGE_ADD_TEMPLATE.format(
            number=code_to_send.number,
            message=message
        )
        Message.send(chat_id, message_text, Message.SYSTEM_TYPE)
        if app.config['SOCKET_MODE'] == 'True':
            socketio.emit('commit', room=str(chat_id), broadcast=True)
        return code_to_send.id

    @staticmethod
    def get(uid):
        """Возвращает форматированный код по ``id`` в виде словаря

        :param uid: идентификатор исходного кода
        :return: Автор и код
        """
        code = Code.query.get(uid)
        return {
            "author": code.author,
            "code": code.content
        }

    @staticmethod
    def get_root_in_chat(chat_id):
        """Получение стартового коммита в чате

        :param chat_id: Id чата
        :return: Объект стартового коммита
        """
        return Code.query.filter_by(chat_link=chat_id, parent_link=None).first()

    @staticmethod
    def get_commits_tree(chat_id):
        """Получение сгенериррованного дерева коммитов для чата

        :return: Сгенерированное дерево коммитов
        """
        tree = Code.get_root_in_chat(chat_id).get_tree_node()
        return tree

    def get_tree_node(self):
        """Получение вершины в дереве коммитов, форматированной для TreantJS

        :return: Вершина в дереве коммитов
        """
        # TODO надо все number = None пересчитать (сделать в миграции)
        number = self.number
        if number is None:
            number = self.id
        node = {
            "text": {
                "name": self.id,
                "title": self.message
            },
            "innerHTML": Code.NODE_MARKUP.format(id=self.id, number=number)
        }
        children = [child.get_tree_node() for child in self.children]
        node["children"] = children
        return node

    @staticmethod
    def get_count_in_chat(chat_id):
        """Получение количества коммитов в одном чате

        :return: количества коммитов
        """
        return Code.query.filter_by(chat_link=chat_id).count()
