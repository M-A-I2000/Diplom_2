import allure
import requests
import random
import string
from curl import *

@allure.step('Генерируем строку состоящую из случайных букв')
def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

@allure.step('Генерируем и сохраняем данные для пользователя')
def new_user_data():
    email = f'{generate_random_string(7)}@yandex.ru'
    password = generate_random_string(7)
    name = generate_random_string(7)

    user_data = {
        'email': email,
        'password': password,
        'name': name
    }
    
    return user_data

@allure.step('Удаление пользователя по токену через запрос к API')
def delete_user(token):
    requests.delete(USER_ACTIONS_ENDPOINT, headers={'Authorization': token})

