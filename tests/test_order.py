import allure
import pytest
import requests
from urls import BASE_URL
from helpers import build_order_payload

class TestOrderManagement:
    @allure.feature("Order management")
    @allure.story("Create order with various colors")
    @pytest.mark.parametrize("colors", [None, ["BLACK"], ["GREY"], ["BLACK", "GREY"]])
    @allure.title("Create order with colors: None, BLACK, GREY, BLACK+GREY")
    def test_create_order_param_colors(self, client, ensure_courier_exists_and_login, colors):
        payload = build_order_payload(colors)
        with allure.step("Send order creation request"):
            resp = client.post(f"{BASE_URL}/orders", data=payload)

        with allure.step("Validate order creation"):
            assert resp.status_code in (200, 201)
            data = resp.json()
            assert "track" in data or ("order" in data and "track" in data.get("order", {}))

    @allure.feature("Order management")
    @allure.story("List orders")
    @allure.title("List orders returns a list")
    def test_list_orders(self, client, ensure_courier_exists_and_login):
        with allure.step("Request list of orders"):
            resp = client.get(f"{BASE_URL}/orders")
        with allure.step("Validate list of orders"):
            assert resp.status_code == 200
            orders = resp.json()
            assert isinstance(orders, list)