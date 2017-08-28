# -*- coding: utf-8 -*-

"""Web-Страницы чата"""

from json import dumps
from flask import render_template, request, redirect
from application import app, socketio
from application.forms import CreateChatForm, AuthChatForm, LoginForm, SendMessageForm, \
    GetTreeForm, GetMessagesForm, SendCodeForm, GetCodeForm, InitChatForm
from application.handlers import access_required, form_required
from application.models import Chat, Message, Code, User
from flask_socketio import join_room, leave_room


@app.route('/tree', methods=['GET'])
@form_required(GetTreeForm)
@access_required
def tree():
    """Данная функция создаёт дерево коммитов чата

    :return: Страницу дерева коммитов
    """
    get_tree_form = GetTreeForm(request.args)
    chat_id = get_tree_form.chat.data
    return dumps(Code.get_commits_tree(chat_id))


@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def chat_page(chat_id):
    """Данная функция возвращает пользователю страницу чата по номеру

    :param chat_id: Номер чата
    :return: Страница чата
    """
    chat_create_form = CreateChatForm()
    login_form = LoginForm()
    init_chat_form = InitChatForm()
    chat = Chat.get(chat_id)
    if not chat:
        return redirect('/')
    auth_form = AuthChatForm()
    if auth_form.validate_on_submit():
        access_key = auth_form.password.data
        User.set_access_key(chat_id, access_key)
    return render_template('chat.html',
                           chat_id=chat.id,
                           socket_mode=(app.config['SOCKET_MODE'] == 'True'),
                           chat_info=chat.get_info(),
                           login=User.get_login(),
                           login_form=login_form,
                           chat_create_form=chat_create_form,
                           init_chat_form=init_chat_form,
                           have_access=chat.is_access_key_valid(User.get_access_key(chat_id)),
                           auth_form=auth_form,
                           allowed_ex=",".join(['.' + i for i in app.config["ALLOWED_EXTENSIONS"]]),
                           allowed_languages=app.config["ALLOWED_LANGUAGES"],
                           initialized=chat.initialized
                          )


@app.route('/send_message', methods=['POST'])
@form_required(SendMessageForm)
@access_required
def send_message():
    """Данная функция отправляет сообщение пользователю

    :return: Отправилось ли сообщение
    """
    send_message_form = SendMessageForm()
    chat_id = send_message_form.chat.data
    message = send_message_form.message.data
    Message.send(chat_id, message, 'usr')
    return dumps({"success": True, "error": ""})


@app.route('/get_messages', methods=['GET'])
@form_required(GetMessagesForm)
@access_required
def get_messages():
    """Запрос получения новых сообщений в чате

    :return: Принято ли сообщение
    """
    get_messages_form = GetMessagesForm(request.args)
    chat_id = get_messages_form.chat.data
    last_message_id = get_messages_form.last_message_id.data
    chat = Chat.get(chat_id)
    return dumps(chat.get_last_messages(last_message_id))


@app.route('/send_code', methods=['POST'])
@form_required(SendCodeForm)
@access_required
def send_code():
    """Данная функция отправляет код на сервер от клиента

    :return: Отправлен ли код
    """
    send_code_form = SendCodeForm()
    chat_id = send_code_form.chat.data
    code = send_code_form.code.data
    parent = send_code_form.parent.data
    message = send_code_form.message.data
    code_id = Code.send(chat_id, code, parent, message)
    return dumps({"success": True, "error": "", "commit": code_id})


@app.route('/get_code', methods=['GET'])
@form_required(GetCodeForm)
def get_code():
    """Данная функция отправляет код с сервера к клиенту

    :return: Код
    """
    get_code_form = GetCodeForm(request.args)
    index = get_code_form.index.data
    return dumps(Code.get(index))


@app.route('/init_chat', methods=['POST'])
@form_required(InitChatForm)
@access_required
def init_chat():
    """Данная функция отправляет код с сервера к клиенту

    :return: Код
    """
    init_chat_form = InitChatForm()
    chat_id = init_chat_form.chat.data
    code_type = init_chat_form.code_type.data
    code = init_chat_form.code.data
    chat = Chat.get(chat_id)
    chat.initialized(code_type, code)
    return dumps({"success": True, "error": ""})


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
