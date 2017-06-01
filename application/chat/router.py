# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, session, flash
from application import app
from json import dumps 
from application import chat, csrf
from application.forms import CreateChatForm
from application.handlers import login_required, csrf_required


@app.route('/add_chat')
@login_required
@csrf_required
def add_chat():
    """
    Данная функция добавляет в сессию пользователя номер чата
    
    :return: Добавлен ли пользователь в чат
    """
    try:
        chat_id = int(request.args['chat'])
    except ValueError:
        return dumps({"success": False, "error": "Bad Chat ID"}), 400
    if chat_id not in session['joined_chats']:
        chat.sys_message(session['login'] + u" присоединился", chat_id)
        session['joined_chats'].append(chat_id)
        session.modified = True
    return dumps({"success": True, "error": ""})


@app.route('/tree', methods=['GET', 'POST'])
@login_required
@csrf_required
def tree():
    """
    Данная функция создаёт дерево коммитов чата
    
    :return: Страницу дерева коммитов
    """
    chat_id = int(request.args['chat'])
    return chat.generate_commits_tree(chat_id)


@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
@login_required
def chat_page(chat_id):
    """
    Данная функция возвращает пользователю страницу чата по номеру
    
    :param chat_id: Номер чата
    
    :return: Страница чата
    """
    if not chat.get_chat_info(chat_id):
        flash(u'Такого чата не существует!')
        return redirect('/')
    chat_info = chat.get_chat_info(chat_id)
    if 'login' in session:
        login = session['login']
        in_session = True
    else:
        login = ""
        in_session = False
    return render_template('chat.html', chat_id=chat_id, socket_mode=(app.config['SOCKET_MODE'] == 'True'), chat_info=chat_info, login=login, in_session=in_session)


@app.route('/create_chat', methods=['GET', 'POST'])
@login_required
def create_chat():
    """
    Данная функция создаёт чат по параметрам
    
    :return: Новая страница чата
    """
    form = CreateChatForm()
    name = form.name.data
    if name == '':
        return redirect('/')
    if form.file.data.filename == '':
        code = form.code.data
    else:
        file = form.file.data
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
            code = file.read()
        else:
            return redirect('/')
    code_type = form.code_type.data
    if code_type not in ["C", "C#", "C++", "CSS", "HTML", "Java", "JavaScript", "Python"]:
        return redirect('/')
    chat_id = chat.create_chat(name, code, code_type, session['login'])
    return redirect('/chat/' + str(chat_id))


@app.route('/get_messages', methods=['GET', 'POST'])
@login_required
@csrf_required
def get_messages():
    """
    Функция принятия сообщений
    
    :return: Принято ли сообщение
    """
    chat_id = int(request.args['chat'])
    return dumps(chat.get_messages(chat_id, session['login']))


@app.route('/send_code', methods=['GET', 'POST'])
@login_required
@csrf_required
def send_code():
    """
    Данная функция отправляет код на сервер от клиента
    
    :return: Отправлен ли код
    """
    chat_id = int(request.args['chat'])
    code = request.args['code']
    parent = request.args['parent']
    cname = request.args['cname']
    code_id = chat.send_code(chat_id, code, session['login'], parent, cname)
    code_id_in_chat = chat.get_commits_in_chat(chat_id).count() - 1
    return dumps({"success": True, "error": "", "commit": code_id_in_chat})


@app.route('/get_code', methods=['GET', 'POST'])
@login_required
@csrf_required
def get_code():
    """
    Данная функция отправляет код с сервера к клиенту
    
    :return: Код
    """
    chat_id = int(request.args['chat'])
    index = int(request.args['index'])
    return dumps(chat.get_code(chat_id, index))


@app.route('/get_chat_info', methods=['GET', 'POST'])
@login_required
@csrf_required
def get_chat_info():
    """
    Данная функция передаёт информациб о чате от сервера к клиенту
    
    :return: Информация о чате
    """
    chat_id = int(request.args['chat'])
    return dumps(chat.get_chat_info(chat_id))


@app.route('/get_commits', methods=['GET', 'POST'])
@login_required
@csrf_required
def get_chat_commits():
    """
    Данная функция передаёт пользователю дерево коммитов исходного кода
    
    :return: Дерево коммитов
    """
    chat_id = int(request.args['chat'])
    return dumps(chat.generate_tree(chat_id))


@app.route('/api/create_chat', methods=['GET', 'POST'])
@csrf.exempt
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
