# -*- coding: utf-8 -*-

"""Тесты методов модели сообщений из обратной связи"""

from base_test_model import *
from application import db
from application.models import Feedback

FEEDBACK_NAME = "test bot"
FEEDBACK_EMAIL = "test@test.com"
FEEDBACK_TEXT = "Lorem Ipsum"


class TestFeedbackModel(BaseTestModel):

    def setUp(self):
        BaseTestModel.setUp(self)
        # self.feedback_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)

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

    def test_type_model_feedback(self):
        self.assertIsInstance(Feedback.id.type, db.Integer)
        self.assertIsInstance(Feedback.name.type, db.String)
        self.assertIsInstance(Feedback.email.type, db.String)
        self.assertIsInstance(Feedback.text.type, db.Text)

    def test_feedback_sending(self):
        send_feedback = Feedback.send(FEEDBACK_NAME, FEEDBACK_EMAIL, FEEDBACK_TEXT)
        feedback_in_db = Feedback.query.get(send_feedback.id)
        self.assertEquals(feedback_in_db.name, FEEDBACK_NAME)
        self.assertEquals(feedback_in_db.email, FEEDBACK_EMAIL)
        self.assertEquals(feedback_in_db.text, FEEDBACK_TEXT)
