# -*- coding: utf-8 -*-

from flask import render_template, redirect
from app import app
from forms import LoginForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/chat/1')
    return render_template('login.html', form=form)


@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def chat_page(chat_id):
    return 'Chat page ' + str(chat_id)
