# -*- coding: utf-8 -*-

from flask import render_template, redirect, session, url_for, request, send_from_directory, abort
from application import app, chat
from forms import LoginForm, login_user, IsInSession
import requests, os

"""
Данный файл содержит основные страницы проекта.
"""

@app.route('/logout')
def logout():
    """
    Функция выхода из сессиии в проекте
    
    :return: Переход на главную страницу
    """
    session.pop('login', None)
    return redirect('/')    


@app.route('/translate')
def translate():
    """
    Функция перевода страницы
    
    :return: Запрос на сервера Яндекса, для перевода страницы
    """
    try:
        chat_id = int(request.args['chat'])
        message_id = int(request.args['index'])
    except ValueError:
        abort(400)
    try:
        return chat.get_translated_message(chat_id, message_id)
    except IndexError:
        return 'No index', 400



@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Данная функция генерирует главную страницу для пользователя
    
    :return: Главная страница с чатами пользователя, является ли человек в сессии, формой входа(Если человек не 
    зарегистрирован, заголовок чата
    """
    chat_title = request.args.get('search_title_text', '')
    chats=chat.find_chat(chat_title)
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.login.data)
    if 'login' in session:
        login = session['login']
    else:
        login = ""
    return render_template('index.html', chats=chats, in_session=IsInSession(), form=form, search_title_text=chat_title, login=login)


@app.route('/documentation/<path:filename>')
def docs_page(filename):
    """
    Данная функция открывает пользователю страницу с документацией
    
    :param filename: Имя файла
    
    :return: Выбранный файл с документацией
    """
    rootdir = os.getcwd()
    path = rootdir + '/docs/_build/html/'
    return send_from_directory(path, filename)



from application.chat.sockets import init_sockets
init_sockets()

import application.chat.router