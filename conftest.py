import pytest
import requests
from urls import COURIER_LOGIN_URL
from helpers import register_new_courier_and_return_login_password

@pytest.fixture
def client():
    return requests.Session()

@pytest.fixture
def ensure_courier_exists_and_login(client):
    login_pass = register_new_courier_and_return_login_password()
    if not login_pass:
        pytest.skip("Не удалось зарегистрировать нового курьера для теста авторизации.")
    login, password, _firstName = login_pass
    return login, password