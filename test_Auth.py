import unittest
import requests
import json
import random

from test_utils import TestOutput

BASE_URL = "http://localhost:8080/api/v1"


class AuthAPITests(unittest.TestCase):
    """Позитивные тесты для эндпоинтов аутентификации"""

    def test_01_login_success(self):
        """Успешный вход в систему"""
        url = f"{BASE_URL}/auth/login"
        headers = {"Content-Type": "application/json"}
        data = {"login": "admin", "password": "Admin123!"}
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(200, response.status_code)
        TestOutput.print_result(self._testMethodName, response)

    def test_02_refresh_token_success(self):
        """Успешное обновление токена"""
        login_url = f"{BASE_URL}/auth/login"
        headers = {"Content-Type": "application/json"}
        login_data = {"login": "admin", "password": "Admin123!"}
        
        login_response = requests.post(login_url, headers=headers, data=json.dumps(login_data))
        refresh_token = login_response.json()["refreshToken"]
   
        url = f"{BASE_URL}/auth/refresh_token"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {refresh_token}"
        }
        
        response = requests.post(url, headers=headers)
        self.assertEqual(200, response.status_code)
        TestOutput.print_result(self._testMethodName, response)

    def test_03_google_oauth_success(self):
        """Успешный запрос OAuth2 Google"""
        url = f"{BASE_URL}/auth/login/oauth2/google"
        headers = {"Content-Type": "application/json"}
        
        response = requests.get(url, headers=headers)
        self.assertEqual(200, response.status_code)
        TestOutput.print_result(self._testMethodName, response)

    def test_04_logout_success(self):
        """Успешный выход из системы"""
        login_url = f"{BASE_URL}/auth/login"
        headers = {"Content-Type": "application/json"}
        login_data = {"login": "admin", "password": "Admin123!"}
        
        login_response = requests.post(login_url, headers=headers, data=json.dumps(login_data))
        access_token = login_response.json()["accessToken"]

        url = f"{BASE_URL}/auth/logout"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(url, headers=headers)
        self.assertEqual(200, response.status_code)
        TestOutput.print_result(self._testMethodName, response)

    def test_05_registration_success(self):
        """Успешная регистрация пользователя"""
        url = f"{BASE_URL}/auth/registration"
        headers = {"Content-Type": "application/json"}

        random_num = random.randint(10000, 99999)
        data = {
            "username": f"testuser{random_num}",
            "email": f"testuser{random_num}@example.com",
            "password": "Test123!"
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(200, response.status_code)
        TestOutput.print_result(self._testMethodName, response)


class AuthNegativeTests(unittest.TestCase):
    """Негативные тесты для эндпоинтов аутентификации"""
    
    def test_login_invalid_credentials(self):
        """Неуспешный вход с неверными данными"""
        url = f"{BASE_URL}/auth/login"
        headers = {"Content-Type": "application/json"}
        data = {"login": "nonexistent", "password": "WrongPass123!"}
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(404, response.status_code)
        TestOutput.print_result(self._testMethodName, response)

    def test_registration_username_conflict(self):
        """Регистрация с существующим username"""
        url = f"{BASE_URL}/auth/registration"
        headers = {"Content-Type": "application/json"}
        data = {
            "username": "admin",
            "email": "newemail@example.com",
            "password": "Test123!"
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(409, response.status_code)
        TestOutput.print_result(self._testMethodName, response)

    def test_registration_email_conflict(self):
        """Регистрация с существующим email"""
        url = f"{BASE_URL}/auth/registration"
        headers = {"Content-Type": "application/json"}
        data = {
            "username": "newuser",
            "email": "admin@example.com",
            "password": "Test123!"
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(409, response.status_code)
        TestOutput.print_result(self._testMethodName, response)

if __name__ == "__main__":
    unittest.main()