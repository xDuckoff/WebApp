# -*- coding: utf-8 -*-

"""Функции работы с реКапчей"""

from application import db
from flask import request
from jinja2 import Markup
import requests


class ReCaptcha(object):
    """Модель Капчи

    :param:
    """

    VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
    site_key = None
    secret_key = None
    is_enabled = False

    def get_code(self):
        """Возвращает новый код ReCaptcha

        :return:
        """
        return "" if not self.is_enabled else ("""
        <script src='//www.google.com/recaptcha/api.js'></script>
        <div class="g-recaptcha" data-sitekey="{SITE_KEY}" data-theme="{THEME}" data-type="{TYPE}" data-size="{SIZE}"\
         data-tabindex="{TABINDEX}"></div>
        """.format(SITE_KEY=self.site_key,
                   THEME=self.theme,
                   TYPE=self.type,
                   SIZE=self.size,
                   TABINDEX=self.tabindex))

    def verify(self, response=None, remote_ip=None):
        """Проверка данных

        :return: bool
        """
        if self.is_enabled:
            data = {
                "secret": self.secret_key,
                "response": response or request.form.get('g-recaptcha-response'),
                "remoteip": remote_ip or request.environ.get('REMOTE_ADDR')
            }

            r = requests.get(self.VERIFY_URL, params=data)
            return r.json()["success"] if r.status_code == 200 else False
        return True
