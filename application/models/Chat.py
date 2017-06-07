# -*- coding: utf-8 -*-
from application import db
from application.chat import send_code


class Chat(db.Model):
    """Модель чата

    :param id: идентификатор
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
        """
        Данная функция создаёт чат

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
        send_code(chat_id, code, username)
        return chat_id
