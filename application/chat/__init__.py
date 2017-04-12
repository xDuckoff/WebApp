from flask import session
from application.models import Message, Code, Chat
from application import db, socketio
from flask_socketio import emit


def create_chat(name, code, username):
    chat_to_create = Chat(name)
    db.session.add(chat_to_create)
    db.session.commit()
    chat_id = chat_to_create.id
    send_code(chat_id, code, username)
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

def send_code(id, text, username):
    CodeToSend = Code(text, username, id)
    db.session.add(CodeToSend)
    db.session.commit()
    code_id = CodeToSend.id
    sys_message("New Commit " + str(code_id), str(id))
    return code_id

def get_code(id, index):
    result = Code.query.filter_by(chat=id)[index]
    return {"author": result.author, "code": result.content}

def find_chat(name):
    try:
        return Chat.query.filter(Chat.name.like('%'+name+'%')).all()
    except IndexError:
        return -1

def sys_message(data, room):
    send_message(int(room), data, 'sys', 'System')
    socketio.emit('message', {'message':data, 'author':'System', 'type':'sys'}, room=room, broadcast=True)
