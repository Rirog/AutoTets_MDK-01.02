import unittest
import requests
import json

BASE_URL = "http://localhost:8080/api/v1"


class AdminUsersTests(unittest.TestCase):
    """Тесты для endpoint'ов модерации пользователей"""

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

    def test_get_all_users_info(self):
        """Тест получения информации о всех пользователях"""
        url = f"{BASE_URL}/admin/list/users"
        response = requests.get(url, headers=self.user_headers)

        self.assertIn(response.status_code, [200, 403])

    def test_get_all_users_info_with_params(self):
        """Тест получения информации о пользователях с параметрами"""
        url = f"{BASE_URL}/admin/list/users"
        params = {"username": "Dupling1", "email": "Dupling1@example.com", "isBanned": False}
        response = requests.get(url, headers=self.user_headers, params=params)
        self.assertIn(response.status_code, [200, 403])

    def test_get_all_banned_users(self):
        """Тест получения информации о забаненных пользователях"""
        url = f"{BASE_URL}/admin/list/users"
        params = {"isBanned": True}
        response = requests.get(url, headers=self.user_headers, params=params)
        self.assertIn(response.status_code, [200, 403])

    def test_get_user_info_by_id(self):
        """Тест получения информации о пользователе по ID"""

        url = f"{BASE_URL}/admin/info/user/1"
        response = requests.get(url, headers=self.user_headers)

        self.assertIn(response.status_code, [200, 403, 404])

    def test_get_user_warnings(self):
        """Тест получения предупреждений пользователя"""
        url = f"{BASE_URL}/admin/info/user/1/warnings"
        response = requests.get(url, headers=self.user_headers)
        self.assertIn(response.status_code, [200, 403, 404])

    def test_revoke_one_active_warning(self):
        """Тест снятия одного активного предупреждения"""
        url = f"{BASE_URL}/admin/warnings/revoke/1"
        response = requests.delete(url, headers=self.user_headers)

        self.assertIn(response.status_code, [200, 400, 403, 404])

    def test_revoke_all_active_warnings(self):
        """Тест снятия всех активных предупреждений"""
        url = f"{BASE_URL}/admin/warnings/revoke/all/1"
        response = requests.delete(url, headers=self.user_headers)
        self.assertIn(response.status_code, [200, 400, 403, 404])

    def test_ban_user(self):
        """Тест бана пользователя"""
        url = f"{BASE_URL}/admin/ban/user/1"
        response = requests.put(url, headers=self.user_headers)

        self.assertIn(response.status_code, [200, 400, 403, 404, 409])

    def test_unban_user(self):
        """Тест разбана пользователя"""
        url = f"{BASE_URL}/admin/unban/user/1"
        response = requests.put(url, headers=self.user_headers)

        self.assertIn(response.status_code, [200, 400, 403, 404, 409])



if __name__ == "__main__":
    unittest.main()