# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
"""
Данный файл содержит основные положения запуска приложения
"""
app = Flask(__name__)
app.config.from_object('config', )
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import router
