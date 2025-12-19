import sys

class TestOutput:
    """Класс для вывода результатов тестов"""
    
    @staticmethod
    def print_result(test_name, response):
        """Вывод результата теста"""
        print(
            # f"\n{'='*50}" \\ смотри как лучше будут выгледеть
            f"\nТест: {test_name}"
            f"\nСтатус код: {response.status_code}"
            f"\nОтвет: {response.text}"
            # f"\n{'='*50}"
        )