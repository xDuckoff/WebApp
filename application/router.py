# -*- coding: utf-8 -*-

"""Основные веб-страницы проекта"""

from application import app, recaptcha
from application.forms import CreateChatForm, FeedbackForm, FindChatForm, LoginForm
from application.models import Chat, User, Feedback, flask_recaptcha
from config import RECAPTCHA_SITE_KEY
from flask import render_template, redirect

@app.route("/send_feedbacks", methods=["POST"])
def send_feedbacks():
    """Функция проверки капчи

    :return: Переход на страницу обратной связи вслучае не заполнения капчи \
    и переход на главную страницу при правильном заполнении
    """
    feedback_form = FeedbackForm()
    name = feedback_form.name.data
    email = feedback_form.email.data
    text = feedback_form.text.data

    if recaptcha.verify():
        Feedback.send(name, email, text)
        return redirect('/')
    return redirect('/feedback')

@app.route('/feedback')
def feedback_page():
    """Функция переходан на страницу обратной связи

    :return: Переход на страницу обратной связи
    """
    feedback_form = FeedbackForm()
    chat_create_form = CreateChatForm()
    login_form = LoginForm()
    return render_template('feedback.html',
                           feedback_form=feedback_form,
                           RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY,
                           login_form=login_form,
                           login=User.get_login(),
                           chat_create_form=chat_create_form,
                           allowed_ex=",".join(['.' + i for i in app.config["ALLOWED_EXTENSIONS"]]),
                           allowed_languages=app.config["ALLOWED_LANGUAGES"]
                          )

@app.route('/', methods=['GET', 'POST'])
def index():
    """Данная функция генерирует главную страницу для пользователя

    :return: Главная страница с чатами пользователя, является ли человек \
    в сессии, формой входа(Если человек не зарегистрирован, заголовок чата
    """
    find_chat_form = FindChatForm()
    chat_create_form = CreateChatForm()
    login_form = LoginForm()
    if login_form.validate_on_submit():
        User.login(login_form.login.data)
    if chat_create_form.validate_on_submit():
        name = chat_create_form.name.data
        code_type = chat_create_form.code_type.data
        code = chat_create_form.code.data
        access_key = chat_create_form.access_key.data
        if chat_create_form.is_file_valid():
            code = chat_create_form.file.data.read()
        chat_id = Chat.create(name, code, code_type, access_key)
        return redirect('/chat/' + str(chat_id))
    return render_template('index.html',
                           chats=Chat.find(find_chat_form.chat_title.data),
                           login_form=login_form,
                           chat_create_form=chat_create_form,
                           find_chat_form=find_chat_form,
                           login=User.get_login(),
                           allowed_ex=",".join(['.' + i for i in app.config["ALLOWED_EXTENSIONS"]]),
                           allowed_languages=app.config["ALLOWED_LANGUAGES"]
                          )

import application.chat_router
