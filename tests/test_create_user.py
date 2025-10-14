import allure
import pytest
import requests

from curl import CREATE_USER
from data import ExpectedResponses, Payloads
from generation import Generation

@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание нового уникального пользователя")
    def test_create_unique_user(self, delete_user):
        payload = {
                "email": Generation.email(),
                "password": Generation.password(),
                "name": Generation.user_name()
        }

        response = requests.post(CREATE_USER, json=payload)

        assert response.status_code == 200
        assert response.json()["success"] is True

        access_token = response.json()["accessToken"]
        delete_user(access_token)

    @allure.title("Попытка регистрации пользователя, который уже существует")
    def test_register_existing_user(self, delete_user):
        email = Generation.email()
        password = Generation.password()
        user_name = Generation.user_name()

        payload = {
                "email": email,
                "password": password,
                "name": user_name
        }

        response = requests.post(CREATE_USER, json=payload)
        assert response.status_code == 200
        assert response.json()["success"] is True

        response_repeated = requests.post(CREATE_USER, json=payload)
        assert response_repeated.status_code == 403
        assert response_repeated.json() == ExpectedResponses.EXISTING_USER

        access_token = response.json()["accessToken"]
        delete_user(access_token)


    @pytest.mark.parametrize(
        "payload",
        [Payloads.missing_user_name, Payloads.missing_password, Payloads.missing_email])
    @allure.title("Создание пользователя без обязательного поля")
    def test_create_user_without_required_field(self, payload):
        response = requests.post(CREATE_USER, json=payload)

        assert response.status_code == 403
        assert response.json() == ExpectedResponses.RESPONSE_MISSING_FIELD
