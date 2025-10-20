import allure
import pytest
import requests
from urls import BASE_URL
from helpers import build_order_payload

class TestOrderManagement:
    @allure.feature("Order management")
    @allure.story("Create order with various colors")
    @pytest.mark.parametrize("colors", [None, ["BLACK"], ["GREY"], ["BLACK", "GREY"]])
    def test_create_order_param_colors(self, client, ensure_courier_exists_and_login, colors):
        payload = build_order_payload(colors)
        resp = client.post(f"{BASE_URL}/orders", data=payload)

        assert resp.status_code in (200, 201), f"Ожидался 200/201, получено {resp.status_code}"
        data = resp.json()
        assert "track" in data or ("order" in data and "track" in data.get("order", {}))

    @allure.feature("Order management")
    @allure.story("List orders")
    def test_list_orders(self, client, ensure_courier_exists_and_login):
        resp = client.get(f"{BASE_URL}/orders")
        assert resp.status_code == 200
        orders = resp.json()
        assert isinstance(orders, list)