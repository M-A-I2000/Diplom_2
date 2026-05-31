import pytest
import requests
import allure
from curl import *
from functions import *


@allure.description('Создаем нового пользователя и возвращаем токен')
@pytest.fixture
def create_new_user_and_return_token_and_data():
    payload = new_user_data()
    with allure.step("Создаем пользователя через API запрос"):
        response = requests.post(CREATE_USER_ENDPOINT, json=payload)
        token = response.json().get("accessToken")
        user_data = payload

    yield response, token, user_data
    delete_user(token)