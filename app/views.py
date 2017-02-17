# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, session, url_for, escape, request, Flask
from app import app, chats
from forms import LoginForm
from beaker.middleware import SessionMiddleware

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        #if request.method == 'POST':
        session['username'] = request.form
        return redirect('/chat/1')
    if 'username' in session :
        return redirect('/chat/1')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def chat_page(chat_id):
    return 'Chat page ' + str(chat_id)


@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    try:
        chat_id = int(request.args['chat'])
        message = [request.args['login'], request.args['message']]
        chats[chat_id].messages.append(message)
    except BaseException:
        return 'Error'
    return 'OK'


@app.route('/get_messages', methods=['GET', 'POST'])
def get_messages():
    try:
        chat_id = int(request.args['chat'])
        index = int(request.args['index'])
        return '<br>'.join(map(lambda x: x[0] + ' ' + x[1], chats[chat_id].messages[index:]))
    except BaseException:
        return 'Error'

app.secret_key = 'OMG_so_secret_SH1T'