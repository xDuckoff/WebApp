# -*- coding: utf-8 -*-

"""Запуск проекта"""

import flask_migrate
from application import app

with app.app_context():
    flask_migrate.upgrade()
