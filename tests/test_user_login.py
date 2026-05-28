import allure
from curl import *
from functions import *
from data_for_tests import *

class TestUserLogin:
      
    @allure.title("Вход с верным логином и паролем")
    @allure.description("Проверяем успешный сценарий авторизации существующего пользователя."
                        "Система должна вернуть - Статус‑код ответа: 200 OK, поле `success` в ответе: `true`."
    )
    def test_login_existing_user(self, create_new_user_and_return_token_and_data):
        _, _, user_data = create_new_user_and_return_token_and_data
        payload = {"email": user_data["email"], "password": user_data["password"]}

        with allure.step("Логинимся пользователем"):
            response = requests.post(LOGIN_USER_ENDPOINT, json=payload)

        with allure.step("Проверка неуспешной авторизации"):
            assert response.status_code == 200
            assert response.json().get("success") is True
            assert "accessToken" in response.json()
    
    
    @allure.title("Вход с неверным логином и паролем")
    @allure.description("Проверяем обработку некорректных данных при попытке авторизации."
                        "Система должна вернуть ошибку статус‑код ответа: 401 Unauthorized и сообщение о том, что указын неверный адрес почты или пароль: «email or password are incorrect»."
    )
    def test_login_invalid_email_and_password(self):
        payload = {"email": "test@test.ru", "password": "test_test"}

        with allure.step("Логинимся пользователем с неверными данными"):
            response = requests.post(LOGIN_USER_ENDPOINT, json=payload)

        with allure.step("Проверка неуспешной авторизации"):
            assert response.status_code == 401
            assert response.json()["success"] is False
            assert response.json()["message"] == INCORRECT_FIELD_MESSAGE