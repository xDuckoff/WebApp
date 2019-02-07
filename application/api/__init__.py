# -*- coding: utf-8 -*-

"""Endpoints для api запросов"""

from flask import Blueprint, jsonify, request, abort
from application import csrf
from application.models import Chat, User, Feedback


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/chat', methods=['GET'])
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


@api.route('/user', methods=['GET', 'PUT'])
@csrf.exempt
def api_user():
    """Получение и сохранение данных пользователя

    :return: параметры пользователя/статус операции сохранения
    """
    if request.method == 'GET':
        user = dict(name=User.get_login())
        return jsonify(user)
    elif request.method == 'PUT':
        data = request.get_json()
        name = data.get('name')
        if name is None:
            abort(400, '"name" parameter is required')
        User.login(name)
        return jsonify(dict(success=True))

import exception
