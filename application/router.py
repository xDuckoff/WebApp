# -*- coding: utf-8 -*-

from flask import render_template, redirect, session, url_for, request
from application import app, chat
from forms import LoginForm, login_user, IsInSession
import requests


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if 'chat' in request.args:
        link = '/chat/' + request.args['chat']
    else:
        link = '/'
    if form.validate_on_submit():
        login_user(form.login.data)
        return redirect(link)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('login', None)
    return redirect('/')    


@app.route('/translate-test')
def translate_page():
    return render_template('translate.html')


@app.route('/translate')
def translate():
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    return requests.get(url, {
        "key": app.config['API_KEY'],
        "text": request.args["text"],
        "lang": "ru"
        }).content


@app.route('/')
def index():
    chat_title = request.args.get('search_title_text', '')
    if chat_title == '':
        chats = []
    else:
        chats=chat.find_chat(str(chat_title))
    return render_template('index.html', chats=chats, in_session=IsInSession())


import application.chat.router
