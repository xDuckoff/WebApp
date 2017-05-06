from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

if app.config['SOCKET_MODE'] == 'True':
	from flask_socketio import SocketIO
	socketio = SocketIO(app)

import router
