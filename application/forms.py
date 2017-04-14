from wtforms import StringField, FileField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf import FlaskForm
from flask.sessions import SessionInterface
from flask import session
from application import app
from application.chat.__init__ import html_special_chars

session_opts = {
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


def login_user(login):
    session['login'] = html_special_chars(login)
    session['last'] = -1


def IsInSession():
    if 'login' in session:
        return True
    return False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

class CreateChatForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    code_type = StringField('codetype', validators=[DataRequired()])
    file = FileField('file')
    code = StringField('code')