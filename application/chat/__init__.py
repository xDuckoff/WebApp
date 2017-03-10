from flask import session
from application.models import Message, Code, Chat
from application import db


def create_chat(name):
    db.session.add(Chat(name))
    db.session.commit()

def send_message(id, text):
    db.session.add(Message(text, session['login']), id)
    db.session.commit()

def get_messages(id, index):
    return map(lambda x: {"author": x.author, "message": x.content}, Message.query.filter_by(chat=id))[index:]

def send_code(id, text):
    db.session.add(Code(text, session['login'], id))
    db.session.commit()

def get_code(id, index):
    return (lambda x: {"author": x.author, "code": x.content})(Code.query.filter_by(chat=id)[index])

def find_chat(name):
    try:
        return Chat.query.filter_by(name=name).limit(1)[0].id
    except IndexError:
        return -1
