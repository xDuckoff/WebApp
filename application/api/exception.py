# -*- coding: utf-8 -*-

"""Обработки исключений/ошибок в запросах"""

from flask import jsonify, abort
from werkzeug.exceptions import BadRequest
from application.api import api


@api.errorhandler(BadRequest)
@api.errorhandler(404)
def handle_errors(error):
    """Обработка ошибок в запросах и возврат информации об ошибке в json формате"""
    response = jsonify(dict(
        code=error.code,
        success=False,
        description=error.description
    ))
    response.status_code = error.code
    return response

@api.route('/<path:invalid_path>')
def handler_invalid_path(invalid_path):
    """(hook) Вызов ошибки 404 в рамках blueprint"""
    abort(404, 'URL /api/' + invalid_path + ' not found')
