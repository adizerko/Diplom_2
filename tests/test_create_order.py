import allure
import requests

from curl import CREATE_ORDER
from data import Payloads, ExpectedResponses


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_ingredients(self, login):
        access_token, email, user_name = login
        headers = {"Authorization": access_token}

        with allure.step("Отправляем POST-запрос на создание заказа"):
            response = requests.post(
                CREATE_ORDER,
                json=Payloads.with_ingredients,
                headers=headers
            )

        with allure.step("Проверяем статус-код ответа"):
            assert response.status_code == 200
        response_json = response.json()

        with allure.step("Проверяем, что 'success' = True"):
            assert response_json.get("success") is True

        with allure.step("Проверяем, что есть ключ 'name'"):
            assert "name" in response_json

        with allure.step("Проверяем, что есть ключ 'order'"):
            assert "order" in response_json

        with allure.step("Проверяем, что 'order.number' это число"):
            assert isinstance(response_json["order"]["number"], int)

    @allure.title("Создание заказа с авторизацией, но без ингредиентов")
    def test_create_order_auth_without_ingredients(self, login):
        access_token, email, user_name = login
        headers = {"Authorization": access_token}

        with allure.step("Отправляем POST-запрос на создание заказа"):
            response = requests.post(
                CREATE_ORDER,
                json=Payloads.without_ingredients,
                headers=headers
            )

        with allure.step("Проверяем статус-код ответа"):
            assert response.status_code == 400

        response_json = response.json()

        with allure.step(
                "Проверяем, что тело ответа соответствует ожиданиям при отсутствии ингредиентов"):
            assert response_json == ExpectedResponses.WITHOUT_INGREDIENTS

    @allure.title("Создание заказа с авторизацией, но с неверным хешем ингредиентов")
    def test_create_order_auth_with_invalid_hash_ingredients(self, login):
        access_token, email, user_name = login
        headers = {"Authorization": access_token}

        with allure.step("Отправляем POST-запрос на создание заказа"):
            response = requests.post(
                CREATE_ORDER,
                json=Payloads.invalid_hash_ingredients,
                headers=headers
            )

        with allure.step("Проверяем статус-код ответа"):
            assert response.status_code == 500


    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        with allure.step("Отправляем POST-запрос на создание заказа без авторизации"):
            response = requests.post(CREATE_ORDER, json=Payloads.with_ingredients)

        with allure.step("Проверяем статус-код ответа"):
            assert response.status_code == 401

        response_json = response.json()

        with allure.step("Проверяем, что success равен False"):
            assert response_json.get("success") is False

        with allure.step("Проверяем, что 'name' отсутствует в ответе"):
            assert "name" not in response_json

        with allure.step("Проверяем, что 'order' отсутствует в ответе"):
            assert "order" not in response_json
