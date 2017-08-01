# -*- coding: utf-8 -*-

"""Тесты Markdown"""

import unittest
from application.models import MarkdownMixin

BASE_TEXT = '<strong>Hello</strong>, I am **Bot**!'
TEXT_WITHOUT_HTML = '&lt;strong&gt;Hello&lt;/strong&gt;, I am **Bot**!'
TEXT_MARKDOWN_DECODED = '<p>&lt;strong&gt;Hello&lt;/strong&gt;, I am <strong>Bot</strong>!</p>'


class TestMarkdownMixin(unittest.TestCase):

    def test_text_escape_html(self):
        self.assertEqual(MarkdownMixin.escape_html(BASE_TEXT), TEXT_WITHOUT_HTML)

    def test_text_markdown(self):
        self.assertEqual(MarkdownMixin.decode(BASE_TEXT), TEXT_MARKDOWN_DECODED)
