from flask import render_template, redirect, request, session
from application import app
from json import dumps 
from application import chat
from application.forms import IsInSession, CreateChatForm, allowed_file

@app.route('/tree', methods=['GET', 'POST'])
def tree():
    chat_id = int(request.args['chat'])
    coms = chat.generate_commits_tree(chat_id)
    return render_template('commitsTree.html',commits = coms)

@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def chat_page(chat_id):
    if not(IsInSession()):
        return redirect('/login?chat=' + str(chat_id))
    return render_template('chat.html',chat_id=chat_id, socket_mode=(app.config['SOCKET_MODE'] == 'True'))

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
    parent = request.args['parent']
    code_id = chat.send_code(chat_id, code, session['login'], parent)
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

@app.route('/get_commits', methods=['GET', 'POST'])
def get_chat_commits():
    chat_id = int(request.args['chat'])
    return dumps(chat.generate_tree(chat_id))
