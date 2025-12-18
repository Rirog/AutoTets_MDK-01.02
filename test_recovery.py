import unittest
import requests
import json
import random

BASE_URL = "http://localhost:8080/api/v1"


class RecoveryPositiveTests(unittest.TestCase):
    """Позитивные тесты восстановления аккаунта"""
    
    def test_reset_password_success(self):
        """Успешный запрос сброса пароля"""
        url = f"{BASE_URL}/recovery/reset-password"
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        data = {"email": "admin@example.com"}
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(200, response.status_code)

    def test_resend_activation_success(self):
        """Успешная повторная отправка активации"""
        reg_url = f"{BASE_URL}/auth/registration"
        reg_headers = {"accept": "application/json", "Content-Type": "application/json"}
        random_num = random.randint(100000, 999999)
        reg_data = {
            "username": f"testuser{random_num}",
            "email": f"testuser{random_num}@example.com",
            "password": "Test123!"
        }
        
        reg_response = requests.post(reg_url, headers=reg_headers, data=json.dumps(reg_data))
        self.assertEqual(200, reg_response.status_code)
        url = f"{BASE_URL}/recovery/resend-activation"
        data = {"email": f"testuser{random_num}@example.com"}
        
        response = requests.post(url, headers=reg_headers, data=json.dumps(data))
        self.assertEqual(200, response.status_code)


class RecoveryNegativeTests(unittest.TestCase):
    """Негативные тесты восстановления аккаунта"""
    
    def test_resend_activation_already_activated(self):
        """Повторная активация для уже активированного"""
        url = f"{BASE_URL}/recovery/resend-activation"
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        data = {"email": "admin@example.com"}
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(400, response.status_code)

    def test_reset_password_empty_email(self):
        """Сброс пароля с пустым email"""
        url = f"{BASE_URL}/recovery/reset-password"
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        data = {"email": ""}
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(400, response.status_code)


if __name__ == "__main__":
    unittest.main()