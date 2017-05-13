import unittest
import os
import flask_migrate
from application import app
from application.models import Message, Code, Chat
from application import db

TEST_DB = 'test'
PATH_TO_DATABASE = os.path.join(os.path.abspath(os.path.curdir), TEST_DB + ".slite")


class Testmodels(unittest.TestCase):

    def setUp(self):
        global CHAT_ID
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + PATH_TO_DATABASE
        with app.app_context():
            flask_migrate.upgrade()




    def tearDown(self):
        os.remove(PATH_TO_DATABASE)

    def test_available_chat(self):
        chat = Chat("some")
        self.assertTrue(hasattr(chat, "id"))
        self.assertTrue(hasattr(chat, "name"))

    def test_available_message(self):
        message = Message("content", "author", 1, "sys")
        self.assertTrue(hasattr(message, "id"))
        self.assertTrue(hasattr(message, "content"))
        self.assertTrue(hasattr(message, "author"))
        self.assertTrue(hasattr(message, "chat"))
        self.assertTrue(hasattr(message, "type"))

    def test_available_code(self):
        code = Code("content", "author", 1, 0)
        self.assertTrue(hasattr(code, "id"))
        self.assertTrue(hasattr(code, "content"))
        self.assertTrue(hasattr(code, "author"))
        self.assertTrue(hasattr(code, "chat"))
        self.assertTrue(hasattr(code, "parent"))

    def test_type_model_chat(self):

        self.assertIsInstance(Chat.id.type, db.Integer)
        self.assertIsInstance(Chat.name.type, db.String)


    def test_type_model_message(self):

        self.assertIsInstance(Message.id.type, db.Integer)
        self.assertIsInstance(Message.content.type, db.Text)
        self.assertIsInstance(Message.author.type, db.String)
        self.assertIsInstance(Message.chat.type, db.Integer)
        self.assertIsInstance(Message.type.type, db.String)


    def test_type_model_code(self):

        self.assertIsInstance(Code.id.type, db.Integer)
        self.assertIsInstance(Code.content.type, db.Text)
        self.assertIsInstance(Code.author.type, db.String)
        self.assertIsInstance(Code.chat.type, db.Integer)
        self.assertIsInstance(Code.parent.type, db.Integer)