import pytest
import requests
from helpers import register_new_courier_and_return_login_password

@pytest.fixture
def client():
    return requests.Session()

@pytest.fixture
def courier_credentials_factory():
    def _factory():
        login_pass = register_new_courier_and_return_login_password()
        if not login_pass:
            return None
        return login_pass  # (login, password, firstName)
    return _factory