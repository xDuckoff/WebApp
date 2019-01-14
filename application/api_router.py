# -*- coding: utf-8 -*-

"""Endpoints для api запросов"""

from flask import jsonify, request
from application import app
from application.models import Chat, User, Feedback


@app.route('/api/chat', methods=['GET'])
def api_chat_list():
    """Получение списка созданных чатов

    :return: список созданных чатов
    """
    search = request.args.get('search', '')
    limit = int(request.args.get('limit', 0))
    page = int(request.args.get('page', 1))
    chats = Chat.find(search, limit, page)
    data = [chat.to_dict() for chat in chats]
    return jsonify(data)


@app.route('/api/user', methods=['GET', 'PUT'])
def api_user():
    """Получение и сохранение данных пользователя

    :return: параметры пользователя/статус операции сохранения
    """
    if request.method == 'GET':
        user = dict(name=User.get_login())
        return jsonify(user)
    elif request.method == 'PUT':
        return jsonify(dict(message='Error'))
