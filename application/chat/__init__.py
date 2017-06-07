# -*- coding: utf-8 -*-

from application.models import Message, Code, Chat
from application import db, app
import sockets
from json import dumps
import requests
import re
import cgi


def create_chat(name, code, code_type, username):
    """
    Данная функция создаёт чат
    
    :param name: Имя чата
    
    :param code: Код чата
    
    :param code_type: Язык программирования
    
    :param username: Имя пользователя
    
    :return: Номер чата
    """
    chat_to_create = Chat(name, code_type)
    db.session.add(chat_to_create)
    db.session.commit()
    chat_id = chat_to_create.id
    send_code(chat_id, code, username)
    return chat_id


def get_chat_info(id):
    """
    Данная функция передаёт пользователю информацию о чате по номеру
    
    :param id: Номер чата
    
    :return: Имя чата и язык программирования чата
    """
    result = Chat.query.get(id)
    if not result:
        return {}
    return {
        'name': result.name,
        'code_type': result.code_type,
        'start_code': result.codes[0]
    }


def send_message(chat_id, text, type_code, username):
    """
    Данная функция добавляет сообщение в базу данных для дальнейшего сохранения
    
    :param chat_id: Номер чата
    
    :param text: Содержание сообщения
    
    :param type_code: Является ля
    
    :param username: Имя пользователя

    :return: Объект созданного сообщения
    """
    message = Message(text, username, chat_id, type_code)
    db.session.add(message)
    db.session.commit()
    return message


def get_messages(chat_id, username):
    """
    Данная функция передаёт сообщения из базы данных
    
    :param chat_id: Номер чата
    
    :param username:  Имя пользователя
    
    :return: Сообщения пользователей
    """
    chat = Chat.query.get(chat_id)
    result = []
    for message in chat.messages:
        if message.type == "usr":
            if message.author == username:
                type_msg = "mine"
            else:
                type_msg = "others"
        else:
            type_msg = "sys"
        result.append({
            "author": message.author,
            "message": message.content,
            "plain_message": plain_text(message.content),
            "type": type_msg
        })
    return result


def send_code(chat_id, text, username, parent=None, cname = u'Начальная версия'):
    """
    Отправление кода на сервер
    
    :param chat_id: Номер чата

    :param text: Код

    :param username: Имя пользователя

    :param parent: Место в дереве коммитов

    :return: Сообщение о коммите и номере кода
    """
    chat = Chat.query.get(chat_id)
    code_to_send = Code(text, username, chat_id, parent, cname)
    db.session.add(code_to_send)
    db.session.commit()
    code_id_in_chat = len(chat.codes) - 1
    sys_message(u"Изменение кода " + str(code_id_in_chat) + u" : '" + unicode(cname) + u"'", str(chat_id))
    sockets.send_code_sockets(chat_id)
    return code_to_send.id


def get_code(id):
    """
    Функция передаёт код с сервера пользователю
    
    :param id: идентификатор исходного кода
    
    :return: Автор и код
    """
    result = Code.query.get(id)
    return {
        "author": result.author,
        "code": result.content
    }


def find_chat(name):
    """
    Функция нахождения чата
    
    :param name: Имя чата
    
    :return: Все чаты, в название которых содержится имя чата
    """
    if name == '':
        return Chat.query.all()[:-10:-1]
    try:
        chat_id = int(name)
        return Chat.query.filter_by(id=chat_id).all()
    except ValueError:
        return Chat.query.filter(Chat.name.like('%'+name+'%')).all()[::-1]


def sys_message(data, room):
    """
    Системное сообщение
    
    :param data: Содержание сообщения
    
    :param room: Номер чата
    
    :return: Системное сообщение
    """
    send_message(int(room), data, 'sys', u'Системное сообщение')
    sockets.sys_message_sockets(data, room)


def get_commits_in_chat(chat_id):
    """
    Данная функция передаёт с сервера клиенту дерево коммитов
    
    :param chat_id: Номер чата
    
    :return: Дерево коммитов
    """
    return Code.query.filter_by(chat_link=chat_id)


def generate_commits_tree(chat_id):
    """
    Данная функция генерирует дерево коммитов для чата
    
    :param chat_id: Номер чата
    
    :return: Сгенерированное дерево коммитов
    """
    root_code = Code.get_root_in_chat(chat_id)
    tree = get_tree_node(root_code)
    return dumps(tree)


def get_tree_node(code):
    NODE_MARKUP = "<div class=\"commit_node circle unchosen\" data-id=\"{id}\">{id}</div>"
    node = {
        "text": {
            "name": code.id,
            "title": code.message
        },
        "innerHTML": NODE_MARKUP.format(id=code.id)
    }
    children = []
    for child_code in code.children:
        children.append(get_tree_node(child_code))
    node["children"] = children
    return node


def translate_text(text, lang):
    """
    Функция переводит текст

    :param text: Исходный тескт

    :param lang: Язык для перевода

    :return: Переведённый текст
    """
    return requests.get(app.config['YA_TL_URL'], {
        "key": app.config['API_KEY'],
        "text": plain_text(text),
        "lang": lang
        }).json()['text'][0]


def get_translated_message(chat_id, message_id):
    """
    Функция для перевода сообщений

    :param chat_id: ID чата

    :param message_id: ID сообщения

    :return: Переведённое сообщение
    """
    message = Message.query.filter_by(chat=chat_id)[message_id]
    return dumps({
        "no": message.content,
        "ru": message.content_ru,
        "en": message.content_en
        })


def plain_text(text):
    """
    Функция удаляет html-теги из текста

    :param text: Исходный текст

    :return: Текст без html-тегов
    """
    text = re.sub(r'\<[^>]*>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def message_escape(text):
    """
    Функция экранирует текст

    :param text: Исходный текст

    :return: Экранированный текст
    """
    text = text.replace('```', '`')
    parts = text.split('`')
    for i in range(0, len(parts), 2):
        parts[i] = cgi.escape(parts[i])
    return '`'.join(parts)
