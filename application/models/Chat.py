# -*- coding: utf-8 -*-

"""Функции работы с чатами и их поиска"""

from application import app, db
from application.models import Code, Message, MarkdownMixin


class Chat(db.Model):
    """Модель чата

    :param name: наименование чата
    :param code_type: тип исходного кода в этом чате
    :param create_time: время создания чата
    :param remove_time: время удаления чата, если значение не равно null
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    code_type = db.Column(db.Text)
    access_key = db.Column(db.Text)
    create_time = db.Column(db.DateTime, nullable=False, default=db.func.now())
    remove_time = db.Column(db.DateTime)

    def __init__(self, name, code_type, access_key):
        self.name = MarkdownMixin.decode(name)
        self.code_type = code_type
        self.access_key = access_key

    @staticmethod
    def create(chat_name, code, code_type, access_key=''):
        """Создаёт чат

        :param chat_name: Имя чата
        :param code: Код чата
        :param code_type: Язык программирования
        :param access_key: Ключ доступа
        :return: Номер чата
        """
        chat_to_create = Chat(chat_name, code_type, access_key)
        db.session.add(chat_to_create)
        db.session.commit()
        chat_id = chat_to_create.id
        Code.send(chat_id, code, None, u'Начальная версия')
        return chat_id

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
    def find(name, limit=10, page=1):
        """Нахождение чатов по названию или по идентификатору,\
        если ``name`` является числом

        :param name: Имя чата
        :param limit: Количество чатов на странице
        :param page: Номер страницы
        :return: Все чаты, в названии которых содержится имя чата
        """
        if name.isdigit():
            chat_id = int(name)
            return [Chat.query.get(chat_id)]
        offset = (page - 1) * limit
        query = Chat.query.order_by(db.desc(Chat.create_time))
        if name != '':
            query = query.filter(Chat.name.like('%' + name + '%'))
        if limit > 0:
            offset = (page - 1) * limit
            query = query.offset(offset).limit(limit)
        return query.all()

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

    def set_name(self, name):
        """Установка названия чата

        :param name: новое название чата
        :return: объект в разных написаниях названия чата: \
            оригинальное, без тегов, экрнированные теги
        """
        self.name = MarkdownMixin.decode(name)
        db.session.commit()
        Message.send_about_change_chat_name(self.id, MarkdownMixin.plain(self.name))
        return {
            "original": self.name,
            "plain": MarkdownMixin.plain(self.name),
            "escaped": MarkdownMixin.escape_html(self.name)
        }

    def to_dict(self):
        """Возвращает объект в виде словаря (для вывода через api)

        :return: словарь объекта
        """
        language = False
        for lang in app.config['ALLOWED_LANGUAGES']:
            if lang['type'] == self.code_type:
                language = lang
        return dict(
            id=self.id,
            name=self.name,
            code_type=self.code_type,
            language=language,
            has_password=bool(self.access_key),
            create_time=self.create_time.isoformat(' '),
            remove_time=None if self.remove_time is None else self.remove_time.isoformat(' '))
