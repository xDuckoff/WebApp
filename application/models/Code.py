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
        """Создание объекта Code

        :param content: Код
        :param author: Автор кода
        :param chat_link: Id чата, в котором находится код
        :param parent_link: Id "родителя" кода
        :param message: Комментарий к коду
        """
        self.content = content
        self.author = author
        self.chat_link = chat_link
        self.parent_link = parent_link
        self.message = message

    @staticmethod
    def send(chat_id, text, username, parent=None, message=u'Начальная версия'):
        """Отправление кода на сервер

        :param chat_id: Номер чата
        :param text: Код
        :param username: Имя пользователя
        :param parent: Место в дереве коммитов
        :param message: Комметарий к коду
        :return: Сообщение о коммите и номере кода
        """
        code_to_send = Code(text, username, chat_id, parent, message)
        db.session.add(code_to_send)
        db.session.commit()
        code_id_in_chat = u"undefined"
        Message.send(chat_id, u"Изменение кода " + code_id_in_chat + u" : '" + message + u"'", 'sys')
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

    @staticmethod
    def get_root_in_chat(chat_id):
        """Получение стартового коммита в чате

        :param chat_id: Id чата
        :return: Объект стартового коммита
        """
        return Code.query.filter_by(chat_link=chat_id, parent_link=None).first()

    @staticmethod
    def get_commits_tree(chat_id):
        """Данная функция генерирует дерево коммитов для чата

        :return: Сгенерированное дерево коммитов
        """
        tree = Code.get_root_in_chat(chat_id).get_tree_node()
        return tree

    def get_tree_node(self):
        """Генерация вершины в дереве коммитов

        :return: Вершина в дереве коммитов
        """
        NODE_MARKUP = "<div class=\"commit_node circle unchosen\" data-id=\"{id}\">{id}</div>"
        node = {
            "text": {
                "name": self.id,
                "title": self.message
            },
            "innerHTML": NODE_MARKUP.format(id=self.id)
        }
        children = []
        for child_code in self.children:
            children.append(child_code.get_tree_node())
        node["children"] = children
        return node
