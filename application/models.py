from application import db

"""
Данный файл содержит модели сообщений, кода и самого чата
"""

class Message(db.Model):
    """
    Класс сообщений содержит в себе имя автора сообщения, номер сообщения, содержание сообщения, номер чата для данного 
    сообщения и тип сообщения и функцию создания сообщения
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    author = db.Column(db.String(256))
    chat = db.Column(db.Integer)
    type = db.Column(db.String(3)) # types: sys, usr

    def __init__(self, content, author, chat, type):
        """
        Данная функция создаёт сообщение в базе данных
        :param content: Содержание сообщения
        :param author: Автор сообщения
        :param chat: Номер чата, для данного сообщения
        :param type: Тип сообщения
        """
        self.content = content
        self.author = author
        self.chat = chat
        self.type = type


class Code(db.Model):
    """
    Класс кода содержит в себе имя сообщения, содержание кода, автора кода, чата кода, номер чата в дереве, и функцию 
    создания кода в базе данных 
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    author = db.Column(db.String(256))
    chat = db.Column(db.Integer)
    parent = db.Column(db.Integer)

    def __init__(self, content, author, chat, parent):
        """
        Функция прикрепления кода к чату
        :param content: Содержание кода
        :param author: Имя Автора коммита кода
        :param chat: ID чата, в котором лежит код
        :param parent: Место в дереве коммитов
        """
        self.content = content
        self.author = author
        self.chat = chat
        self.parent = parent


class Chat(db.Model):
    """
    Класс чата содержит в себе номер чата в базе данных, навзание чата, язык программирования для чата и функцию 
    создания чата
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    code_type = db.Column(db.String(256))

    def __init__(self, name, code_type):
        """
        Функция создаёт чат в базе данных
        :param name: Название чата
        :param code_type: Язык программирования
        """
        self.name = name
        self.code_type = code_type
