# -*- coding: utf-8 -*-

"""Основные положения запуска приложения"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO
from flask_recaptcha import ReCaptcha

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect()
csrf.init_app(app)
socketio = SocketIO(app)
recaptcha = ReCaptcha(app=app)

import router
