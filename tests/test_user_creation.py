import pytest
import allure
import requests
from curl import *
from functions import *
from data_for_tests import *

class TestUserCreation:
    
    @allure.title("Успешное создание нового пользователя")
    @allure.description("Проверяем успешный сценарий создания нового пользователя через API."
                        "Система должна вернуть - Статус‑код ответа: 200 OK, поле `success` в ответе: `true`."
    )
    def test_create_user_success(self, create_new_user_and_return_token_and_data):
        response, _ , _ = create_new_user_and_return_token_and_data

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200
            assert response.json().get("success") is True


    @allure.title("Ошибка при создании пользователя с такими же данными")
    @allure.description("Проверяем обработку дублирования данных при попытке создать пользователя с уже существующими данными."
                        "Система должна вернуть ошибку 403 и сообщение о том, что такой пользователь уже существует: «User already exists»."
    )
    def test_create_user_with_duplicated_data_not_successful(self, create_new_user_and_return_token_and_data):
        _, _, user_data = create_new_user_and_return_token_and_data

        payload = {"email": user_data["email"], "password": user_data["password"], "name": user_data["name"]}

        with allure.step("Повторное создание пользователя"):
            response = requests.post(CREATE_USER_ENDPOINT, json=payload)

        with allure.step("Проверка появления ошибки"):
            assert response.status_code == 403
            assert response.json().get("success") is False
            assert response.json().get("message") == USER_DUPLICATION_MESSAGE

    @pytest.mark.parametrize("empty_field", ["email", "password", "name"])
    @allure.title("Создание пользователя без обязательного поля {empty_field}")
    @allure.description(
        "Проверяем обработку отсутствующих обязательных полей при создании пользователя. "
        "Система должна возвращать ошибку 403 и сообщение о недостаточных данных: «Email, password and name are required fields»"
    )
    def test_create_user_with_empty_field(self, empty_field):
        data = new_user_data()
        data.pop(empty_field)
        
        with allure.step(f"Пробуем зарегистрировать пользователя без поля: {empty_field}"):
            response = requests.post(CREATE_USER_ENDPOINT, data=data)

        with allure.step("Проверка появления ошибки"):
            assert response.status_code == 403
            assert response.json().get("success") is False
            assert response.json().get("message") == EMPTY_FIELD_MESSAGE
