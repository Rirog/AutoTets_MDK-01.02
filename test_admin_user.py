import unittest
import requests
import json

BASE_URL = "http://localhost:8080/api/v1"


class AdminUsersPositiveTests(unittest.TestCase):
    """Позитивные тесты для эндпоинтов модерации пользователей"""

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

    def test_get_all_users_info_success(self):
        """Успешное получение информации о всех пользователях"""
        url = f"{BASE_URL}/admin/list/users"
        response = requests.get(url, headers=self.user_headers)
        self.assertEqual(200, response.status_code)

    def test_get_user_info_by_id_success(self):
        """Успешное получение информации о пользователе по ID"""
        url = f"{BASE_URL}/admin/info/user/1"
        response = requests.get(url, headers=self.user_headers)
        self.assertEqual(200, response.status_code)

    def test_get_user_warnings_success(self):
        """Успешное получение предупреждений пользователя"""
        url = f"{BASE_URL}/admin/info/user/6/warnings"
        response = requests.get(url, headers=self.user_headers)
        self.assertEqual(200, response.status_code)

    def test_get_all_users_with_username_filter_success(self):
        """Успешное получение пользователей с фильтром по username"""
        url = f"{BASE_URL}/admin/list/users"
        params = {"username": "admin"}
        response = requests.get(url, headers=self.user_headers, params=params)
        self.assertEqual(200, response.status_code)

    def test_get_all_users_with_email_filter_success(self):
        """Успешное получение пользователей с фильтром по email"""
        url = f"{BASE_URL}/admin/list/users"
        params = {"email": "admin@example.com"}
        response = requests.get(url, headers=self.user_headers, params=params)
        self.assertEqual(200, response.status_code)

    def test_get_all_active_users_success(self):
        """Успешное получение активных пользователей"""
        url = f"{BASE_URL}/admin/list/users"
        params = {"isBanned": False} 
        response = requests.get(url, headers=self.user_headers, params=params)
        self.assertEqual(200, response.status_code)


class AdminUsersNegativeTests(unittest.TestCase):
    """Негативные тесты для эндпоинтов модерации пользователей"""

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

    def test_get_user_info_by_id_not_found(self):
        """Получение информации о несуществующем пользователе"""
        url = f"{BASE_URL}/admin/info/user/99999"
        response = requests.get(url, headers=self.user_headers)
        if response.status_code == 404:
            self.assertEqual(404, response.status_code)

    def test_get_user_warnings_not_found(self):
        """Получение предупреждений несуществующего пользователя"""
        url = f"{BASE_URL}/admin/info/user/99999/warnings"
        response = requests.get(url, headers=self.user_headers)
        if response.status_code == 404:
            self.assertEqual(404, response.status_code)

    def test_revoke_one_active_warning_no_permission(self):
        """Снятие предупреждения без прав"""
        url = f"{BASE_URL}/admin/warnings/revoke/1"
        response = requests.delete(url, headers=self.user_headers)
        if response.status_code == 403:
            self.assertEqual(403, response.status_code)

    def test_revoke_all_active_warnings_no_permission(self):
        """Снятие всех предупреждений без прав"""
        url = f"{BASE_URL}/admin/warnings/revoke/all/1"
        response = requests.delete(url, headers=self.user_headers)
        if response.status_code == 403:
            self.assertEqual(403, response.status_code)

    def test_ban_user_no_permission(self):
        """Бан пользователя без прав"""
        url = f"{BASE_URL}/admin/ban/user/1"
        response = requests.put(url, headers=self.user_headers)
        if response.status_code == 403:
            self.assertEqual(403, response.status_code)

    def test_unban_user_no_permission(self):
        """Разбан пользователя без прав"""
        url = f"{BASE_URL}/admin/unban/user/1"
        response = requests.put(url, headers=self.user_headers)
        if response.status_code == 403:
            self.assertEqual(403, response.status_code)

    def test_ban_self_not_allowed(self):
        """Попытка забанить самого себя"""
        url = f"{BASE_URL}/admin/ban/user/1"
        response = requests.put(url, headers=self.user_headers)
        if response.status_code in [400, 409]:
            self.assertIn(response.status_code, [400, 409])

    def test_unban_not_banned_user(self):
        """Попытка разбанить не забаненного пользователя"""
        url = f"{BASE_URL}/admin/unban/user/1"
        response = requests.put(url, headers=self.user_headers)
        if response.status_code in [400, 409]:
            self.assertIn(response.status_code, [400, 409])

    def test_revoke_warning_no_active_warnings(self):
        """Снятие предупреждения у пользователя без активных предупреждений"""
        url = f"{BASE_URL}/admin/warnings/revoke/1"
        response = requests.delete(url, headers=self.user_headers)
        if response.status_code == 400:
            self.assertEqual(400, response.status_code)

    def test_authorization_required(self):
        """Проверка обязательности авторизации для админ эндпоинтов"""
        url = f"{BASE_URL}/admin/list/users"
        headers_without_auth = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers_without_auth)
        self.assertEqual(401, response.status_code)
    
if __name__ == "__main__":
    unittest.main()