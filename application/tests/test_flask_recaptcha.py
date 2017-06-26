from base_test_model import *
from application import app
from flask import Flask
from flask_recaptcha import ReCaptcha

app.config.update({
    "debug": True,
    "RECAPTCHA_SITE_KEY": "SITE_KEY",
    "RECAPTCHA_SITE_SECRET": "SECRET",
    "RECAPTCHA_ENABLED": True
})

class TestReCaptchaForm(BaseTestModel):

    def test_recaptcha_enabled(self):
        recaptcha = ReCaptcha(site_key="SITE_KEY", secret_key="SECRET_KEY")
        self.assertIsInstance(recaptcha, ReCaptcha)
        self.assertTrue(recaptcha.is_enabled)
        self.assertIn("script", recaptcha.get_code())
        self.assertFalse(recaptcha.verify(response="None", remote_ip="0.0.0.0"))

    def test_recaptcha_enabled_flask(self):
        app.config.update({
            "RECAPTCHA_ENABLED": True
        })
        recaptcha = ReCaptcha(app=app)
        self.assertIsInstance(recaptcha, ReCaptcha)
        self.assertTrue(recaptcha.is_enabled)
        self.assertIn("script", recaptcha.get_code())
        self.assertFalse(recaptcha.verify(response="None", remote_ip="0.0.0.0"))

    def test_recaptcha_disabled(self):
        recaptcha = ReCaptcha(site_key="SITE_KEY", secret_key="SECRET_KEY", is_enabled=False)
        self.assertFalse(recaptcha.is_enabled)
        self.assertEqual(recaptcha.get_code(), "")
        self.assertTrue(recaptcha.verify(response="None", remote_ip="0.0.0.0"))

    def test_recaptcha_disabled_flask(self):
        app.config.update({
            "RECAPTCHA_ENABLED": False
        })
        recaptcha = ReCaptcha(app=app)
        self.assertFalse(recaptcha.is_enabled)
        self.assertEqual(recaptcha.get_code(), "")
        self.assertTrue(recaptcha.verify(response="None", remote_ip="0.0.0.0"))
