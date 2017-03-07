# -*- coding: utf-8 -*-

from flask import render_template, redirect, session, url_for, request
from app import app
from forms import LoginForm, make_session


def IsInSession():
    if login in session:
        return True
    return False


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    numberofchat = request.args.get('chat','')
    link = (numberofchat == '')* '/' + (not numberofchat == '') * ('chat/'+numberofchat)
    if form.validate_on_submit():
        make_session(form.login.data)
        return redirect(link)
    if IsInSession():
        return redirect(link)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if not(IsInSession()): return redirect('/login')
    session.pop('login', None)
    return redirect(url_for('index'))    


@app.route('/')
def index():
    return render_template('index.html')

import app.chat.route
