import random
import string
import requests
import pytest

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

def _generate_random_string(length: int = 10) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def register_new_courier_and_return_login_password():
    login = _generate_random_string(10)
    password = _generate_random_string(10)
    first_name = _generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f"{BASE_URL}/courier", data=payload)
    if response.status_code == 201:
        return login, password, first_name
    return None

@pytest.fixture
def client():
    return requests.Session()

@pytest.fixture
def ensure_courier_exists_and_login(client):
    login_pass = register_new_courier_and_return_login_password()
    if not login_pass:
        pytest.skip("Не удалось зарегистрировать нового курьера для теста авторизации.")
    login, password, _ = login_pass
    login_resp = client.post(f"{BASE_URL}/courier/login", data={"login": login, "password": password})
    assert login_resp.status_code == 200
    return login, password