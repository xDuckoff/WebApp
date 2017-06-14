# -*- coding: utf-8 -*-

"""Запуск проекта"""

import os
import flask_migrate
from application import app

with app.app_context():
    flask_migrate.upgrade()

    go_to_dir = 'cd docs/'
    make_html = 'make html'
    go_up = 'cd ..'

    os.system(go_to_dir + '\n' + make_html + '\n' + go_up + '\n')
