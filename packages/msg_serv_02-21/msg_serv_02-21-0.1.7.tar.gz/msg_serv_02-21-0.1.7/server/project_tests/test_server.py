"""Unit тест скрипта сервера"""

import unittest
from server import create_response_message
from common.constants import *


class TestServer(unittest.TestCase):
    def setUp(self):
        self.success_answer = {RESPONSE: 200}
        self.error_answer = {RESPONSE: 400, ERROR: ERROR_COMMENT}
        self.valid_message = {
            ACTION: TYPE_ACTION,
            TIME: 12.34,
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: DEFAULT_ACCOUNT_NAME,
                STATUS: DEFAULT_STATUS
            }
        }
        self.not_action_message = {
            TIME: 12.34,
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: DEFAULT_ACCOUNT_NAME,
                STATUS: DEFAULT_STATUS
            }
        }
        self.wrong_action_message = {
            ACTION: 'some action',
            TIME: 12.34,
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: DEFAULT_ACCOUNT_NAME,
                STATUS: DEFAULT_STATUS
            }
        }
        self.not_time_message = {
            ACTION: TYPE_ACTION,
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: DEFAULT_ACCOUNT_NAME,
                STATUS: DEFAULT_STATUS
            }
        }
        self.not_user_message = {
            ACTION: TYPE_ACTION,
            TIME: 12.34,
            TYPE: STATUS,
        }
        self.not_user_name_message = {
            ACTION: TYPE_ACTION,
            TIME: 12.34,
            TYPE: STATUS,
            USER: {
                STATUS: DEFAULT_STATUS
            }
        }
        self.not_user_status_message = {
            ACTION: TYPE_ACTION,
            TIME: 12.34,
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: DEFAULT_ACCOUNT_NAME,
            }
        }

    def tearDown(self):
        pass

    def test_get_success_response(self):
        self.assertEqual(create_response_message(self.valid_message), self.success_answer)

    def test_get_without_action(self):
        self.assertEqual(create_response_message(self.not_action_message), self.error_answer)

    def test_get_wrong_action(self):
        self.assertEqual(create_response_message(self.wrong_action_message), self.error_answer)

    def test_get_without_time(self):
        self.assertEqual(create_response_message(self.not_time_message), self.error_answer)

    def test_get_without_user(self):
        self.assertEqual(create_response_message(self.not_user_message), self.error_answer)

    def test_get_without_user_name(self):
        self.assertEqual(create_response_message(self.not_user_name_message), self.error_answer)

    def test_get_without_user_status(self):
        self.assertEqual(create_response_message(self.not_user_status_message), self.error_answer)


if __name__ == '__main__':
    unittest.main()
