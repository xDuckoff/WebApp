# -*- coding: utf-8 -*-

from flask import render_template
from app import app
from forms import LoginForm


@app.route('/')
def index():
    return render_template('index.html', title=u'Главная')


@app.route('/login', methods=['GET', 'POST'])
def login():
    LForm = LoginForm()
    return render_template('login.html', title=u'Вход', form=LForm)


@app.route('/my', methods=['GET', 'POST'])
def my():
    LForm = LoginForm()
    return render_template('my.html', title=u'Личный кабинет', form=LForm)
