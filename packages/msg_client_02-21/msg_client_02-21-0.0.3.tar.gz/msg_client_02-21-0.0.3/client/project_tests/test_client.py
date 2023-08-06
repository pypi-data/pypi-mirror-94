"""Unit тест скрипта клиента."""

import unittest
from Cryptodome.PublicKey import RSA

from client.transport import ClientTransport
from server.server.core import HandlerMessage

from common.constants import ACTION, TIME, TYPE, \
    STATUS, USER, ACCOUNT_NAME, DEFAULT_ACCOUNT_NAME, ERROR_COMMENT, RESPONSE, ERROR, TYPE_ACTION_PRESENCE, PUBLIC_KEY, DEFAULT_HOSTNAME, DEFAULT_PORT


class TestClient(unittest.TestCase):
    def setUp(self):
        self.server_obj = HandlerMessage(DEFAULT_HOSTNAME, DEFAULT_PORT, None)
        self.client_obj = ClientTransport(DEFAULT_HOSTNAME, DEFAULT_PORT, None, None, None, RSA.generate(2048))
        self.client_message = self.transport_obj.create_message(TYPE_ACTION_PRESENCE)
        self.client_message[TIME] = 12.34
        self.valid_client_message = {
            ACTION: TYPE_ACTION_PRESENCE,
            TIME: 12.34,
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: DEFAULT_ACCOUNT_NAME,
                PUBLIC_KEY: '123'
            }
        }



        self.notice_of_success = '200: OK'
        self.notice_of_error = f'400: {ERROR_COMMENT}'
        self.success_server_answer = {RESPONSE: 200}
        self.error_server_answer = {RESPONSE: 400, ERROR: ERROR_COMMENT}
        self.except_er_server_answer = {}

    def tearDown(self):
        pass

    def test_check_valid_client_message(self):
        self.assertEqual(self.client_message, self.valid_client_message)

    def test_get_success_answer(self):
        self.assertEqual(
            self.transport_obj.check_answer(),
            self.notice_of_success)

    def test_get_error_answer(self):
        self.assertEqual(
            self.transport_obj.check_answer(),
            self.notice_of_error)

    def test_get_exception(self):
        self.assertRaises(
            ValueError,
            self.transport_obj.check_answer,
            self.except_er_server_answer)




if __name__ == '__main__':
    unittest.main()
