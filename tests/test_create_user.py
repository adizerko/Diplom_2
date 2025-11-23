import allure
import pytest
import requests

from conftest import create_user
from curl import CREATE_USER
from data import ExpectedResponses, Payloads


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание нового уникального пользователя")
    def test_create_unique_user(self, create_user):
        with allure.step("Создаём нового пользователя через API"):
            email, password, name, response = create_user

        with allure.step("Проверяем статус-код ответа"):
            assert response.status_code == 200

        res_json = response.json()

        with allure.step("Проверяем успех операции"):
            assert res_json["success"] is True

        with allure.step("Проверяем данные пользователя"):
            assert res_json["user"]["email"] == email
            assert res_json["user"]["name"] == name

        with allure.step("Проверяем наличие токенов"):
            assert "accessToken" in res_json
            assert "refreshToken" in res_json

    @allure.title("Попытка регистрации пользователя, который уже существует")
    def test_register_existing_user(self, create_user):
        email, password, user_name, response = create_user

        payload = {
            "email": email,
            "password": password,
            "name": user_name
        }

        with allure.step("Отправляем POST-запрос на регистрацию уже существующего пользователя"):
            response_repeated = requests.post(CREATE_USER, json=payload)

        with allure.step("Проверяем статус-код ответа"):
            assert response_repeated.status_code == 403

        with allure.step("Проверяем тело ответа"):
            assert response_repeated.json() == ExpectedResponses.EXISTING_USER

    @pytest.mark.parametrize(
        "payload",
        [Payloads.missing_user_name, Payloads.missing_password, Payloads.missing_email])
    @allure.title("Создание пользователя без обязательного поля")
    def test_create_user_without_required_field(self, payload):
        with allure.step("Отправляем POST-запрос на создание пользователя с неполными данными"):
            response = requests.post(CREATE_USER, json=payload)

        with allure.step("Проверяем статус-код ответа"):
            assert response.status_code == 403

        with allure.step("Проверяем тело ответа"):
            assert response.json() == ExpectedResponses.RESPONSE_MISSING_FIELD
