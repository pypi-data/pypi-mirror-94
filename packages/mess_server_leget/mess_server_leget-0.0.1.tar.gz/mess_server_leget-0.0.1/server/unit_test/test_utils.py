import json
import os
import sys
import unittest

root_dir = os.path.normpath(os.path.join(os.getcwd(), '../..'))
sys.path.append(root_dir)
from server.common.settings import ENCODING, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoding_message = None
        self.received_message = None

    def send(self, test_message_to_send):
        test_json_message = json.dumps(self.test_dict)
        self.encoding_message = test_json_message.encode(settings.ENCODING)
        self.received_message = test_message_to_send

    def recv(self, max_length):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestUtils(unittest.TestCase):
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }
    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_err = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    test_str_recv_err = 'error'

    def test_get_message(self):
        """
        Тест функция проверяет корректность расшифровки словаря
        :return:
        """
        test_socket_ok = TestSocket(self.test_dict_recv_ok)
        test_socket_error = TestSocket(self.test_dict_recv_err)
        test_socket_str = TestSocket(self.test_str_recv_err)
        test_socket_none = TestSocket(None)
        self.assertEqual(get_message(test_socket_ok), self.test_dict_recv_ok)
        self.assertEqual(get_message(test_socket_error), self.test_dict_recv_err)
        # проверяет будет ли исключение, если отправить не словарь
        with self.assertRaises(ValueError):
            get_message(test_socket_str)
        # проверяет будет ли исключение, если не будет данных
        with self.assertRaises(ValueError):
            get_message(test_socket_none)

    def test_send_message(self):
        test_socket = TestSocket(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)
        self.assertEqual(test_socket.encoding_message, test_socket.received_message)
        # проверяет будет ли исключение, если отправить вместо socket словарь
        with self.assertRaises(Exception):
            send_message(self.test_dict_send, self.test_dict_recv_err)
        # прверяет будет ли исключение, если отправить вместо словаря другой объект
        with self.assertRaises(Exception):
            send_message(test_socket, test_socket)


if __name__ == '__main__':
    unittest.main()
