import unittest
import requests
import json

BASE_URL = "http://localhost:8080/api/v1"


class RecoveryAccountTests(unittest.TestCase):
    """Тесты для endpoint'ов восстановления аккаунта"""



    def test_reset_password_positive(self):
        """Позитивный тест сброса пароля"""

        url = f"{BASE_URL}/recovery/reset-password"

        headers = {"accept": "application/json", "Content-Type": "application/json"}
        data = {"email": "admin@example.com"}

        response = requests.post(url, headers=headers, data=json.dumps(data))

        self.assertEqual(200, response.status_code)
        response_json = response.json()
        self.assertIn("message", response_json)


    def test_resend_activation_already_activated(self):
        """Тест повторной отправки ативации аккаунта"""
        url = f"{BASE_URL}/recovery/resend-activation"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {"email": "john@example.com"}
        data_reg = {
            "username": "Dupling2",
            "email": "Dupling2@example.com",
            "password": "Dupling123!"
        }
        
        url_reg =f"{BASE_URL}/auth/registration"
        requests.post(url_reg, headers=headers, data=json.dumps(data_reg))
        response = requests.post(url, headers=headers, data=json.dumps(data))

        self.assertEqual(200, response.status_code)
        response_json = response.json()
        self.assertIn("message", response_json)
        self.assertIn("отправлено", response_json["message"])


if __name__ == "__main__":
    unittest.main()