import requests
from config.settings import BASE_URL_API,AIRPORT
from utils.api_helpers import api_request


def test_gel_all_airports(airport,auth_headers):
    r = api_request("get", BASE_URL_API + AIRPORT, headers=auth_headers)

    lista = r.text
    assert r.status_code == 200
    assert r.text != ""

