# -*- coding: utf-8 -*-

from application import db


class Chat(db.Model):
    """Модель чата"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    code_type = db.Column(db.String(256))

    def __init__(self, name, code_type):
        """Конструктор чата"""
        self.name = name
        self.code_type = code_type
