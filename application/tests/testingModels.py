import unittest
import os
import flask_migrate
from application import chat
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

    

    def test_type_model_chat(self):
        chat =Chat("some")
        self.assertIsInstance(Chat.id.type, db.Integer)
        self.assertIsInstance(Chat.name.type, db.String)


    def test_type_model_message(self):
        message = Message("content", "author", 1, "sys")
        self.assertIsInstance(Message.id.type, db.Integer)
        self.assertIsInstance(Message.content.type, db.Text)
        self.assertIsInstance(Message.author.type, db.String)
        self.assertIsInstance(Message.chat.type, db.Integer)
        self.assertIsInstance(Message.type.type, db.String)


    def test_type_model_code(self):
        code = Code("content", "author", 1, 0)
        self.assertIsInstance(Code.id.type, db.Integer)
        self.assertIsInstance(Code.content.type, db.Text)
        self.assertIsInstance(Code.author.type, db.String)
        self.assertIsInstance(Code.chat.type, db.Integer)
        self.assertIsInstance(Code.parent.type, db.Integer)