# -*- coding: utf-8 -*-

"""Тесты методов модели сообщений из обратной связи"""

from base_test_model import *
from application import db
from application.models import Feedback
from mock import patch

FEEDBACK_NAME = "test bot"
FEEDBACK_EMAIL = "test@test.com"
FEEDBACK_TEXT = "Lorem Ipsum"
TRELLO_CARD_URL = "http://trello/card/id"


class TestFeedbackModel(BaseTestModel):

    def test_available_code(self):
        feedback_params = {
            "name": FEEDBACK_NAME,
            "email": FEEDBACK_EMAIL,
            "text": FEEDBACK_TEXT
        }
        feedback = Feedback(**feedback_params)
        self.assertTrue(hasattr(feedback, "id"))
        self.assertTrue(hasattr(feedback, "name"))
        self.assertTrue(hasattr(feedback, "email"))
        self.assertTrue(hasattr(feedback, "text"))
        self.assertTrue(hasattr(feedback, "trello_link"))

    def test_type_model_feedback(self):
        self.assertIsInstance(Feedback.id.type, db.Integer)
        self.assertIsInstance(Feedback.name.type, db.String)
        self.assertIsInstance(Feedback.email.type, db.String)
        self.assertIsInstance(Feedback.text.type, db.Text)
        self.assertIsInstance(Feedback.trello_link.type, db.String)

    @patch.object(Feedback, 'send_to_trello', return_value=None)
    def test_feedback_sending(self, *args):
        send_feedback = Feedback.send(FEEDBACK_NAME, FEEDBACK_EMAIL, FEEDBACK_TEXT)
        feedback_in_db = Feedback.query.get(send_feedback.id)
        self.assertEquals(feedback_in_db.name, FEEDBACK_NAME)
        self.assertEquals(feedback_in_db.email, FEEDBACK_EMAIL)
        self.assertEquals(feedback_in_db.text, FEEDBACK_TEXT)

    @patch.object(Feedback, 'send_to_trello', return_value=TRELLO_CARD_URL)
    def test_trello_card_url_after_send_feedback(self, mock_send_to_trello_method):
        send_feedback = Feedback.send(FEEDBACK_NAME, FEEDBACK_EMAIL, FEEDBACK_TEXT)
        feedback_in_db = Feedback.query.get(send_feedback.id)
        self.assertTrue(mock_send_to_trello_method.called)
        self.assertEquals(feedback_in_db.trello_link, TRELLO_CARD_URL)
