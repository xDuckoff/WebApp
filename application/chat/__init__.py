from flask import session
from application.models import Message, Code, Chat
from application import db


def create_chat(name):
    db.session.add(Chat(name))
    db.session.commit()

def send_message(id, text):
    db.session.add(Message(text, session['login'], id))
    db.session.commit()

def get_messages(id, index):
    result = Message.query.filter_by(chat=id)[index:]
    ret = []
    for i in result:
        ret.append({"author": i.author, "message": i.content})
    return ret

def send_code(id, text):
    db.session.add(Code(text, session['login'], id))
    db.session.commit()

def get_code(id, index):
    result = Code.query.filter_by(chat=id)[index]
    return {"author": result.author, "code": result.content}

def find_chat(name):
    try:
        return Chat.query.filter_by(name=name).limit(1)[0].id
    except IndexError:
        return -1
