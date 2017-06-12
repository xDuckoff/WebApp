# -*- coding: utf-8 -*-

"""Тесты методов кода"""

from base_test_model import *
from application import db
from application.models import Chat, Code


class TestCodeModel(BaseTestModel):

    def setUp(self):
        BaseTestModel.setUp(self)
        self.chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, USERNAME)

    def test_available_code(self):
        code = Code("content", "author", 1, None, COMMIT_MESSAGE)
        self.assertTrue(hasattr(code, "id"))
        self.assertTrue(hasattr(code, "content"))
        self.assertTrue(hasattr(code, "author"))
        self.assertTrue(hasattr(code, "message"))
        self.assertTrue(hasattr(code, "chat_link"))
        self.assertTrue(hasattr(code, "parent_link"))

    def test_type_model_code(self):
        self.assertIsInstance(Code.id.type, db.Integer)
        self.assertIsInstance(Code.content.type, db.Text)
        self.assertIsInstance(Code.author.type, db.String)
        self.assertIsInstance(Code.message.type, db.String)
        self.assertIsInstance(Code.chat_link.type, db.Integer)
        self.assertIsInstance(Code.parent_link.type, db.Integer)

    def test_code_sending(self):
        send_code_id = Code.send(self.chat_id, CODE, USERNAME, PARENT_CODE_ID, COMMIT_MESSAGE)
        sent_code = Code.get(send_code_id)
        self.assertEquals(sent_code.get('author'), USERNAME)
        self.assertEquals(sent_code.get('code'), CODE)

    def test_get_root_in_chat_with_single_code(self):
        code = Code.get_root_in_chat(self.chat_id)
        self.assertIsInstance(code, Code)
        self.assertEquals(code.author, USERNAME)
        self.assertEquals(code.content, CHAT_CODE)
        self.assertEquals(code.chat_link, self.chat_id)
        self.assertEquals(code.parent_link, None)
        self.assertEquals(code.message, START_COMMIT_MESSAGE)

    def test_get_root_in_chat_with_many_codes(self):
        parent_code = Code.get_root_in_chat(self.chat_id)
        Code.send(self.chat_id, CHAT_CODE, USERNAME, parent_code.id, COMMIT_MESSAGE)
        got_root_code = Code.get_root_in_chat(self.chat_id)
        self.assertIsInstance(got_root_code, Code)
        self.assertEquals(got_root_code.id, parent_code.id)

    def test_get_commits_tree_with_single_code(self):
        tree = Code.get_commits_tree(self.chat_id)
        self.assertEqual(tree.get('text').get('name'), 1)
        self.assertEqual(tree.get('text').get('title'), START_COMMIT_MESSAGE)
        self.assertEqual(tree.get('children'), [])
        self.assertEqual(tree.get('innerHTML'), NODE_MARKUP.format(id=1))

    def test_get_commits_tree_with_many_codes(self):
        parent_code = Code.get_root_in_chat(self.chat_id)
        child_code_id = Code.send(self.chat_id, CHAT_CODE, USERNAME, parent_code.id, COMMIT_MESSAGE)
        tree = Code.get_commits_tree(self.chat_id)
        self.assertIsInstance(tree.get('children'), list)
        self.assertIsInstance(tree['children'][0], dict)
        self.assertIsInstance(tree['children'][0].get('text'), dict)
        self.assertEqual(tree['children'][0]['text'].get('name'), child_code_id)
