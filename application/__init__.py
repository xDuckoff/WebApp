# -*- coding: utf-8 -*-

"""Основные положения запуска приложения"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect()
csrf.init_app(app)
socketio = SocketIO(app)

import router

import flask_migrate

with app.app_context():    
	flask_migrate.upgrade()

	import os

	go_to_dir = 'cd docs/'
	make_html = 'make html'
	go_up = 'cd ..'
	os.system(go_to_dir + '\n' + make_html + '\n' + go_up + '\n')