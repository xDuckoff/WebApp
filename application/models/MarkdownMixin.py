# -*- coding: utf-8 -*-

"""Функции для обоработки строк, пришедших со стороны клиента
"""

import cgi
from markdown import markdown
from jinja2 import Template


class MarkdownMixin(object):
    """Класс-примесь для обработки строк: экранирование и преобразования синтаксиса Markdown
    """

    @staticmethod
    def escape_html(text):
        """Экранирование текста

        :param text: Исходный текст
        :return: Экранированный текст
        """
        text = text.replace('```', '`')
        parts = text.split('`')
        for i in range(0, len(parts), 2):
            parts[i] = cgi.escape(parts[i])
        return '`'.join(parts)

    @classmethod
    def decode(cls, text):
        """Преобразование текста в HTML в соответствии с синтаксисом Markdown

        :param text: исходный текст
        :return: преобразовнный в HTML текст
        """
        if text is None:
            text = ""
        text = cls.escape_html(text)
        text = markdown(text)
        return text

    @staticmethod
    def plain(text):
        template = Template('{{ text | striptags }}')
        return template.render(text=text)
