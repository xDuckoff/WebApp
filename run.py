# -*- coding: utf-8 -*-

"""Запуск проекта"""

from application import app

import flask_migrate

with app.app_context():    
	flask_migrate.upgrade()

	import os

	go_to_dir = 'cd docs/'
	make_html = 'make html'
	go_up = 'cd ..'
	os.system(go_to_dir + '\n' + make_html + '\n' + go_up + '\n')
