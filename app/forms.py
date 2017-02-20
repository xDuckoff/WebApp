from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
