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
