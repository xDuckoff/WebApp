from flask import session
from message import Message
class Chat:
    def __init__(self):
        self.messages = []
        self.mods = []
        self.user_sessions = []

    def Send_message(self, text):
        self.messages.append( Message(len(self.messages), text, session['login']) )