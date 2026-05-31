import allure
import requests
from curl import *
from functions import *
from data_for_tests import *

class TestOrderCreation:

    @allure.title("Создание заказа автторизованным пользователем и ингридиентами")
    @allure.description("Проверяем успешный сценарий создания заказа авторизованным пользователем с указанием ингредиентов."
                    "Система должна вернуть: Статус‑код ответа: 200 OK, поле `success` в ответе: `true`."
)
    def test_create_order_with_auth_success(self, create_new_user_and_return_token_and_data):
        _, token, _ = create_new_user_and_return_token_and_data

        with allure.step("Создаем заказ авторизованным пользователем"):
            response = requests.post(CREATE_ORDER_ENDPOINT, json={"ingredients": INGREDIENTS_HASH}, headers={"Authorization": token})

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200
            assert response.json().get("success") is True
            assert "order" in response.json()

    @allure.title("Создание заказа с ингридиентами, но без авторизации пользователя")
    @allure.description("Проверяем обработку попытки создания заказа с ингредиентами без авторизации."
                    "Система должна вернуть: Статус‑код ответа: 200 OK, поле `success` в ответе: `true`."
)
    def test_create_order_without_auth_failed(self):

        with allure.step("Создаем заказ без авторизации пользователя"):
            response = requests.post(CREATE_ORDER_ENDPOINT, json={"ingredients": INGREDIENTS_HASH})
            
        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200
            assert response.json().get("success") is True
            assert "order" in response.json()

    @allure.title("Появление ошибки при создании заказа без ингридиентов")
    @allure.description("Проверяем обработку попытки создания заказа без указания ингредиентов."
                    "Система должна вернуть: Статус‑код ответа: 400 Bad Request, поле `success` в ответе: `false`, сообщение: «Ingredient ids must be provided»."
)
    def test_create_order_without_ingredients_failed(self):

        with allure.step("Создаем заказ без авторизации пользователя"):
            response = requests.post(CREATE_ORDER_ENDPOINT, json={})
            
        with allure.step("Проверка корректного ответа"):
            assert response.status_code == 400
            assert response.json().get("success") is False
            assert response.json().get("message") == EMPTY_INGREDIENT_INPUT_MESSAGE

    @allure.title("Появление ошибки при создании заказа с неверным хешем ингридиента")
    @allure.description("Проверяем обработку попытки создания заказа с некорректным хешем ингредиента."
                    "Система должна вернуть: Статус‑код ответа: 500 Internal Server Error."
)
    def test_create_order_with_invalid_hash_ingredients(self):

        with allure.step("Создаем заказ без авторизации пользователя"):
            response = requests.post(CREATE_ORDER_ENDPOINT, json={"ingredients":['wrong_hash1']})
            
        with allure.step("Проверка корректного ответа"):
            assert response.status_code == 500