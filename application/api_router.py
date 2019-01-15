# -*- coding: utf-8 -*-

"""Endpoints для api запросов"""

from flask import jsonify, request
from werkzeug.exceptions import HTTPException, BadRequest, InternalServerError
from application import app, csrf
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
@csrf.exempt
def api_user():
    """Получение и сохранение данных пользователя

    :return: параметры пользователя/статус операции сохранения
    """
    if request.method == 'GET':
        user = dict(name=User.get_login())
        return jsonify(user)
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            name = data.get('name')
            if name is None:
                raise BadRequest('"name" parameter is required')
            User.login(name)
            return jsonify(dict(success=True))
        except HTTPException as e:
            response = jsonify(dict(
                message=e.get_description()
            ))
            response.status_code = e.code
            return response
