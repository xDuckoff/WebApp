# -*- coding: utf-8 -*-

"""Основные веб-страницы проекта"""

import os
import application.chat_router
from application import app, recaptcha
from application.forms import CreateChatForm, FeedbackForm, FindChatForm, LoginForm
from application.models import Chat, User, Feedback, flask_recaptcha
from config import RECAPTCHA_SITE_KEY
from flask import render_template, redirect, send_from_directory, request


@app.route('/logout')
def logout():
    """Функция выхода из сессии в проекте

    :return: Переход на главную страницу
    """
    User.logout()
    return redirect('/')

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

    return render_template('feedback.html',
                           feedback_form=feedback_form,
                           RECAPTCHA_SITE_KEY=RECAPTCHA_SITE_KEY)

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
        if chat_create_form.is_file_valid():
            code = chat_create_form.file.data.read()
        chat_id = Chat.create(name, code, code_type)
        return redirect('/chat/' + str(chat_id))
    return render_template('index.html',
                           chats=Chat.find(find_chat_form.chat_title.data),
                           in_session=User.is_logined(),
                           login_form=login_form,
                           chat_create_form=chat_create_form,
                           find_chat_form=find_chat_form,
                           login=User.get_login(),
                           allowed_ex=",".join(['.' + i for i in app.config["ALLOWED_EXTENSIONS"]]),
                           allowed_languages=app.config["ALLOWED_LANGUAGES"]
                          )


@app.route('/documentation/<path:filename>')
def docs_page(filename):
    """Данная функция открывает пользователю страницу с документацией

    :param filename: Имя файла
    :return: Выбранный файл с документацией
    """
    rootdir = os.getcwd()
    path = rootdir + '/docs/_build/html/'
    return send_from_directory(path, filename)
