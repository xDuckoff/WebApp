from flask import session
from application.models import Message, Code, Chat_Model
from application import db


class Chat:
    ids = 0

    def __init__(self, name):
        self.id = Chat.ids
        self.name = name
        Chat.ids += 1
        db.session.add(Chat_Model(self.id, self.name))
        db.session.commit()

    def send_message(self, text):
        db.session.add(Message(text, session['login'], self.id))
        db.session.commit()

    def get_messages(self, index):
        return map(lambda x: {"author": x.author, "message": x.content}, Message.query.filter_by(chat=self.id))[index:]

    def send_code(self, text):
        db.session.add(Code(text, session['login'], self.id))
        db.session.commit()

    def get_code(self, index):
        return (lambda x: {"author": x.author, "code": x.content})(Code.query.filter_by(chat=self.id)[index])
