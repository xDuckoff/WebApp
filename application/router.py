# -*- coding: utf-8 -*-

from flask import render_template, redirect, session, url_for, request
from application import app, chat
from forms import LoginForm, login_user, IsInSession


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


@app.route('/')
def index():
    chat_title = request.args.get('search_title_text', '')
    if chat_title == '':
        return render_template('index.html', chats=[])
    else:
        return render_template('index.html',chats=chat.find_chat(str(chat_title)))


import application.chat.router
