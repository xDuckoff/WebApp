# -*- coding: utf-8 -*-

from flask import render_template, redirect, session, url_for, request
from app import app, chats
from chat import make_session
from forms import LoginForm
from json import dumps
from chat import Chat

login = 'login'


def IsInSession():
    if login in session:
        return True
    return False


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    numberofchat = request.args.get('chat','')
    link = (numberofchat == '')* '/' + (not numberofchat == '') * ('chat/'+numberofchat)
    if form.validate_on_submit():
        make_session(form.login.data)
        return redirect(link)
    if IsInSession():
        return redirect(link)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if not(IsInSession()): return redirect('/login')
    session.pop('login', None)
    return redirect(url_for('index'))    


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def chat_page(chat_id):
    if not(IsInSession()): return redirect('/login?chat=' + str(chat_id))
    return render_template('chat.html')

@app.route('/create_chat')
def create_chat():
    chats.append(Chat())
    return redirect('/chat/'+str(len(chats)))

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    if len(request.args['message']) > 0:
        chats[chat_id].send_message(request.args['message'])


@app.route('/get_messages', methods=['GET', 'POST'])
def get_messages():
    if not(IsInSession()):
        print 'redirect'
        return redirect('/login')
    chat_id = int(request.args['chat'])
    index = int(request.args['index'])
    return dumps(chats[chat_id].get_messages(index))

app.secret_key = '~\xe1\xa4EsQ\xf1\xf6\xfb\x92\x1e\x85\xfb\x9b\x07K\xef\x9cL`\x0e"\x07\xa8'