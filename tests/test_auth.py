import allure
import pytest
from urls import COURIER_LOGIN_URL

class TestCourierAuth:
    @allure.feature("Courier authentication")
    @allure.story("Courier login success")
    def test_login_success(self, client, ensure_courier_exists_and_login):
        # ensure_courier_exists_and_login возвращает (login, password)
        login, password = ensure_courier_exists_and_login
        resp = client.post(COURIER_LOGIN_URL, data={"login": login, "password": password})
        assert resp.status_code == 200
        data = resp.json()
        assert "id" in data

    @allure.story("Courier login missing fields")
    @pytest.mark.parametrize("payload", [
        {"login": "someuser"},   # отсутствует пароль
        {"password": "password"},  # отсутствует логин
        {},                        # оба поля отсутствуют
    ])
    def test_login_missing_fields(self, client, payload):
        resp = client.post(COURIER_LOGIN_URL, data=payload)
        assert resp.status_code in (400, 422)

        # Попытка проверить тело ответа, если оно есть
        try:
            body = resp.json()
            assert isinstance(body, dict)
        except ValueError:
            # Если ответ не JSON, проверяем, что есть текст в теле
            assert resp.text

    @allure.story("Courier login wrong credentials")
    def test_login_wrong_credentials(self, client, ensure_courier_exists_and_login):
        login, password = ensure_courier_exists_and_login
        wrong_password = password + "X"
        resp = client.post(COURIER_LOGIN_URL, data={"login": login, "password": wrong_password})
        assert resp.status_code in (400, 401, 403, 404)