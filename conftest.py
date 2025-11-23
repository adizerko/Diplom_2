import pytest
import requests

from curl import CREATE_USER, LOGIN_USER, DELETE_USER
from data import ExpectedResponses
from generation import Generation


@pytest.fixture
def create_user():
    email = Generation.email()
    password = Generation.password()
    user_name = Generation.user_name()

    payload = {
        "email": email,
        "password": password,
        "name": user_name
    }

    response = requests.post(CREATE_USER, json=payload)
    access_token = response.json()["accessToken"]

    assert response.status_code == 200
    assert response.json()["success"] is True

    yield email, password, user_name, response

    headers = {"Authorization":access_token}
    response_del = requests.delete(DELETE_USER, headers=headers)

    assert response_del.status_code == 202
    assert response_del.json() == ExpectedResponses.SUCCESS_DELETE_USER

@pytest.fixture
def login(create_user):
    email, password, user_name, response = create_user
    payload = {
        "email": email,
        "password": password
    }

    response = requests.post(LOGIN_USER, json=payload)

    assert response.status_code == 200
    assert response.json()["success"] is True

    access_token = response.json().get("accessToken")

    return access_token, email, user_name

@pytest.fixture
def delete_user():
    def delete(access_token):
        headers = {"Authorization":access_token}
        response = requests.delete(DELETE_USER, headers=headers)

        assert response.status_code == 202
        assert response.json() == ExpectedResponses.SUCCESS_DELETE_USER

    yield delete
