import allure
import requests

from curl import LOGIN_USER
from data import ExpectedResponses
from generation import Generation

@allure.feature("Авторизация пользователя")
class TestLogin:

    @allure.title("Успешный вход зарегистрированного пользователя")
    def test_login_existing_user(self, create_user):
        email, password, user_name = create_user

        payload = {
            "email": email,
            "password": password
        }

        response_login = requests.post(LOGIN_USER, json=payload)

        assert response_login.status_code == 200
        assert response_login.json()["user"]["email"] == email
        assert response_login.json()["user"]["name"] == user_name

    @allure.title("Попытка входа с неверным логином и паролем")
    def test_login_with_invalid_credentials(self):
        payload = {
            "email": Generation.email(),
            "password": Generation.password()
        }

        response = requests.post(LOGIN_USER, json=payload)

        assert response.status_code == 401
        assert response.json() == ExpectedResponses.INVALID_CREDENTIALS
