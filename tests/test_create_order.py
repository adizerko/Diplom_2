import allure
import pytest
import requests

from curl import CREATE_ORDER
from data import Payloads

@allure.feature("Создание заказа")
class TestCreateOrder:

    @pytest.mark.parametrize(
        "payloads, status_code",
        [(Payloads.with_ingredients, 200),
         (Payloads.without_ingredients, 400, ),
         (Payloads.invalid_hash_ingredients, 500)])
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, login, payloads, status_code):
        access_token, email, user_name = login
        headers = {"Authorization":access_token}

        response = requests.post(
            CREATE_ORDER, json=payloads, headers=headers)

        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "payloads, status_code",
        [(Payloads.with_ingredients, 200),
         (Payloads.without_ingredients, 400,),
         (Payloads.invalid_hash_ingredients, 500)])
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, payloads, status_code):
        response = requests.post(CREATE_ORDER, json=payloads)
        assert response.status_code == status_code
