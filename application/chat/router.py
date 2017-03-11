from flask import render_template, redirect, request
from application import app
from json import dumps
from application import chat
from application.forms import IsInSession


@app.route('/chat/<chat_id>', methods=['GET', 'POST'])
def chat_page(chat_id):
    if not(IsInSession()):
        return redirect('/login?chat=' + str(chat_id))
    chat_id = int(chat_id)
    return render_template('chat.html')


@app.route('/create_chat', methods=['GET', 'POST'])
def create_chat():
    if not(IsInSession()):
        return redirect('/login')

    name = request.args['name']
    code = request.args['code']
    chat_id = chat.create_chat(name)
    chat.send_code(chat_id, code)
    
    return redirect('/chat/' + str(chat_id))


@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    message = request.args['message']
    if len(message) > 0:
        chat.send_message(chat_id, message)
    return 'OK'


@app.route('/get_messages', methods=['GET', 'POST'])
def get_messages():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    index = int(request.args['index'])
    return dumps(chat.get_messages(chat_id, index))


@app.route('/send_code', methods=['GET', 'POST'])
def send_code():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    code = request.args['code']
    if len(code) > 0:
        chat.send_code(chat_id, code)
    return 'OK'


@app.route('/get_code', methods=['GET', 'POST'])
def get_code():
    if not(IsInSession()):
        return redirect('/login')
    chat_id = int(request.args['chat'])
    index = int(request.args['index'])
    return dumps(chat.get_code(chat_id, index))
