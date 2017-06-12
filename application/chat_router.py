# -*- coding: utf-8 -*-

"""Web-Страницы чата"""

from json import dumps
from flask import render_template, redirect, request, session
from application import app, socketio
from application import csrf
from application.forms import CreateChatForm
from application.handlers import login_required, csrf_required
from application.models import Chat, Message, Code, User
from flask_socketio import join_room, leave_room


@app.route('/join_chat', methods=['GET', 'POST'])
@login_required
@csrf_required
def join_chat():
    """Данная функция добавляет в сессию пользователя номер чата

    :return: Добавлен ли пользователь в чат
    """
    chat_id = request.args.get('chat', '')
    if not Chat.was_created(chat_id):
        return dumps({"success": False, "error": "Bad chat"}), 400
    if User.join_chat(int(chat_id)):
        Message.send(chat_id, u"Присоединился к чату", 'sys')
    return dumps({"success": True, "error": ""})


@app.route('/tree', methods=['GET', 'POST'])
@login_required
@csrf_required
def tree():
    """Данная функция создаёт дерево коммитов чата

    :return: Страницу дерева коммитов
    """
    chat_id = request.args.get('chat', '')
    if not Chat.was_created(chat_id):
        return 'Bad chat', 400
    return dumps(Code.get_commits_tree(int(chat_id)))


@app.route('/chat/<chat_id>', methods=['GET', 'POST'])
@login_required
def chat_page(chat_id):
    """Данная функция возвращает пользователю страницу чата по номеру

    :param chat_id: Номер чата
    :return: Страница чата
    """
    if not Chat.was_created(chat_id):
        return redirect('/')
    chat = Chat.get(int(chat_id))
    return render_template('chat.html',
                           chat_id=chat.id,
                           socket_mode=(app.config['SOCKET_MODE'] == 'True'),
                           chat_info=chat.get_info(),
                           login=User.get_login(),
                           in_session=User.is_logined()
                          )


@app.route('/send_message', methods=['GET', 'POST'])
@login_required
@csrf_required
def send_message():
    """Данная функция отправляет сообщение пользователю

    :return: Отправилось ли сообщение
    """
    if app.config['SOCKET_MODE'] == 'True':
        return dumps({"success": False, "error": "Bad mode"}), 400
    chat_id = request.args.get('chat', '')
    message = request.args.get('message', '')
    if not Chat.was_created(chat_id):
        return dumps({"success": False, "error": "Bad chat"}), 400
    try:
        Message.send(chat_id, message, 'usr')
    except OverflowError:
        return dumps({"success": False, "error": "Length Limit(1, 1000)"}), 400
    else:
        return dumps({"success": True, "error": ""})


@app.route('/get_messages', methods=['GET', 'POST'])
@login_required
@csrf_required
def get_messages():
    """Функция принятия сообщений

    :return: Принято ли сообщение
    """
    chat_id = request.args.get('chat', '')
    if not Chat.was_created(chat_id):
        return 'Bad chat', 400
    chat = Chat.get(chat_id)
    return dumps(chat.get_messages())


@app.route('/translate')
def translate():
    """Функция перевода страницы

    :return: Запрос на сервера Яндекса, для перевода страницы
    """
    chat_id = request.args.get('chat', '')
    message_id = request.args.get('index', '')
    if not Chat.was_created(chat_id):
        return 'Bad chat', 400
    chat = Chat.get(chat_id)
    if not chat.has_message(message_id):
        return 'Bad message', 400
    message = chat.messages[int(message_id)]
    return dumps(message.translate())


@app.route('/send_code', methods=['GET', 'POST'])
@login_required
@csrf_required
def send_code():
    """Данная функция отправляет код на сервер от клиента

    :return: Отправлен ли код
    """
    chat_id = request.args.get('chat', '')
    code = request.args.get('code', '')
    parent = request.args.get('parent', '')
    cname = request.args.get('cname', '')
    if not Chat.was_created(chat_id):
        return dumps({"success": False, "error": "Bad chat"}), 400
    code_id = Code.send(chat_id, code, parent, cname)
    return dumps({"success": True, "error": "", "commit": code_id})


@app.route('/get_code', methods=['GET', 'POST'])
@login_required
@csrf_required
def get_code():
    """Данная функция отправляет код с сервера к клиенту

    :return: Код
    """
    index = int(request.args.get('index', ''))
    return dumps(Code.get(index))


@app.route('/api/create_chat', methods=['GET', 'POST'])
@csrf.exempt
def api_create_chat():
    """Данная функция создаёт чат по параметрам, используется для api

    :return: Адрес новой страницы чата
    """
    form = CreateChatForm()
    name = form.name.data
    code = form.code.data
    code_type = form.code_type.data
    chat_id = Chat.create(name, code, code_type)
    return '/chat/' + str(chat_id)


if app.config['SOCKET_MODE'] == 'True':

    @socketio.on('message')
    def handle_message(json):
        """Данная функция принимает сообщения от пользователя через сокеты

        :param json: json запрос
        :return: Сообщение
        """
        chat_id = json.get('room', '')
        if not Chat.was_created(chat_id):
            return
        try:
            Message.send(chat_id, json.get('message', ''), 'usr')
        except OverflowError:
            return

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
