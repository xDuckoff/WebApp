from flask import Flask
from chat import Chat
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware
from forms import session_opts, BeakerSessionInterface

app = Flask(__name__)
app.config.from_object('config')
app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
app.session_interface = BeakerSessionInterface()

chats = [Chat()]

from app import views