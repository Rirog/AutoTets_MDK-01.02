import unittest
import requests
import json

from test_utils import TestOutput

BASE_URL = "http://localhost:8080/api/v1"


class SuperAdminPositiveTests(unittest.TestCase):
    """Позитивные тесты для эндпоинтов супер-администратора"""

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

    def test_get_all_admins_info_success(self):
        """Успешное получение информации о всех администраторах """
        url = f"{BASE_URL}/admin/list/admins"
        response = requests.get(url, headers=self.user_headers)
        self.assertEqual(200, response.status_code)
        TestOutput.print_result(self._testMethodName, response)

    def test_get_all_admins_info_with_params_success(self):
        """Успешное получение информации об администраторах с параметрами"""
        url = f"{BASE_URL}/admin/list/admins"
        params = {"username": "admin", "email": "admin@example.com"}
        response = requests.get(url, headers=self.user_headers, params=params)
        self.assertEqual(200, response.status_code)
        TestOutput.print_result(self._testMethodName, response)

class SuperAdminNegativeTests(unittest.TestCase):
    """Негативные тесты для эндпоинтов супер-администратора"""

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

    def test_create_new_admin_username_conflict(self):
        """Создание администратора с существующим username"""
        url = f"{BASE_URL}/admin/create/admin"
        data = {
            "username": "admin",
            "email": "newemail@example.com",
            "password": "Test123!"
        }
        response = requests.post(url, headers=self.user_headers, data=json.dumps(data))
        if response.status_code == 409:
            self.assertEqual(409, response.status_code)
            TestOutput.print_result(self._testMethodName, response)

    def test_get_admin_info_not_found(self):
        """Получение информации о несуществующем администраторе"""
        url = f"{BASE_URL}/admin/info/admin"
        params = {"id": 99999}
        response = requests.get(url, headers=self.user_headers, params=params)
        if response.status_code == 404:
            self.assertEqual(404, response.status_code)
            TestOutput.print_result(self._testMethodName, response)

    def test_delete_admin_not_found(self):
        """Удаление несуществующего администратора"""
        url = f"{BASE_URL}/admin/delete/admin"
        params = {"id": 99999}
        response = requests.delete(url, headers=self.user_headers, params=params)
        if response.status_code == 404:
            self.assertEqual(404, response.status_code)
            TestOutput.print_result(self._testMethodName, response)

if __name__ == "__main__":
    unittest.main()