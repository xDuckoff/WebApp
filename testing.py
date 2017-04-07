import unittest
from application import chat, forms


username = 'Bot'
chat_name = 'Test Chat'
chat_code = 'Test Code'
test_message = 'Hello, I am Bot!'
test_code = 'from test import test'
chat_id = 0

class TestBaseChatFunctions(unittest.TestCase):

	def test_chat_creating(self):
		chat_id = chat.create_chat(chat_name, chat_code, username)
		self.assertEquals(chat.get_chat_info(chat_id), {'name': chat_name})
		self.assertEquals(chat.get_code(chat_id, 0), {'author': username, 'code': chat_code})

	def test_message_sending(self):
		chat.send_message(chat_id, test_message, 'usr', username)
		self.assertEquals(chat.get_messages(chat_id, username)[-1], {'message': test_message, 'type': 'mine', 'author': username})

	def test_code_sending(self):
		chat.send_code(chat_id, test_code, username)
		self.assertEquals(chat.get_code(chat_id, 1), {"author": username, "code": test_code})


unittest.main()
