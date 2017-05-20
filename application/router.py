# -*- coding: utf-8 -*-

from flask import render_template, redirect, session, url_for, request, send_from_directory
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


@app.route('/translate-test')
def translate_page():
    """
    Функция перевода страницы
    
    :return: Переведённую страницу
    """
    return render_template('translate.html')


@app.route('/translate')
def translate():
    """
    Функция перевода страницы
    
    :return: Запрос на сервера Яндекса, для перевода страницы
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    return requests.get(url, {
        "key": app.config['API_KEY'],
        "text": request.args["text"],
        "lang": "ru"
        }).content


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
    return render_template('index.html', chats=chats, in_session=IsInSession(), form=form, search_title_text=chat_title)


@app.route('/d/<path:filename>')
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