from flask import session
from message import Message
class Chat:
    def __init__(self):
        self.messages = []
        self.mods = []
        
    def send_message(self, text):
        self.messages.append( Message(len(self.messages), text, session['login']) )

    def get_messages(self, index):
    	if index >= len(self.messages):
    		return []
    	res = []
    	for msg in self.messages[index:]:
    		res.append({'author': msg.author, 'message': msg.text})
    	return res


def make_session(login):
    session['login'] = login
    session['last'] = -1