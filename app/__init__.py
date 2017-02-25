from flask import Flask
from chat import Chat

app = Flask(__name__)
app.config.from_object('config')

chats = [Chat()]

from app import views

