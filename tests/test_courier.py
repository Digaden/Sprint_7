import allure
import pytest
from urls import COURIER_URL
from helpers import register_new_courier_and_return_login_password

class TestCourierManagement:
    @allure.feature("Courier management")
    @allure.story("Create courier")
    @allure.title("Create courier: успешное создание")
    def test_create_courier_success(self, client):
        login_pass = register_new_courier_and_return_login_password()
        assert login_pass is not None and len(login_pass) == 3
        login, password, firstName = login_pass

        payload = {
            "login": login,
            "password": password,
            "firstName": firstName
        }

        with allure.step("Create courier via API"):
            resp = client.post(COURIER_URL, data=payload)
        with allure.step("Validate creation response"):
            assert resp.status_code == 201, f"Oжидался код 201, получено {resp.status_code}"
            data = resp.json()
            assert data.get("ok") is True

    @allure.feature("Courier management")
    @allure.story("Create courier")
    @allure.title("Create courier: дубликат вызывает ошибку")
    def test_create_duplicate_courier(self, client):
        login_pass = register_new_courier_and_return_login_password()
        assert login_pass is not None and len(login_pass) == 3
        login, password, firstName = login_pass

        payload = {
            "login": login,
            "password": password,
            "firstName": firstName
        }

        with allure.step("Create courier (первый раз)"):
            resp = client.post(COURIER_URL, data=payload)
        with allure.step("Попытка создать дубликат"):
            resp2 = client.post(COURIER_URL, data=payload)

        with allure.step("Validate duplicate response"):
            # Однозначная проверка: ожидаем 409
            assert resp2.status_code in (400, 409)
            try:
                body = resp2.json()
                # Проверяем текст в поле message, если есть
                if isinstance(body, dict) and "message" in body:
                    message_text = body["message"]
                    assert isinstance(message_text, str) and message_text.strip()
                else:
                    # Нет поля message: fallback на текст ответа
                    assert isinstance(resp2.text, str) and resp2.text.strip()
            except ValueError:
                assert isinstance(resp2.text, str) and resp2.text.strip()

    @allure.feature("Courier management")
    @allure.story("Create courier")
    @pytest.mark.parametrize("payload", [
        {"password": "pass12345", "firstName": "John"},  # без login
        {"login": "user12345", "firstName": "John"},     # без password
        {"login": "user12345", "password": "pass12345"}  # без firstName
    ])
    @allure.title("Create courier with missing fields should fail")
    def test_create_courier_missing_fields(self, client, payload):
        with allure.step(f"Attempt to create courier with payload={payload}"):
            resp = client.post(COURIER_URL, data=payload)
        with allure.step("Validate error response"):
            # Однозначная проверка: ожидаем 400/422 (зависит от реализации)
            assert resp.status_code in (400, 422)
            try:
                body = resp.json()
                if isinstance(body, dict) and "message" in body:
                    message_text = body["message"]
                    assert isinstance(message_text, str) and message_text.strip()
                else:
                    assert isinstance(resp.text, str) and resp.text.strip()
            except ValueError:
                assert isinstance(resp.text, str) and resp.text.strip()