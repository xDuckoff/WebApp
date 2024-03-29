# -*- coding: utf-8 -*-

"""Тесты методов чата"""

from base_test_model import *
from application import db
from application.models import Message, Chat, Code, MarkdownMixin


class TestChatModel(BaseTestModel):

    def setUp(self):
        BaseTestModel.setUp(self)
        self.chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE)

    def __create_mock_chats(self, count):
        db.session.remove()
        db.drop_all()
        db.create_all()
        langs = app.config['ALLOWED_LANGUAGES']
        for i in xrange(count):
            Chat.create('Chat name', 'Chat code', langs[i % len(langs)]['type'])


    def test_available_chat(self):
        self.assertTrue(hasattr(Chat, "id"))
        self.assertTrue(hasattr(Chat, "name"))
        self.assertTrue(hasattr(Chat, "create_time"))
        self.assertTrue(hasattr(Chat, "remove_time"))

    def test_type_model_chat(self):
        self.assertIsInstance(Chat.id.type, db.Integer)
        self.assertIsInstance(Chat.name.type, db.String)
        self.assertIsInstance(Chat.create_time.type, db.DateTime)
        self.assertIsInstance(Chat.remove_time.type, db.DateTime)

    def test_create_chat(self):
        chat = Chat.get(self.chat_id)
        chat_info = chat.get_info()
        self.assertEquals(chat_info.get('name'), MarkdownMixin.decode(CHAT_NAME))
        self.assertEquals(chat_info.get('code_type'), CODE_TYPE)

    def test_get_all_messages(self):
        second_message = Message.send(self.chat_id, MESSAGE, MESSAGE_TYPE)
        third_message = Message.send(self.chat_id, MESSAGE, MESSAGE_TYPE)
        chat = Chat.get(self.chat_id)
        got_messages = chat.get_last_messages()
        self.assertEqual(len(got_messages), 3)
        self.assertEqual(got_messages[1].get('id'), second_message.id)
        self.assertEqual(got_messages[2].get('id'), third_message.id)

    def test_chat_has_message(self):
        chat = Chat.get(self.chat_id)
        message_id = Message.send(self.chat_id, MESSAGE, 'usr').id - 1
        self.assertTrue(chat.has_message(str(message_id)))
        self.assertFalse(chat.has_message(str(message_id + 1)))

    def test_chat_has_code(self):
        chat = Chat.get(self.chat_id)
        code_id = Code.send(self.chat_id, CODE, PARENT_CODE_ID, COMMIT_MESSAGE) - 1
        self.assertTrue(chat.has_code(str(code_id)))
        self.assertFalse(chat.has_code(str(code_id + 1)))

    def test_find_chat_by_full_name(self):
        search_name = CHAT_NAME
        found_chat_list = Chat.find(search_name)
        self.assertGreaterEqual(len(found_chat_list), 1)
        self.assertEqual(found_chat_list[0].name, MarkdownMixin.decode(CHAT_NAME))

    def test_find_chat_by_name(self):
        search_name = CHAT_NAME[2:-2]
        found_chat_list = Chat.find(search_name)
        self.assertGreaterEqual(len(found_chat_list), 1)
        self.assertIn(search_name, found_chat_list[0].name)

    def test_find_chat_by_id(self):
        search_id = str(self.chat_id)
        found_chat_list = Chat.find(search_id)
        self.assertEqual(len(found_chat_list), 1)
        self.assertEqual(found_chat_list[0].id, int(search_id))

    def test_find_chat_all(self):
        CHAT_COUNT = 15
        INFINITELY_LIMIT = 0
        self.__create_mock_chats(CHAT_COUNT)
        chats = Chat.find('', limit=INFINITELY_LIMIT)
        self.assertEqual(len(chats), CHAT_COUNT)
        # self.assertLessEqual(len(Chat.find('')), 10)

    def test_find_with_limit(self):
        CHAT_COUNT = 10
        LIMIT = 5
        self.__create_mock_chats(CHAT_COUNT)
        chats = Chat.find('', limit=LIMIT)
        self.assertEqual(len(chats), LIMIT)

    def test_find_with_page(self):
        CHAT_COUNT = 6
        LIMIT = 5
        PAGE = 2
        self.__create_mock_chats(CHAT_COUNT)
        chats = Chat.find('', limit=LIMIT, page=PAGE)
        self.assertEqual(len(chats), CHAT_COUNT - LIMIT)

    def test_get_last_messages(self):
        chat = Chat.get(self.chat_id)
        old_message = Message.send(self.chat_id, MESSAGE, MESSAGE_TYPE)
        new_message = Message.send(self.chat_id, MESSAGE, MESSAGE_TYPE)
        got_last_messages = chat.get_last_messages(old_message.id)
        self.assertEqual(len(got_last_messages), 1)
        self.assertEqual(got_last_messages[0].get('id'), new_message.id)

    def test_is_access_key_valid(self):
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, CHAT_ACCESS_KEY)
        chat = Chat.get(chat_id)
        self.assertTrue(chat.is_access_key_valid(CHAT_ACCESS_KEY))
        self.assertFalse(chat.is_access_key_valid(CHAT_INCORRECT_ACCESS_KEY))

    def test_change_chat_name(self):
        new_chat_name = CHAT_NAME * 2
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, CHAT_ACCESS_KEY)
        chat = Chat.get(chat_id)
        chat.set_name(new_chat_name)
        chat = Chat.get(chat_id)
        self.assertEqual(chat.name, MarkdownMixin.decode(new_chat_name))

    def test_set_chat_name_return(self):
        new_chat_name = CHAT_NAME * 2
        chat_id = Chat.create(CHAT_NAME, CHAT_CODE, CODE_TYPE, CHAT_ACCESS_KEY)
        chat = Chat.get(chat_id)
        set_chat_name_return = chat.set_name(new_chat_name)
        self.assertIsInstance(set_chat_name_return, dict)
        self.assertEqual(set_chat_name_return.get('original', None), chat.name)
        self.assertNotEqual(set_chat_name_return.get('plain', None), None)
        self.assertNotEqual(set_chat_name_return.get('escaped', None), None)
