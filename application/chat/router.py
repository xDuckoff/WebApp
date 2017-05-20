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
    """
    Данная функция добавляет в сессию пользователя номер чата
    
    :return: Добавлен ли пользователь в чат
    """
    if not IsInSession():
        return dumps({"success": False, "error": "Login error"}), 403
    chat_id = request.args['chat_id']
    if chat_id not in session['joined_chats']:
        session['joined_chats'].append(chat_id)
        session.modified = True
    return dumps({"success": True, "error": ""})

@app.route('/tree', methods=['GET', 'POST'])
def tree():
    """
    Данная функция создаёт дерево коммитов чата
    
    :return: Страницу дерева коммитов
    """
    if not IsInSession():
        return 'Login error', 403
    chat_id = int(request.args['chat'])
    coms = chat.generate_commits_tree(chat_id)
    return render_template('commitsTree.html',commits = coms)

@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def chat_page(chat_id):
    """
    Данная функция возвращает пользователю страницу чата по номеру
    
    :param chat_id: Номер чата
    
    :return: Страница чата
    """
    if not IsInSession():
        flash(u'Вы не авторизированны!')
        return redirect('/')
    if not chat.get_chat_info(chat_id):
        flash(u'Такого чата не существует!')
        return redirect('/')
    chat_info = chat.get_chat_info(chat_id)
    return render_template('chat.html',chat_id=chat_id, socket_mode=(app.config['SOCKET_MODE'] == 'True'), disabled_login_btn=True, chat_info=chat_info)

@app.route('/create_chat', methods=['GET', 'POST'])
def create_chat():
    """
    Данная функция создаёт чат по параметрам
    
    :return: Новая страница чата
    """
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
    """
    Функция принятия сообщений
    
    :return: Принято ли сообщение
    """
    if not IsInSession():
        return 'Login error', 403
    chat_id = int(request.args['chat'])
    return dumps(chat.get_messages(chat_id, session['login']))

@app.route('/send_code', methods=['GET', 'POST'])
def send_code():
    """
    Данная функция отправляет код на сервер от клиента
    
    :return: Отправлен ли код
    """
    if not IsInSession():
        return dumps({"success": False, "error": "Login error"}), 403
    chat_id = int(request.args['chat'])
    code = request.args['code']
    parent = request.args['parent']
    code_id = chat.send_code(chat_id, code, session['login'], parent)
    return dumps({"success": True, "error": ""})


@app.route('/get_code', methods=['GET', 'POST'])
def get_code():
    """
    Данная функция отправляет код с сервера к клиенту
    
    :return: Код
    """
    if not IsInSession():
        return 'Login error', 403
    chat_id = int(request.args['chat'])
    index = int(request.args['index'])
    return dumps(chat.get_code(chat_id, index))

@app.route('/get_chat_info', methods=['GET', 'POST'])
def get_chat_info():
    """
    Данная функция передаёт информациб о чате от сервера к клиенту
    
    :return: Информация о чате
    """
    if not IsInSession():
        return 'Login error', 403
    chat_id = int(request.args['chat'])
    return dumps(chat.get_chat_info(chat_id))

@app.route('/get_commits', methods=['GET', 'POST'])
def get_chat_commits():
    """
    Данная функция передаёт пользователю дерево коммитов исходного кода
    
    :return: Дерево коммитов
    """
    if not IsInSession():
        return 'Login error', 403
    chat_id = int(request.args['chat'])
    return dumps(chat.generate_tree(chat_id))


@app.route('/api/create_chat', methods=['GET', 'POST'])
def API_create_chat():
    """
    Данная функция создаёт чат по параметрам, используется для api

    :return: Адрес новой страницы чата
    """
    form = CreateChatForm()
    name = form.name.data
    code = form.code.data
    code_type = form.code_type.data
    chat_id = chat.create_chat(name, code, code_type, "Sublime bot")
    return '/chat/' + str(chat_id)
