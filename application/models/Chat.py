# -*- coding: utf-8 -*-

'''Функции работы с чатами и их поиска'''

from application import db
from application.models import Code


class Chat(db.Model):
    """Модель чата

    :param name: наименование чата
    :param code_type: тип исходного кода в этом чате
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    code_type = db.Column(db.String(256))

    def __init__(self, name, code_type):
        self.name = name
        self.code_type = code_type

    @staticmethod
    def create(chat_name, code, code_type, username):
        """Создаёт чат

        :param chat_name: Имя чата
        :param code: Код чата
        :param code_type: Язык программирования
        :param username: Имя пользователя
        :return: Номер чата
        """
        chat_to_create = Chat(chat_name, code_type)
        db.session.add(chat_to_create)
        db.session.commit()
        chat_id = chat_to_create.id
        Code.send(chat_id, code, username)
        return chat_id

    @staticmethod
    def get(id):
        """Возвращает чат по id

        :param id: Номер искомого чата
        :return: Объект чата
        """
        return Chat.query.get(id)

    def get_info(self):
        """Возвращает форматированный чат в виде словаря

        :return: Имя чата и язык программирования чата
        """
        return {
            'name': self.name,
            'code_type': self.code_type,
            'start_code': Code.get_root_in_chat(self.id)
        }

    @staticmethod
    def find(name):
        """Нахождение чатов по названию или по идентификатору,\
        если ``name`` является числом

        :param name: Имя чата
        :return: Все чаты, в названии которых содержится имя чата
        """
        if name == '':
            return Chat.query.all()[:-10:-1]
        if name.isdigit():
            chat_id = int(name)
            return Chat.query.filter_by(id=chat_id).all()
        return Chat.query.filter(Chat.name.like('%' + name + '%')).all()[::-1]

    def get_messages(self, username=""):
        """Получение всех сообщений в чате в форматированном виде

        :param username:  Имя пользователя
        :return: Сообщения пользователей
        """
        return [message.get_info(username) for message in self.messages]
