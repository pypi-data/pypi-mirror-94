import os
import sys
import unittest

root_dir = os.path.normpath(os.path.join(os.getcwd(), '../..'))
sys.path.append(root_dir)

from client.client import create_presence, process_ans
from server.common.settings import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestClient(unittest.TestCase):
    def test_valid_request(self):
        """
        Тест функция, проверяет правильность запроса
        :return:
        """
        test_request = create_presence()
        test_request[TIME] = 15.15
        self.assertEqual(test_request, {ACTION: PRESENCE, TIME: 15.15, USER: {ACCOUNT_NAME: 'Guest'}}, 'Ошибка запроса')
        # на мощном компьютере работает и вариант ниже, а тестировал на виртульной машине,
        # там время разное на последнюю цифру
        # self.assertEqual(test_request, {ACTION: PRESENCE, TIME: time(), USER: {ACCOUNT_NAME: 'Guest'}},
        # 'Ошибка запроса')

    def test_return_dict(self):
        """
        Тест функция, проверяет, что возвращается словарь
        :return:
        """
        self.assertIsInstance(create_presence(), dict, "Ошибка, вернулся не словарь")

    def test_response_200_pars(self):
        """
        Тест функция, проверяет правильно ли разобран ответ 200
        :return:
        """
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : все работает')

    def test_response_pars(self):
        """
        Тест функция, проверяет правильно ли разобран ответ не 200
        :return:
        """
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad request'}), '400 : Bad request')

    def test_error(self):
        """
        Тест функция, проверяет вернет ли функция ValueError? если нет RESPONSE в message
        :return:
        """
        with self.assertRaises(ValueError):
            process_ans({ERROR: 'Bad request'})


if __name__ == '__main__':
    unittest.main()
