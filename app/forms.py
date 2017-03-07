from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask.sessions import SessionInterface

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


def make_session(login):
    session['login'] = login
    session['last'] = -1
