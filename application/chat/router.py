from flask import render_template, redirect, request, session
from application import app
from json import dumps
from application import chat
from application.forms import IsInSession, CreateChatForm, allowed_file
from application import app

if app.config['SOCKET_MODE'] == 'True':
    from application import socketio
    from flask_socketio import send, emit, join_room, leave_room

if app.config['SOCKET_MODE'] == 'True':
    @socketio.on('message')
    def handle_message(json):
        chat_id = int(json['room'])
        chat.send_message(chat_id, json['message'], 'usr', session['login'])
        socketio.emit('message', {'message':json['message'], 'author':session['login'], 'type':'usr'}, json=True, room=json['room'], broadcast=True)


    @socketio.on('join')
    def on_join(room):
        join_room(room)
        chat.sys_message(str(session['login']) + " joined", room)


    @socketio.on('leave')
    def on_leave(room):
        leave_room(room)


@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def chat_page(chat_id):
    if not(IsInSession()):
        return redirect('/login?chat=' + str(chat_id))
    return render_template('chat.html', socket_mode=(app.config['SOCKET_MODE'] == 'True'))


@app.route('/create_chat', methods=['GET', 'POST'])
def create_chat():
    if not(IsInSession()):
        return redirect('/login')
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
    chat_id = chat.create_chat(name, code, session['login'])
    return redirect('/chat/' + str(chat_id))


if app.config['SOCKET_MODE'] == 'False':
    @app.route('/send_message', methods=['GET', 'POST'])
    def send_message():
        if not(IsInSession()):
            return redirect('/login')
        chat_id = int(request.args['chat'])
        message = request.args['message']
        if len(message) > 0:
            chat.send_message(chat_id, message, "usr", session['login'])
        return 'OK'


@app.route('/get_messages', methods=['GET', 'POST'])
def get_messages():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    return dumps(chat.get_messages(chat_id, session['login']))

@app.route('/send_code', methods=['GET', 'POST'])
def send_code():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    code = request.args['code']
    code_id = chat.send_code(chat_id, code, session['login'])
    return 'OK'


@app.route('/get_code', methods=['GET', 'POST'])
def get_code():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    index = int(request.args['index'])
    return dumps(chat.get_code(chat_id, index))

@app.route('/get_chat_info', methods=['GET', 'POST'])
def get_chat_info():
    chat_id = int(request.args['chat'])
    return dumps(chat.get_chat_info(chat_id))
