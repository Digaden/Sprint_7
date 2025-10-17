import allure
import pytest
import requests
from conftest import BASE_URL, register_new_courier_and_return_login_password

@allure.feature("Courier authentication")
@allure.story("Courier login success")
def test_login_success():
    login_pass = register_new_courier_and_return_login_password()
    assert login_pass is not None and len(login_pass) == 3
    login, password, _ = login_pass

    resp = requests.post(f"{BASE_URL}/courier/login", data={"login": login, "password": password})
    assert resp.status_code == 200, f"Ожидалось 200, получено {resp.status_code}"
    data = resp.json()
    assert "id" in data

@allure.feature("Courier authentication")
@allure.story("Courier login missing fields")
def test_login_missing_fields():
    resp = requests.post(f"{BASE_URL}/courier/login", data={"login": "someuser"})
    assert resp.status_code in (400, 422), f"Ожидалась ошибка 400/422, получено {resp.status_code}"

@allure.feature("Courier authentication")
@allure.story("Courier login wrong credentials")
def test_login_wrong_credentials():
    login_pass = register_new_courier_and_return_login_password()
    if not login_pass:
        pytest.skip("Не удалось зарегистрировать курьера для теста.")
    login, wrong_password, _ = login_pass
    wrong_password = wrong_password + "X"
    resp = requests.post(f"{BASE_URL}/courier/login", data={"login": login, "password": wrong_password})
    assert resp.status_code in (400, 401, 403, 404), f"Ожидалась ошибка 4xx, получено {resp.status_code}"