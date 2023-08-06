"""Unit тест общих функций"""

import json
import unittest
from common.constants import ENCODING, ACTION, TIME, TYPE, STATUS, USER, ACCOUNT_NAME, \
    DEFAULT_ACCOUNT_NAME, DEFAULT_STATUS, RESPONSE, ERROR, ERROR_COMMENT, SIZE_PACKET, \
    TYPE_ACTION_PRESENCE
from common.functions import get_data, send_data, validate_port_number


class TestSocket:

    def __init__(self, dct_to_send):
        self.dct_to_send = dct_to_send
        self.test_encoded_msg = None
        self.encoded_msg = None

    def send(self, encoded_msg):
        self.test_encoded_msg = json.dumps(self.dct_to_send).encode(ENCODING)
        self.encoded_msg = encoded_msg

    def recv(self, size_pack):
        test_encoded_str = json.dumps(self.dct_to_send).encode(ENCODING)
        return test_encoded_str


class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.test_dct = {
            ACTION: TYPE_ACTION_PRESENCE,
            TIME: 12.34,
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: DEFAULT_ACCOUNT_NAME,
                STATUS: DEFAULT_STATUS
            }
        }
        self.test_dct_success = {RESPONSE: 200}
        self.test_dct_error = {RESPONSE: 400,
                               ERROR: ERROR_COMMENT}

        self.test_sock_client = TestSocket(self.test_dct)
        self.test_sock_success = TestSocket(self.test_dct_success)
        self.test_sock_error = TestSocket(self.test_dct_error)

        self.valid_port_number = 8000
        self.invalid_port_number = 80

    def tearDown(self):
        pass

    def test_check_send_msg(self):
        self.assertEqual(self.test_sock_client.test_encoded_msg, self.test_sock_client.encoded_msg)

    def test_get_send_exception(self):
        self.assertRaises(TypeError, send_data, self.test_sock_client, self.test_sock_client)

    def test_check_recv_success(self):
        self.assertEqual(get_data(self.test_sock_success, SIZE_PACKET), self.test_dct_success)

    def test_check_recv_error(self):
        self.assertEqual(get_data(self.test_sock_error, SIZE_PACKET), self.test_dct_error)

    def test_get_recv_exception(self):
        with self.assertRaises(AttributeError):
            get_data(self.test_dct, SIZE_PACKET)

    def test_check_port_number(self):
        self.assertTrue(validate_port_number(self.valid_port_number))

    def test_check_port_number_exception(self):
        with self.assertRaises(ValueError):
            validate_port_number(self.invalid_port_number)


if __name__ == '__main__':
    unittest.main()
