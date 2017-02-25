# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, session, url_for, escape, request, Flask
from app import app, chats
from chat import make_session
from forms import LoginForm, BeakerSessionInterface
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        #if request.method == 'POST':
        make_session(request.form)
        return redirect('/chat/1')
    if 'login' in session :
        return redirect('/chat/1')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('index'))


@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def chat_page(chat_id):
    return 'Chat page ' + str(chat_id)


@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    try:
        chat_id = int(request.args['chat'])
        chats[chat_id].Send_message(request.args['message'])
    except BaseException:
        return 'Error'
    return 'OK'


@app.route('/get_messages', methods=['GET', 'POST'])
def get_messages():
    try:
        chat_id = int(request.args['chat'])
        index = int(request.args['index'])
        return '<br>'.join(map(lambda x: x[0] + ' ' + x[1], chats[chat_id].messages[index:].text))
    except BaseException:
        return 'Error'

app.secret_key = '~\xe1\xa4EsQ\xf1\xf6\xfb\x92\x1e\x85\xfb\x9b\x07K\xef\x9cL`\x0e"\x07\xa8'
