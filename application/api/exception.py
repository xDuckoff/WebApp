# -*- coding: utf-8 -*-

"""Обработки исключений/ошибок в запросах"""

from flask import jsonify
from werkzeug.exceptions import BadRequest
from application.api import api


@api.errorhandler(BadRequest)
def handle_errors(error):
    """Обработка ошибок в запросах и возврат информации об ошибке в json формате"""
    response = jsonify(dict(
        code=error.code,
        success=False,
        description=error.description
    ))
    response.status_code = error.code
    return response
