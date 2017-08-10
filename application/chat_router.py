# -*- coding: utf-8 -*-

"""Web-Страницы чата"""

from json import dumps
from flask import render_template, redirect, request
from application import app, socketio
from application import csrf
from application.forms import CreateChatForm, AuthChatForm
from application.handlers import csrf_required, access_required
from application.models import Chat, Message, Code, User
from flask_socketio import join_room, leave_room


@app.route('/tree', methods=['GET', 'POST'])
@csrf_required
@access_required
def tree():
    """Данная функция создаёт дерево коммитов чата

    :return: Страницу дерева коммитов
    """
    chat_id = request.args.get('chat', '')
    if not Chat.was_created(chat_id):
        return 'Bad chat', 400
    return dumps(Code.get_commits_tree(int(chat_id)))


@app.route('/chat/<chat_id>', methods=['GET', 'POST'])
def chat_page(chat_id):
    """Данная функция возвращает пользователю страницу чата по номеру

    :param chat_id: Номер чата
    :return: Страница чата
    """
    if not Chat.was_created(chat_id):
        return redirect('/')
    chat = Chat.get(int(chat_id))
    auth_form = AuthChatForm()
    if auth_form.validate_on_submit():
        User.set_access_key(chat_id, auth_form.password.data)
    return render_template('chat.html',
                           chat_id=chat.id,
                           socket_mode=(app.config['SOCKET_MODE'] == 'True'),
                           chat_info=chat.get_info(),
                           login=User.get_login(),
                           have_access=chat.is_access_key_valid(User.get_access_key(chat_id)),
                           auth_form=auth_form
                          )


@app.route('/send_message', methods=['GET', 'POST'])
@csrf_required
@access_required
def send_message():
    """Данная функция отправляет сообщение пользователю

    :return: Отправилось ли сообщение
    """
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
@csrf_required
@access_required
def get_messages():
    """Запрос получения новых сообщений в чате

    :return: Принято ли сообщение
    """
    chat_id = request.args.get('chat', '')
    last_message_id = int(request.args.get('last_message_id', 0))
    if not Chat.was_created(chat_id):
        return 'Bad chat', 400
    chat = Chat.get(chat_id)
    return dumps(chat.get_last_messages(last_message_id))


@app.route('/send_code', methods=['GET', 'POST'])
@csrf_required
@access_required
def send_code():
    """Данная функция отправляет код на сервер от клиента

    :return: Отправлен ли код
    """
    chat_id = request.args.get('chat', '')
    code = request.args.get('code', '')
    parent = request.args.get('parent', '')
    message = request.args.get('message', '')
    if not Chat.was_created(chat_id):
        return dumps({"success": False, "error": "Bad chat"}), 400
    code_id = Code.send(chat_id, code, parent, message)
    return dumps({"success": True, "error": "", "commit": code_id})


@app.route('/get_code', methods=['GET', 'POST'])
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
    access_key = form.access_key.data
    chat_id = Chat.create(name, code, code_type, access_key)
    return '/chat/' + str(chat_id)


if app.config['SOCKET_MODE'] == 'True':

    @access_required
    @socketio.on('join')
    def on_join(room):
        """Данная функция сообщает о присоединение пользователя к чату

        :param room: номер чата
        :return: Системное сообщение о входе пользователя
        """
        join_room(room)

    @access_required
    @socketio.on('leave')
    def on_leave(room):
        """Данная функция удаляет человека из чата

        :param room: Номер чата
        """
        leave_room(room)
