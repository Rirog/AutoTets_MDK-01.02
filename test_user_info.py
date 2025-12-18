import unittest
import requests
import json

BASE_URL = "http://localhost:8080/api/v1"


class UserInfoTests(unittest.TestCase):
    """Тесты для endpoint'ов информации о пользователе"""

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

    def test_get_user_profile_info(self):
        """Тест получения информации о профиле"""
        url = f"{BASE_URL}/user/info/profile"
        response = requests.get(url, headers=self.user_headers)
        self.assertEqual(200, response.status_code)
        
        response_json = response.json()
        self.assertIn("id", response_json)
        self.assertIn("username", response_json)
        self.assertIn("email", response_json)

    def test_get_user_role(self):
        """Тест получения роли пользователя"""
        url = f"{BASE_URL}/user/info/role"
        response = requests.get(url, headers=self.user_headers)
        self.assertEqual(200, response.status_code)
        
        response_json = response.json()
        self.assertIn("role", response_json)

    def test_get_all_sessions(self):
        """Тест получения всех сеансов пользователя"""
        url = f"{BASE_URL}/user/info/sessions"
        response = requests.get(url, headers=self.user_headers)
        self.assertEqual(200, response.status_code)
        
        response_json = response.json()
        self.assertIn("currentSession", response_json)
        self.assertIn("otherSessions", response_json)

        UserInfoTests.sessions_data = response_json

    def test_revoke_all_sessions(self):
        """Тест завершения всех сеансов, кроме текущего"""
        url = f"{BASE_URL}/user/info/sessions/revoke/all"
        response = requests.delete(url, headers=self.user_headers)
        self.assertEqual(200, response.status_code)

    def test_get_avatar(self):
        """Тест получения аватара профиля"""
        url = f"{BASE_URL}/user/info/avatar"
        response = requests.get(url, headers=self.user_headers)
        
        self.assertIn(response.status_code, [200, 404, 204])
            
    def test_revoke_other_session_after_creating_new_session(self):
        """Тест: создаем новую сессию и пытаемся её удалить"""
        login_url = f"{BASE_URL}/auth/login"
        data = {"login": "admin", "password": "Admin123!"}
        login_response = requests.post(login_url, headers=self.user_headers, data=json.dumps(data))
        
        if login_response.status_code == 200:
            sessions_url = f"{BASE_URL}/user/info/sessions"
            sessions_response = requests.get(sessions_url, headers=self.user_headers)
            
            if sessions_response.status_code == 200:
                sessions_data = sessions_response.json()

                if isinstance(sessions_data["otherSessions"], list) and len(sessions_data["otherSessions"]) > 0:
                    other_session = sessions_data["otherSessions"][-1]
                    session_id = other_session.get("id")
                    
                    if session_id:
                        revoke_url = f"{BASE_URL}/user/info/sessions/revoke"
                        params = {"sessionId": session_id}
                        revoke_response = requests.delete(revoke_url, headers=self.user_headers, params=params)

                        self.assertIn(revoke_response.status_code, [200, 403, 409])


if __name__ == "__main__":
    unittest.main()