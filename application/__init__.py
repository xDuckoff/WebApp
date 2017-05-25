# -*- coding: utf-8 -*-
"""
Данный файл содержит основные положения запуска приложения
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CSRFProtect(app)

import router
