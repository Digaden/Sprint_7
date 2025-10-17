import allure
import pytest
import requests
from conftest import BASE_URL, register_new_courier_and_return_login_password

@allure.feature("Courier management")
@allure.story("Create courier")
def test_create_courier_success():
    login_pass = register_new_courier_and_return_login_password()
    assert login_pass is not None and len(login_pass) == 3
    login, password, firstName = login_pass

    payload = {
        "login": login,
        "password": password,
        "firstName": firstName
    }

    resp = requests.post(f"{BASE_URL}/courier", data=payload)
    assert resp.status_code == 201, f"Oжидался код 201, получен {resp.status_code}"
    data = resp.json()
    assert data.get("ok") is True

@allure.feature("Courier management")
@allure.story("Create courier")
def test_create_duplicate_courier():
    login_pass = register_new_courier_and_return_login_password()
    assert login_pass is not None and len(login_pass) == 3
    login, password, firstName = login_pass

    payload = {
        "login": login,
        "password": password,
        "firstName": firstName
    }
    resp = requests.post(f"{BASE_URL}/courier", data=payload)
    assert resp.status_code in (400, 409), f"Ожидалась ошибка дубликата (400/409), получено {resp.status_code}"

@allure.feature("Courier management")
@allure.story("Create courier")
def test_create_courier_missing_fields():
    # отсутствуют обязательные поля
    payloads = [
        {"password": "pass12345", "firstName": "John"},  # без login
        {"login": "user12345", "firstName": "John"},    # без password
        {"login": "user12345", "password": "pass12345"}  # без firstName
    ]
    for payload in payloads:
        resp = requests.post(f"{BASE_URL}/courier", data=payload)
        assert resp.status_code == 400, f"Ожидалась 400, получено {resp.status_code}"