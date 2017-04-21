from flask import render_template, redirect, request, session
from application import app, socketio
from json import dumps
from application import chat
from application.forms import IsInSession, CreateChatForm, allowed_file
from flask_socketio import send, emit, join_room, leave_room

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

@app.route('/treePage', methods=['GET', 'POST'])
def treePage():
    return render_template('treeTest.html')

@app.route('/tree', methods=['GET', 'POST'])
def tree():
    coms = [
        {'id':1, 'parent':0, 'head': "1"},
        {'id':2, 'parent':1, 'head': "0"},
        {'id':3, 'parent':1, 'head': "0"},
        {'id':4, 'parent':2, 'head': "0"}
    ]
    return render_template('commitsTree.html',commits = coms)

@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def chat_page(chat_id):
    if not(IsInSession()):
        return redirect('/login?chat=' + str(chat_id))
    return render_template('chat.html')


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
    index = int(request.args['index'])
    return dumps(chat.get_code(index))

@app.route('/get_chat_info', methods=['GET', 'POST'])
def get_chat_info():
    chat_id = int(request.args['chat'])
    return dumps(chat.get_chat_info(chat_id))

@app.route('/get_commits', methods=['GET', 'POST'])
def get_chat_commits():
    chat_id = int(request.args['chat'])
    return dumps(chat.generate_tree(chat_id))
