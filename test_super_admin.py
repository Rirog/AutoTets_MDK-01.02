import unittest
import requests
import json

BASE_URL = "http://localhost:8080/api/v1"


class SuperAdminTests(unittest.TestCase):
    """Тесты для endpoint'ов супер-администратора"""

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

    def test_create_new_admin(self):
        """Тест создания нового администратора"""
        url = f"{BASE_URL}/admin/create/admin"
        data = {
            "username": "newadmin",
            "email": "newadmin@example.com",
            "password": "NewAdmin123!"
        }
        response = requests.post(url, headers=self.user_headers, data=json.dumps(data))
        self.assertIn(response.status_code, [200, 403, 409])

    def test_get_all_admins_info(self):
        """Тест получения информации о всех администраторах"""
        url = f"{BASE_URL}/admin/list/admins"
        response = requests.get(url, headers=self.user_headers)
        self.assertEqual(200, response.status_code)

    def test_get_all_admins_info_with_params(self):
        """Тест получения информации о администраторах с параметрами"""
        url = f"{BASE_URL}/admin/list/admins"
        params = {"username": "newadmin", "email": "Newadmin@example.com"}
        response = requests.get(url, headers=self.user_headers, params=params)
        self.assertEqual(200, response.status_code)
        print(response.text)

    def test_get_admin_info(self):
        """Тест получения информации об администраторе по ID"""
        url = f"{BASE_URL}/admin/info/admin"
        params = {"id": 2}
        response = requests.get(url, headers=self.user_headers, params=params)
        self.assertIn(response.status_code, [200, 404])

    def test_delete_admin(self):
        """Тест удаления администратора"""
        url = f"{BASE_URL}/admin/delete/admin"
        params = {"id": 2}
        response = requests.delete(url, headers=self.user_headers, params=params)
        self.assertEqual(200, response.status_code)

if __name__ == "__main__":
    unittest.main()