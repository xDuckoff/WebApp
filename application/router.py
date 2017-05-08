# -*- coding: utf-8 -*-

from flask import render_template, redirect, session, url_for, request
from application import app, chat
from forms import LoginForm, login_user, IsInSession


@app.route('/logout')
def logout():
    session.pop('login', None)
    return redirect('/')    


@app.route('/', methods=['GET', 'POST'])
def index():
    chat_title = request.args.get('search_title_text', '')
    chats=chat.find_chat(str(chat_title))
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.login.data)
    return render_template('index.html', chats=chats, in_session=IsInSession(), form=form)


import application.chat.router
