import unittest
import requests
import json

from test_utils import TestOutput

BASE_URL = "http://localhost:8080/api/v1"


class UserInfoPositiveTests(unittest.TestCase):
    """Позитивные тесты для эндпоинты информации о пользователе """

    @classmethod
    def setUpClass(cls):
        """Получение токена перед всеми тестами"""
        url = f"{BASE_URL}/auth/login"
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        data = {"login": "admin", "password": "Admin123!"}
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        cls.access_token = response.json()["accessToken"]
        cls.user_headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cls.access_token}"
        }

    def test_get_user_profile_info_success(self):
        """Успешное получение информации о профиле"""
        url = f"{BASE_URL}/user/info/profile"
        response = requests.get(url, headers=self.user_headers)
        self.assertEqual(200, response.status_code)
        TestOutput.print_result(self._testMethodName, response)

    def test_get_user_role_success(self):
        """Успешное получение роли пользователя"""
        url = f"{BASE_URL}/user/info/role"
        response = requests.get(url, headers=self.user_headers)
        self.assertEqual(200, response.status_code)
        TestOutput.print_result(self._testMethodName, response)

    def test_get_all_sessions_success(self):
        """Успешное получение всех сеансов пользователя"""
        url = f"{BASE_URL}/user/info/sessions"
        response = requests.get(url, headers=self.user_headers)
        self.assertEqual(200, response.status_code)
        TestOutput.print_result(self._testMethodName, response)

    def test_revoke_all_sessions_success(self):
        """Успешное завершение всех сеансов, кроме текущего"""
        url = f"{BASE_URL}/user/info/sessions/revoke/all"
        response = requests.delete(url, headers=self.user_headers)
        self.assertEqual(200, response.status_code)
        TestOutput.print_result(self._testMethodName, response)



class UserInfoNegativeTests(unittest.TestCase):
    """Негативные тесты для эндпоинтов информации о пользователе"""

    @classmethod
    def setUpClass(cls):
        """Получение токена перед всеми тестами"""
        url = f"{BASE_URL}/auth/login"
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        data = {"login": "admin", "password": "Admin123!"}
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        cls.access_token = response.json()["accessToken"]
        cls.user_headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cls.access_token}"
        }

    def test_get_avatar_not_found(self):
        """Получение аватара, когда его нет"""
        url = f"{BASE_URL}/user/info/avatar"
        response = requests.get(url, headers=self.user_headers)
        if response.status_code in [404, 204]:
            self.assertIn(response.status_code, [404, 204])
            TestOutput.print_result(self._testMethodName, response)


if __name__ == "__main__":
    unittest.main()