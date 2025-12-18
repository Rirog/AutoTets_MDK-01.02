import unittest
import requests
import json

BASE_URL = "http://localhost:8080/api/v1"


class AuthAPITests(unittest.TestCase):
    """Набор автотестов для endpoint'ов аутентификации"""

    def test_01_login(self):
        """Тест входа в систему"""
        url = f"{BASE_URL}/auth/login"
        headers = {"Content-Type": "application/json"}
        data = {"login": "admin", "password": "Admin123!"}
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        self.assertEqual(200, response.status_code)
        response_json = response.json()
        self.assertIn("accessToken", response_json)
        self.assertIn("refreshToken", response_json)

        AuthAPITests.access_token = response_json["accessToken"]
        AuthAPITests.refresh_token = response_json["refreshToken"]


    def test_02_refresh_token(self):
        """Тест обновления токена"""
        url = f"{BASE_URL}/auth/refresh_token"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AuthAPITests.refresh_token}"
        }
        
        response = requests.post(url, headers=headers)
        
        self.assertEqual(200, response.status_code)
        response_json = response.json()
        self.assertIn("accessToken", response_json)
        self.assertIn("refreshToken", response_json)
        

        AuthAPITests.access_token = response_json["accessToken"]
        AuthAPITests.refresh_token = response_json["refreshToken"]


    def test_03_google_oauth(self):
        """Тест OAuth2 Google"""
        url = f"{BASE_URL}/auth/login/oauth2/google"
        headers = {"Content-Type": "application/json"}
        
        response = requests.get(url, headers=headers)
        
        self.assertEqual(200, response.status_code)
        response_json = response.json()
        
        self.assertEqual("/oauth2/authorization/google", response_json["oauthUrl"])
        self.assertEqual("/login/oauth2/code/google", response_json["successUrl"])


    def test_04_logout(self):
        """Тест выхода из системы"""
        url = f"{BASE_URL}/auth/logout"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {AuthAPITests.access_token}"
        }
        
        response = requests.get(url, headers=headers)

        self.assertEqual(200, response.status_code)
    
    
    def test_05_registration(self):
        """Тест регистрации пользователя"""
        url = f"{BASE_URL}/auth/registration"
        headers = {"Content-Type": "application/json"}
        data = {
            "username": "Dupling1",
            "email": "Duplin1g@example.com",
            "password": "Dupling123!"
        }

        responce = requests.post(url, headers=headers, data=json.dumps(data))

        self.assertEqual(200, responce.status_code)
        response_json = responce.json()
        self.assertIn("Письмо с подтверждением регистрации отправлено", response_json["message"])


if __name__ == "__main__":
    unittest.main()