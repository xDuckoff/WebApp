from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask import render_template, redirect, request, session, url_for, escape, request, Flask


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])