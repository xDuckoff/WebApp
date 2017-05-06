from flask import session
from application.models import Message, Code, Chat
from application import db
from application import app
import cgi

if app.config['SOCKET_MODE'] == 'True':
    from application import socketio
    from flask_socketio import emit


def create_chat(name, code, username):
    name = cgi.escape(name)
    code = cgi.escape(code)
    chat_to_create = Chat(name)
    db.session.add(chat_to_create)
    db.session.commit()
    chat_id = chat_to_create.id
    send_code(chat_id, code, username, 0)
    return chat_id

def get_chat_info(id):
    result = Chat.query.get(id)
    return {'name':result.name}

def send_message(id, text, type, username):
    db.session.add(Message(text, username, id, type))
    db.session.commit()

def get_messages(id, username):
    result = Message.query.filter_by(chat=id)
    ret = []
    for i in result:

        if i.type == "usr":
            if i.author == username:
                type = "mine"
            else:
                type = "others"
        else:
            type = "system"

        ret.append({"author": i.author, "message": i.content, "type": type})
    return ret

def send_code(id, text, username, parent):
    text = cgi.escape(text)
    CodeToSend = Code(text, username, id, parent)
    db.session.add(CodeToSend)
    db.session.commit()
    code_id = CodeToSend.id
    sys_message("New Commit " + str(code_id), str(id))
    socketio.emit('commit', room=str(id), broadcast=True)
    return code_id

def get_code(id, index):
    result = Code.query.filter_by(chat=id)[index]
    return {"author": result.author, "code": result.content}

def find_chat(name):
    return Chat.query.filter(Chat.name.like('%'+name+'%')).all()

def sys_message(data, room):
    send_message(int(room), data, 'sys', 'System')
    if app.config['SOCKET_MODE'] == 'True':
        socketio.emit('message', {'message':data, 'author':'System', 'type':'sys'}, room=room, broadcast=True)

def get_commits_in_chat(chat):
    return Code.query.filter_by(chat=chat)

def generate_commits_tree(chat):
    commits = get_commits_in_chat(chat)
    commits_data = []
    for index in range(0, commits.count()):
        commit = commits[index]
        commits_data.append({"id":index, "author":str(commit.author), "parent":int(commit.parent)})
    return commits_data
