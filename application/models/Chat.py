# -*- coding: utf-8 -*-

"""Функции работы с чатами и их поиска"""

from application import db
from application.models import Code, Message, MarkdownMixin


class Chat(db.Model):
    """Модель чата

    :param name: наименование чата
    :param code_type: тип исходного кода в этом чате
    :param create_time: время создания чата
    :param remove_time: время удаления чата, если значение не равно null
    :param initialized: инициализирован ли чат
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    code_type = db.Column(db.Text)
    access_key = db.Column(db.Text)
    create_time = db.Column(db.DateTime, nullable=False, default=db.func.now())
    remove_time = db.Column(db.DateTime)
    initialized = db.Column(db.Boolean, default=False)

    def __init__(self, name, access_key):
        self.name = MarkdownMixin.decode(name)
        self.access_key = access_key

    @staticmethod
    def create(chat_name, access_key=''):
        """Создаёт чат

        :param chat_name: Имя чата
        :param access_key: Ключ доступа
        :return: Номер чата
        """
        chat_to_create = Chat(chat_name, access_key)
        db.session.add(chat_to_create)
        db.session.commit()
        chat_id = chat_to_create.id
        return chat_id

    def initialize(self, code_type, code):
        """Инициализирует чат

        :param code_type: Тип исходного кода
        :param code: Начальная версия исходного кода
        """
        self.code_type = code_type
        Code.send(self.id, code, None, u'Начальная версия')
        self.initialized = True
        db.session.commit()

    @staticmethod
    def get(uid):
        """Возвращает чат по id

        :param uid: Номер искомого чата
        :return: Объект чата
        """
        return Chat.query.get(uid)

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

    def get_last_messages(self, last_message_id=0):
        """Получение последних сообщений в чате в форматированном виде, \
        которые были сохранены после определенного сообщения. \
        Если ``last_message_id`` не задано, то будут возвращены все сообщения в чате.

        :param last_message_id: id сообщения, после которого надо получить последние сообщения
        :return: Сообщения пользователей
        """
        last_messages = self.messages.filter(Message.id > last_message_id)
        return [message.get_info() for message in last_messages]

    def has_message(self, message_id):
        """Проверка существования сообщения в чате

        :param message_id: Id сообщения
        :return: True, если сообщение существует, False в противном случае
        """
        return message_id.isdigit() and self.messages.count() > int(message_id)

    def has_code(self, code_id):
        """Проверка существования кода в чате

        :param code_id: Id код
        :return: True, если код существует, False в противном случае
        """
        return code_id.isdigit() and len(self.codes) > int(code_id)

    def is_access_key_valid(self, password):
        """Проверка на валидность пароля

        :param password: Пароль
        :return: Является ли пароль валидным
        """
        return not self.access_key or self.access_key == password
