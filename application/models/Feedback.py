# -*- coding: utf-8 -*-

"""Функции работы с данными обратной связи"""

import json
import requests
from application import app, db


class Feedback(db.Model):
    """Модель данных в форме обратной связи

    :param name: имя пользователя
    :param email: почта пользователя
    :param text: вопрос пользователя
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(256))
    text = db.Column(db.Text)
    trello_link = db.Column(db.Text)

    def __init__(self, name, email, text):
        self.name = name
        self.email = email
        self.text = text

    def send_to_trello(self):
        """Отправка сообщения в trello через API

        :return: ссылка на созданную карточку
        """
        API_URL = "https://api.trello.com/1/cards"
        querystring = {
            "name": self.text,
            "desc": self.__get_trello_description(),
            "idList": app.config["TRELLO_LIST_ID"],
            "key": app.config["TRELLO_API_KEY"],
            "token": app.config["TRELLO_API_TOKEN"]
        }
        response = requests.request("POST", API_URL, params=querystring)
        card = json.loads(response.text)
        return card.get('url')

    def __get_trello_description(self):
        """Получение текста внутреннего содержания карточки

        :return: содержание карточки
        """
        template = u"От: {name} <{email}>\n{text}"
        return template.format(
            name=self.name,
            email=self.email,
            text=self.text
        )

    @staticmethod
    def send(name, email, text):
        """Отправляет данные в базу для сохранения

        :param name: имя пользователя
        :param email: почта пользователя
        :param text: вопрос пользователя
        :return: Объект созданных данных
        """
        feedback = Feedback(name, email, text)
        feedback.trello_link = feedback.send_to_trello()
        db.session.add(feedback)
        db.session.commit()
        return feedback
