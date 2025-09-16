from config.settings import BASE_URL_API,USERS_ME
from utils.api_helpers import api_request


def test_me(auth_headers):
    r = api_request(
        "GET",
        BASE_URL_API + USERS_ME,
        headers=auth_headers,
        timeout=10,  # opcional
    )
    assert r.status_code == 200
    assert r.text != ""

