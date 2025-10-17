import allure
import pytest
import requests
from conftest import BASE_URL

def build_order_payload(colors=None):
    payload = [
        ("firstName", "Test"),
        ("lastName", "User"),
        ("address", "Test address"),
        ("metroStation", "1"),
        ("phone", "+79000000000"),
        ("deliveryDate", "2025-12-01"),
        ("rentTime", "5"),
    ]
    if colors is not None:
        for c in colors:
            payload.append(("color", c))
    return payload

@allure.feature("Order management")
@allure.story("Create order with various colors")
@pytest.mark.parametrize("colors", [None, ["BLACK"], ["GREY"], ["BLACK", "GREY"]])
def test_create_order_param_colors(colors, requests_session=None):
    sess = requests_session or requests.Session()

    payload = build_order_payload(colors)
    resp = sess.post(f"{BASE_URL}/orders", data=payload)

    if resp.status_code in (401, 403):
        from conftest import register_new_courier_and_return_login_password
        login_pass = register_new_courier_and_return_login_password()
        if login_pass:
            login, password, _ = login_pass
            login_resp = sess.post(f"{BASE_URL}/courier/login", data={"login": login, "password": password})
            assert login_resp.status_code == 200
            resp = sess.post(f"{BASE_URL}/orders", data=payload)

    assert resp.status_code in (200, 201), f"Ожидался 200/201, получено {resp.status_code}"
    data = resp.json()
    assert "track" in data or ("order" in data and "track" in data["order"])

@allure.feature("Order management")
@allure.story("List orders")
def test_list_orders():
    resp = requests.get(f"{BASE_URL}/orders")
    assert resp.status_code == 200, f"Ожидался 200, получено {resp.status_code}"
    orders = resp.json()
    assert isinstance(orders, list)