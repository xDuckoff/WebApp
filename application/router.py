# -*- coding: utf-8 -*-

from flask import render_template, redirect, session, url_for, request
from application import app, chat
from forms import LoginForm, login_user, IsInSession
import requests


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


@app.route('/', methods=['GET', 'POST'])
def index():
    chat_title = request.args.get('search_title_text', '')
    chats=chat.find_chat(chat_title)
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.login.data)
    return render_template('index.html', chats=chats, in_session=IsInSession(), form=form, search_title_text=chat_title)


import application.chat.router
