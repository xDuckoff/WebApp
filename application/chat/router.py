from flask import render_template, redirect, request, session
from application import app, socketio
from json import dumps
from application import chat
from application.forms import IsInSession, CreateChatForm, allowed_file
from flask_socketio import send, emit, join_room, leave_room

@socketio.on('message')
def handle_message(json):
    chat_id = int(json['room'])
    chat.send_message(chat_id, json['message'], 'usr')
    send({'message':json['message'], 'author':session['login'], 'type':'usr'}, json=True, room=json['room'], broadcast=True)

@socketio.on('join')
def on_join(room):
    join_room(room)
    sys_message(str(session['login']) + " joined", room)

def sys_message(data, room):
    chat.send_message(int(room), data, 'sys')
    socketio.send({'message':data, 'author':'System', 'type':'sys'}, json=True, room=room, broadcast=True)

@socketio.on('leave')
def on_leave(room):
    leave_room(room)


@app.route('/chat/<chat_id>', methods=['GET', 'POST'])
def chat_page(chat_id):
    if not(IsInSession()):
        return redirect('/login?chat=' + str(chat_id))
    try:
        chat_id = int(chat_id)
        return render_template('chat.html')
    except ValueError:
        return 'Not Found', 404


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
    chat_id = chat.create_chat(name)
    chat.send_code(chat_id, code)
    return redirect('/chat/' + str(chat_id))


@app.route('/get_messages', methods=['GET', 'POST'])
def get_messages():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    return dumps(chat.get_messages(chat_id))


@app.route('/send_code', methods=['GET', 'POST'])
def send_code():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    code = request.args['code']
    if len(code) > 0:
        code_id = chat.send_code(chat_id, code)
        sys_message("New Commit " + str(code_id), chat_id)
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
