import allure
import requests

from curl import LOGIN_USER
from data import ExpectedResponses
from generation import Generation


@allure.feature("Авторизация пользователя")
class TestLogin:

    @allure.title("Успешный вход зарегистрированного пользователя")
    def test_login_existing_user(self, create_user):
        email, password, user_name, response = create_user

        payload = {
            "email": email,
            "password": password
        }

        with allure.step("Отправляем POST-запрос на вход пользователя"):
            response_login = requests.post(LOGIN_USER, json=payload)

        with allure.step("Проверяем статус-код ответа"):
            assert response_login.status_code == 200

        with allure.step("Проверяем данные пользователя в ответе"):
            res_json = response_login.json()
            assert res_json["user"]["email"] == email
            assert res_json["user"]["name"] == user_name

    @allure.title("Попытка входа с неверным логином и паролем")
    def test_login_with_invalid_credentials(self):
        payload = {
            "email": Generation.email(),
            "password": Generation.password()
        }

        with allure.step("Отправляем POST-запрос с неверными данными"):
            response = requests.post(LOGIN_USER, json=payload)

        with allure.step("Проверяем статус-код ответа"):
            assert response.status_code == 401

        with allure.step("Проверяем тело ответа"):
            assert response.json() == ExpectedResponses.INVALID_CREDENTIALS
