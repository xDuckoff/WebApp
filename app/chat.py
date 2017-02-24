from flask import session
from message import Message
class Chat:
    def __init__(self):
        self.messages = []
        self.mods = []
        
    def send_message(self, text):
        self.messages.append( Message(len(self.messages), text, session['login']) )


def make_session(self, login):
    session['login'] = login
    session['last'] = -1