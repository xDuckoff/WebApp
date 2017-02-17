from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    nick = StringField('nick', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
