from flask import session
from application.models import Message, Code, Chat
from application import db


def create_chat(name):
    chat_to_create = Chat(name)
    db.session.add(chat_to_create)
    db.session.commit()
    return chat_to_create.id

def get_chat_info(id):
    result = Chat.query.get(id)
    return {'name':result.name}

def send_message(id, text, type):
    db.session.add(Message(text, session['login'], id, type))
    db.session.commit()

def get_messages(id, index):
    result = Message.query.filter_by(chat=id)[index:]
    ret = []
    for i in result:

    	if i.type == "usr":
    		if i.author == session['login']:
    			type = "mine"
    		else:
    			type = "others"
    	else:
    		type = "system"

        ret.append({"author": i.author, "message": i.content, "type": type})
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
