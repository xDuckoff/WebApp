# -*- coding: utf-8 -*-

"""Endpoints для api запросов"""

from flask import redirect, jsonify
from application import app
from application.models import Chat, User, Feedback


@app.route('/api/chat', methods=['GET'])
def api_chat_list():
    """Получение списка созданных чатов

    :return: список созданных чатов
    """
    chats = Chat.query.all()
    data = [chat.to_dict() for chat in chats]
    return jsonify(data)
