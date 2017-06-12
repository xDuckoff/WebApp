# -*- coding: utf-8 -*-

"""Основные веб-страницы проекта"""

import os
import cgi
from json import dumps
from flask import render_template, redirect, session, request, send_from_directory
from application import app
from forms import LoginForm, CreateChatForm
from application.models import Chat


@app.route('/logout')
def logout():
    """Функция выхода из сессии в проекте

    :return: Переход на главную страницу
    """
    session.clear()
    return redirect('/')


@app.route('/translate')
def translate():
    """Функция перевода страницы

    :return: Запрос на сервера Яндекса, для перевода страницы
    """
    chat_id = int(request.args['chat'])
    message_id = int(request.args['index'])
    chat = Chat.get(chat_id)
    try:
        message = chat.messages[message_id]
    except IndexError:
        return 'No index', 400
    return dumps(message.translate())


@app.route('/', methods=['GET', 'POST'])
def index():
    """Данная функция генерирует главную страницу для пользователя

    :return: Главная страница с чатами пользователя, является ли человек \
    в сессии, формой входа(Если человек не зарегистрирован, заголовок чата
    """
    chat_title = request.args.get('search_title_text', '')
    chats = Chat.find(chat_title)
    chat_create_form = CreateChatForm()
    login_form = LoginForm()
    if login_form.validate_on_submit():
        session['login'] = cgi.escape(login_form.login.data)
        session['joined_chats'] = []
    if 'login' in session:
        login = session['login']
    else:
        login = ""
    allowed_ex = ['.' + x for x in app.config["ALLOWED_EXTENSIONS"]]
    return render_template('index.html',
                           chats=chats,
                           in_session=bool(login),
                           login_form=login_form,
                           chat_create_form=chat_create_form,
                           search_title_text=chat_title,
                           login=login,
                           allowed_ex=",".join(allowed_ex)
                          )


@app.route('/documentation/<path:filename>')
def docs_page(filename):
    """Данная функция открывает пользователю страницу с документацией

    :param filename: Имя файла
    :return: Выбранный файл с документацией
    """
    rootdir = os.getcwd()
    path = rootdir + '/docs/_build/html/'
    return send_from_directory(path, filename)

import application.chat_router
