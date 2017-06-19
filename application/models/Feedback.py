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
    text = db.Column(db.String(256))

    def __init__(self, name, email, text):
        self.name = name
        self.email = email
        self.text = text

    @staticmethod
    def create(name, email, text):
        """Создаёт массив данных ввиде словаря

        :param feedback: данные
        :return: массив данных
        """
        feedback = {'Имя пользователя': name,
                    'Почта пользователя': email,
                    'Вопрос пользователя': text}

        return feedback

    @staticmethod
    def send(name, email, text):
        """Отправляет данные в базу для сохранения

        :param name: имя пользователя
        :param email: почта пользователя
        :param text: вопрос пользователя
        :return: Объект созданных данных
        """
        #if len(text) > 1000 or not text:
        #    raise OverflowError
        feedback = Feedback(name, email, text)
        db.session.add(feedback)
        db.session.commit()
#        if app.config['SOCKET_MODE'] == 'True':
#            socketio.emit('feedback', feedback.get_info(), room='feedback', broadcast=True)
