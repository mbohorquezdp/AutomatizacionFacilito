import requests
from config.settings import BASE_URL_API,USERS
from utils.api_helpers import api_request


def test_list_users(auth_headers,limit=2):
    skip=0
    results = []

    #r = requests.get(f"{BASE_URL_API}{USERS}",params={"skip":skip,"limit":limit},headers=auth_headers,timeout=10)
    r = api_request(
        "GET",
        BASE_URL_API + USERS,
        params={"skip": skip, "limit": limit},
        headers=auth_headers,
        timeout=10,  # opcional
    )
    lista = r.text
    assert r.status_code == 200
    assert r.text != ""








