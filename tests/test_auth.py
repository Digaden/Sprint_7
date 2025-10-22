import allure
import pytest
from urls import COURIER_LOGIN_URL

class TestCourierAuth:
    @allure.feature("Courier authentication")
    @allure.title("Login success: возвращает id")
    @allure.story("Courier login success")
    def test_login_success(self, client, ensure_courier_exists_and_login):
        login, password = ensure_courier_exists_and_login
        with allure.step("Send login request with valid credentials"):
            resp = client.post(COURIER_LOGIN_URL, data={"login": login, "password": password})
        with allure.step("Validate response"):
            assert resp.status_code == 200
            data = resp.json()
            assert "id" in data

    @allure.feature("Courier authentication")
    @allure.title("Login missing fields: корректная обработка 400/422 и тела ответа")
    @allure.story("Courier login missing fields")
    @pytest.mark.parametrize("payload", [
        {"login": "someuser"},   # отсутствует пароль
        {"password": "password"},  # отсутствует логин
        {},                        # оба поля отсутствуют
    ])
    def test_login_missing_fields(self, client, payload):
        with allure.step(f"Send login request with payload={payload}"):
            resp = client.post(COURIER_LOGIN_URL, data=payload)
        with allure.step("Validate error response"):
            assert resp.status_code in (400, 422)
            try:
                body = resp.json()
                message_text = body.get("message", "")
                assert isinstance(message_text, str) and message_text.strip()
            except ValueError:
                pytest.fail("Expected JSON с полем 'message' в ответе об ошибке")

    @allure.feature("Courier authentication")
    @allure.title("Login wrong credentials: корректная обработка тела ответа")
    @allure.story("Courier login wrong credentials")
    def test_login_wrong_credentials(self, client, ensure_courier_exists_and_login):
        login, password = ensure_courier_exists_and_login
        wrong_password = password + "X"
        with allure.step("Send login request with wrong credentials"):
            resp = client.post(COURIER_LOGIN_URL, data={"login": login, "password": wrong_password})
        with allure.step("Validate error response"):
            assert resp.status_code in (400, 401, 403, 404)
            try:
                body = resp.json()
                message_text = body.get("message", "")
                assert isinstance(message_text, str) and message_text.strip()
            except ValueError:
                pytest.fail("Expected JSON с полем 'message' в ответе об ошибке")