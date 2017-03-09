from flask import render_template, redirect, request
from application import app, chats
from json import dumps
from application.chat import Chat
from application.forms import IsInSession


@app.route('/chat/<chat_id>', methods=['GET', 'POST'])
def chat_page(chat_id):
    if not(IsInSession()):
        return redirect('/login?chat=' + str(chat_id))
    if chat_id.isdigit():
        return render_template('chat.html')
    else:
        for i in chats:
            if i.name == chat_id:
                chat_id = i.id
                return render_template('chat.html')
    return 'Not Found', 404


@app.route('/create_chat')
def create_chat():
    if not(IsInSession()):
        return redirect('/login')
    try:
        name = request.args['name']
    except IndexError:
        return redirect('/')
    chats.append(Chat(name))
    return redirect('/chat/'+chats[-1].name)


@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    if len(request.args['message']) > 0:
        chats[chat_id].send_message(request.args['message'])
    return 'OK'


@app.route('/get_messages', methods=['GET', 'POST'])
def get_messages():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    index = int(request.args['index'])
    return dumps(chats[chat_id].get_messages(index))


@app.route('/send_code', methods=['GET', 'POST'])
def send_code():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    if len(request.args['code']) > 0:
        chats[chat_id].send_code(request.args['code'])
    return 'OK'


@app.route('/get_code', methods=['GET', 'POST'])
def get_code():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    index = int(request.args['index'])
    return dumps(chats[chat_id].get_code(index))
