# -*- coding: utf-8 -*-

from flask import session
from application.models import Message, Code, Chat
from application import db
from application import app
import sockets
import cgi
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
    send_code(chat_id, code, username, 0)
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
    return {'name':result.name, 'code_type':result.code_type}

def send_message(id, text, type, username):
    """
    Данная функция добавляет сообщение в базу данных для дальнейшего сохранения
    
    :param id: Номер чата
    
    :param text: Содержание сообщения
    
    :param type: Является ля
    
    :param username: Имя пользователя
    """
    text_ru = translate_text(text, 'ru')
    text_en = translate_text(text, 'en')
    db.session.add(Message(text, text_ru, text_en, username, id, type))
    db.session.commit()

def get_messages(id, username):
    """
    Данная функция передаёт сообщения из базы данных
    
    :param id: Номер чата
    
    :param username:  Имя пользователя
    
    :return: Сообщения пользователей
    """
    result = Message.query.filter_by(chat=id)
    ret = []
    for i in result:

        if i.type == "usr":
            if i.author == username:
                type = "mine"
            else:
                type = "others"
        else:
            type = "sys"

        ret.append({"author": i.author, "message": i.content, "plain_message": plain_text(i.content), "type": type})
    return ret

def send_code(id, text, username, parent, cname = u'Начальная версия'):
    """
    Отправление кода на сервер
    
    :param id: Номер чата
    
    :param text: Код
    
    :param username: Имя пользователя
     
    :param parent: Место в дереве коммитов
    
    :return: Сообщение о коммите и номере кода
    """
    CodeToSend = Code(text, username, id, parent, cname)
    db.session.add(CodeToSend)
    db.session.commit()
    code_id = CodeToSend.id
    code_id_in_chat = len(Code.query.filter_by(chat=id).all()) - 1
    sys_message(u"Изменение кода " + str(code_id_in_chat) + u" : '" + unicode(cname) + u"'", str(id))
    sockets.send_code_sockets(id)
    return code_id

def get_code(id, index):
    """
    Функция передаёт код с сервера пользователю
    
    :param id: Номер чата
    
    :param index: Индекс
    
    :return: Автор и код
    """
    result = Code.query.filter_by(chat=id)[index]
    return {"author": result.author, "code": result.content}

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

def get_commits_in_chat(chat):
    """
    Данная функция передаёт с сервера клиенту дерево коммитов
    
    :param chat: Номер чата
    
    :return: Дерево коммитов
    """
    return Code.query.filter_by(chat=chat)

def generate_commits_tree(chat):
    """
    Данная функция генерирует дерево коммитов для чата
    
    :param chat: Номер чата
    
    :return: Сгенерированное дерево коммитов
    """
    commits = get_commits_in_chat(chat)
    commits_data = [{"children": []} for i in range(0, commits.count())]
    
    commits_data[0] = {"text": "{name: '0'}", "children":[],
                       "innerHTML":"<div class = \"circle unchosen\" onclick = \"choose_node(0)\" id=\"commit-button0\">0</div>"}
    for index in range(commits.count() - 1, 0, -1):
        commit = commits[index]
        commits_data[index]["text"] = {"name": str(index)}
        commits_data[index]["innerHTML"] = "<div class = \"circle unchosen\" onclick = \"{0}\" id=\"commit-button{1}\">{1}</div".format('choose_node('+str(index)+')', str(index))
        commits_data[commit.parent]["children"].append(commits_data[index])
    return dumps(commits_data[0])

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
