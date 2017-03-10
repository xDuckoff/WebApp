from flask import render_template, redirect, request
from application import app
from json import dumps
from application import chat
from application.forms import IsInSession


@app.route('/chat/<chat_id>', methods=['GET', 'POST'])
def chat_page(chat_id):
    if not(IsInSession()):
        return redirect('/login?chat=' + str(chat_id))
    if chat_id.isdigit():
        chat_id = int(chat_id)
        return render_template('chat.html')
    else:
        chat_id = chat.find_chat(chat_id)
        if chat_id == -1:
            return 'Not Found', 404
        return render_template('chat.html')


@app.route('/create_chat', methods=['GET', 'POST'])
def create_chat(name="default"):
    if not(IsInSession()):
        return redirect('/login')
    chat.create_chat(name)
    return redirect('/chat/' + name)


@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    if len(request.args['message']) > 0:
        chat.send_message(chat, message)
    return 'OK'


@app.route('/get_messages', methods=['GET', 'POST'])
def get_messages():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    index = int(request.args['index'])
    return dumps(chat.get_messages(chat, index))


@app.route('/send_code', methods=['GET', 'POST'])
def send_code():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    if len(request.args['code']) > 0:
        chat.send_code(chat, message)
    return 'OK'


@app.route('/get_code', methods=['GET', 'POST'])
def get_code():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    index = int(request.args['index'])
    return dumps(chat.get_code(chat, index))
