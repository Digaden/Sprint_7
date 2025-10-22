import random
import string
import requests
from urls import COURIER_URL  # точка создания курьера

def _generate_random_string(length: int = 10) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def register_new_courier_and_return_login_password(base_url: str = COURIER_URL):
    login = _generate_random_string(10)
    password = _generate_random_string(10)
    first_name = _generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(base_url, data=payload)
    if response.status_code == 201:
        return login, password, first_name
    return None

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