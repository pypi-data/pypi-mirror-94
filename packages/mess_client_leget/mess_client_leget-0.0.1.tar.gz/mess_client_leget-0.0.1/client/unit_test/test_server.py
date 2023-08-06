import os
import sys
import unittest

root_dir = os.path.normpath(os.path.join(os.getcwd(), '..'))
sys.path.append(root_dir)

from server.common import RESPONSE, ERROR
from server import process_client_message


class TestServer(unittest.TestCase):
    error_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    right_dict = {RESPONSE: 200}

    def test_no_action(self):
        """
        Тест функция, проверяет работу без параметра ACTION
        :return:
        """

        self.assertEqual(process_client_message({'time': 1607866996.0035086, 'user': {'account_name': 'Guest'}}),
                         self.error_dict, "Ошибка! Работает без параметра ACTION!")

    def test_no_time(self):
        """
        Тест функция, проверяет работу без параметра time
        :return:
        """

        self.assertEqual(process_client_message({'action': 'presence', 'user': {'account_name': 'Guest'}}),
                         self.error_dict, "Ошибка! Работает без параметра time!")

    def test_action_is_known(self):
        """
        Тест функция, проверяет работу с нейзвестным действием
        :return:
        """
        self.assertEqual(process_client_message({'action': 'unknown', 'time': 1607866996.0035086,
                                                 'user': {'account_name': 'Guest'}}), self.error_dict,
                         "Ошибка! Работает с неизвестным действием!")

    def test_no_user(self):
        """
        Тест функция, проверяет работу без параметра user
        :return:
        """
        self.assertEqual(process_client_message({'action': 'presence', 'time': 1607866996.0035086}), self.error_dict,
                         "Ошибка! Работает без параметра user!")

    def test_user_not_guest(self):
        """
        Тест функция, проверяет работу c параметром user не Guest
        :return:
        """
        self.assertEqual(process_client_message({'action': 'presence', 'time': 1607866996.0035086,
                                                 'user': {'account_name': 'Guido'}}), self.error_dict,
                         "Ошибка! Работает с параметром user не Guest!")

    def test_all_right(self):
        """
        Тест функция, проверяет правильную работу
        :return:
        """
        self.assertEqual(process_client_message({'action': 'presence', 'time': 1607866996.0035086,
                                                 'user': {'account_name': 'Guest'}}), self.right_dict,
                         'Ошибка, не работает с правильными параметрами')

    def test_valid_time(self):
        """
        Тест функция, проверяет что вернулся словарь
        :return:
        """
        self.assertIsInstance(process_client_message({'action': 'presence', 'time': 1607866996.0035086,
                                                      'user': {'account_name': 'Guest'}}), dict,
                              'Ошибка! Вернулся не словарь')


if __name__ == '__main__':
    unittest.main()
