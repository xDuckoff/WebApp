# -*- coding: utf-8 -*-

"""Функции работы с данными обратной связи"""

from application import db


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

    def __init__(self, name, email, text):
        self.name = name
        self.email = email
        self.text = text

    @staticmethod
    def send(name, email, text):
        """Отправляет данные в базу для сохранения

        :param name: имя пользователя
        :param email: почта пользователя
        :param text: вопрос пользователя
        :return: Объект созданных данных
        """
        feedback = Feedback(name, email, text)
        db.session.add(feedback)
        db.session.commit()
        return feedback
