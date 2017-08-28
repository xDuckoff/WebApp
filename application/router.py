# -*- coding: utf-8 -*-

"""Основные веб-страницы проекта"""

from flask import render_template, redirect, flash
from application import app
from application.forms import CreateChatForm, FeedbackForm, FindChatForm, LoginForm
from application.models import Chat, User, Feedback
from application.handlers import form_required


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
    return render_template('index.html',
                           chats=Chat.find(find_chat_form.chat_title.data),
                           login_form=login_form,
                           chat_create_form=chat_create_form,
                           find_chat_form=find_chat_form,
                           login=User.get_login()
                          )


@app.route('/create_chat', methods=['POST'])
@form_required(CreateChatForm)
def create_chat():
    """Создание чата

    :return: Перенаправление на страницу чата
    """
    chat_create_form = CreateChatForm()
    name = chat_create_form.name.data
    access_key = chat_create_form.access_key.data
    chat_id = Chat.create(name, access_key)
    return redirect('/chat/' + str(chat_id))


@app.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    """Функция переходан на страницу обратной связи

    :return: Переход на страницу обратной связи
    """
    feedback_form = FeedbackForm()
    chat_create_form = CreateChatForm()
    login_form = LoginForm()
    if feedback_form.validate_on_submit():
        name = feedback_form.name.data
        email = feedback_form.email.data
        text = feedback_form.text.data
        Feedback.send(name, email, text)
        flash(u'Сообщение успешно отправлено', 'feedback')
        return redirect('/feedback')
    return render_template('feedback.html',
                           feedback_form=feedback_form,
                           login_form=login_form,
                           login=User.get_login(),
                           chat_create_form=chat_create_form,
                           allowed_ex=",".join(['.' + i for i in app.config["ALLOWED_EXTENSIONS"]]),
                           allowed_languages=app.config["ALLOWED_LANGUAGES"]
                          )

import application.chat_router
