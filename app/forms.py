from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask import render_template, redirect, request, session, url_for, escape, request, Flask
from flask import Flask, session
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware

session_opts = {
    #'session.type': 'ext:memcached',
    'session.url': '127.0.0.1:11211',
    'session.data_dir': './cache',
}

class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])

class BeakerSessionInterface(SessionInterface):
    def open_session(self, app, request):
        session = request.environ['beaker.session']
        return session

    def save_session(self, app, session, response):
        session.save()
