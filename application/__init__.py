# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from flask_wtf.csrf import CSRFProtect

"""
Данный файл содержит основные положения запуска приложения
"""

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
with app.app_context():
    upgrade()
csrf = CSRFProtect()
csrf.init_app(app)
socketio = None
if app.config['SOCKET_MODE'] == 'True':
    from flask_socketio import SocketIO
    socketio = SocketIO(app)

import router
