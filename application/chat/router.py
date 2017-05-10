# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, session, flash, url_for
from application import app
from json import dumps 
from application import chat
from application.forms import IsInSession, CreateChatForm, allowed_file
import markdown
import cgi

@app.route('/add_chat')
def add_chat():
    if not IsInSession():
        return dumps({"success": False, "error": "Login error"}), 403
    chat_id = request.args['chat_id']
    if chat_id not in session['joined_chats']:
        session['joined_chats'].append(chat_id)
        session.modified = True
    return dumps({"success": True, "error": ""})

@app.route('/tree', methods=['GET', 'POST'])
def tree():
    if not IsInSession():
        return 'Login error', 403
    chat_id = int(request.args['chat'])
    coms = chat.generate_commits_tree(chat_id)
    return render_template('commitsTree.html',commits = coms)

@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def chat_page(chat_id):
    if not IsInSession():
        flash(u'Вы не авторизированны!')
        return redirect('/')
    if not chat.get_chat_info(chat_id):
        flash(u'Такого чата не существует!')
        return redirect('/')
    return render_template('chat.html',chat_id=chat_id, socket_mode=(app.config['SOCKET_MODE'] == 'True'), disabled_login_btn=True)

@app.route('/create_chat', methods=['GET', 'POST'])
def create_chat():
    if not IsInSession():
        return 'Login error', 403
    form = CreateChatForm()
    name = form.name.data
    if form.file.data.filename == '':
        code = form.code.data
    else:
        file = form.file.data
        if file and allowed_file(file.filename):
            code = file.read()
        else:
            return redirect('/')
    code_type = form.code_type.data
    chat_id = chat.create_chat(name, code, code_type, session['login'])
    return redirect('/chat/' + str(chat_id))

@app.route('/get_messages', methods=['GET', 'POST'])
def get_messages():
    if not IsInSession():
        return 'Login error', 403
    chat_id = int(request.args['chat'])
    return dumps(chat.get_messages(chat_id, session['login']))

@app.route('/send_code', methods=['GET', 'POST'])
def send_code():
    if not IsInSession():
        return dumps({"success": False, "error": "Login error"}), 403
    chat_id = int(request.args['chat'])
    code = request.args['code']
    parent = request.args['parent']
    code_id = chat.send_code(chat_id, code, session['login'], parent)
    return dumps({"success": True, "error": ""})


@app.route('/get_code', methods=['GET', 'POST'])
def get_code():
    if not IsInSession():
        return 'Login error', 403
    chat_id = int(request.args['chat'])
    index = int(request.args['index'])
    return dumps(chat.get_code(chat_id, index))

@app.route('/get_chat_info', methods=['GET', 'POST'])
def get_chat_info():
    if not IsInSession():
        return 'Login error', 403
    chat_id = int(request.args['chat'])
    return dumps(chat.get_chat_info(chat_id))

@app.route('/get_commits', methods=['GET', 'POST'])
def get_chat_commits():
    if not IsInSession():
        return 'Login error', 403
    chat_id = int(request.args['chat'])
    return dumps(chat.generate_tree(chat_id))
