# -*- coding: utf-8 -*-

"""Web-Страницы чата"""

from flask import render_template, redirect, request, session
from application import app, socketio
from json import dumps 
from application import csrf
from application.forms import CreateChatForm
from application.handlers import login_required, csrf_required
from application.models import Chat, Message, Code


@app.route('/add_chat')
@login_required
@csrf_required
def add_chat():
    """Данная функция добавляет в сессию пользователя номер чата
    
    :return: Добавлен ли пользователь в чат
    """
    try:
        chat_id = int(request.args['chat'])
    except ValueError:
        return dumps({"success": False, "error": "Bad Chat ID"}), 400
    if chat_id not in session['joined_chats']:
        Message.send(chat_id, session['login'] + u" присоединился", 'sys')
        session['joined_chats'].append(chat_id)
        session.modified = True
    return dumps({"success": True, "error": ""})


@app.route('/tree', methods=['GET', 'POST'])
@login_required
@csrf_required
def tree():
    """Данная функция создаёт дерево коммитов чата
    
    :return: Страницу дерева коммитов
    """
    chat_id = int(request.args['chat'])
    return dumps(Code.get_commits_tree(chat_id))


@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
@login_required
def chat_page(chat_id):
    """Данная функция возвращает пользователю страницу чата по номеру

    :param chat_id: Номер чата
    :return: Страница чата
    """
    chat = Chat.get(chat_id)
    if 'login' in session:
        login = session['login']
        in_session = True
    else:
        login = ""
        in_session = False
    return render_template(
        'chat.html',
        chat_id=chat_id,
        socket_mode=(app.config['SOCKET_MODE'] == 'True'),
        chat_info=chat.get_info(),
        login=login,
        in_session=in_session
    )


@app.route('/create_chat', methods=['GET', 'POST'])
@login_required
def create_chat():
    """Данная функция создаёт чат по параметрам

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
    chat_id = Chat.create(name, code, code_type, session['login'])
    return redirect('/chat/' + str(chat_id))


@app.route('/get_messages', methods=['GET', 'POST'])
@login_required
@csrf_required
def get_messages():
    """Функция принятия сообщений

    :return: Принято ли сообщение
    """
    chat_id = int(request.args['chat'])
    chat = Chat.get(chat_id)
    return dumps(chat.get_messages(session['login']))


@app.route('/translate')
def translate():
    """Функция перевода страницы

    :return: Запрос на сервера Яндекса, для перевода страницы
    """
    chat_id = int(request.args['chat'])
    message_id = int(request.args['index'])
    chat = Chat.get(chat_id)
    try:
        message = chat.messages[message_id]
    except IndexError:
        return 'No index', 400
    return dumps(message.translate())


@app.route('/send_code', methods=['GET', 'POST'])
@login_required
@csrf_required
def send_code():
    """Данная функция отправляет код на сервер от клиента

    :return: Отправлен ли код
    """
    chat_id = int(request.args['chat'])
    code = request.args['code']
    parent = request.args['parent']
    cname = request.args['cname']
    code_id = Code.send(chat_id, code, session['login'], parent, cname)
    return dumps({"success": True, "error": "", "commit": code_id})


@app.route('/get_code', methods=['GET', 'POST'])
@login_required
@csrf_required
def get_code():
    """Данная функция отправляет код с сервера к клиенту

    :return: Код
    """
    index = int(request.args['index'])
    return dumps(Code.get(index))


@app.route('/get_chat_info', methods=['GET', 'POST'])
@login_required
@csrf_required
def get_chat_info():
    """Данная функция передаёт информациб о чате от сервера к клиенту

    :return: Информация о чате
    """
    chat_id = int(request.args['chat'])
    chat = Chat.get(chat_id)
    return dumps(chat.get_info())


@app.route('/api/create_chat', methods=['GET', 'POST'])
@csrf.exempt
def API_create_chat():
    """Данная функция создаёт чат по параметрам, используется для api

    :return: Адрес новой страницы чата
    """
    form = CreateChatForm()
    name = form.name.data
    code = form.code.data
    code_type = form.code_type.data
    chat_id = Chat.create(name, code, code_type, "Sublime bot")
    return '/chat/' + str(chat_id)


if app.config['SOCKET_MODE'] == 'True':
    from flask_socketio import join_room, leave_room


    @socketio.on('message')
    def handle_message(json):
        """Данная функция принимает сообщения от пользователя через сокеты

        :param json: json запрос
        :return: Сообщние
        """
        chat_id = int(json['room'])
        try:
            Message.send(chat_id, json['message'], 'usr', session['login'])
        except OverflowError:
            pass


    @socketio.on('join')
    def on_join(room):
        """Данная функция сообщает о присоединение пользователя к чату

        :param room: номер чата
        :return: Системное сообщение о входе пользователя
        """
        join_room(room)


    @socketio.on('leave')
    def on_leave(room):
        """Данная функция удаляет человека из чата

        :param room: Номер чата
        """
        leave_room(room)

else:
    @app.route('/send_message', methods=['GET', 'POST'], endpoint='send_message')
    @login_required
    @csrf_required
    def send_message():
        """Данная функция отправляет сообщение пользователю

        :return: Отправилось ли сообщение
        """
        chat_id = int(request.args['chat'])
        message = request.args['message']
        try:
            Message.send(chat_id, message, 'usr', session['login'])
        except OverflowError:
            result = {"success": False, "error": "Length Limit(1, 1000)"}
        else:
            result = {"success": True, "error": ""}
        return dumps(result)
