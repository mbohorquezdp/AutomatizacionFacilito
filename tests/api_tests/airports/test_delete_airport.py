
from utils.api_helpers import api_request
from config.settings import BASE_URL_API, AIRPORT

def _join(b, p):  # une URLs sin duplicar/omitir '/'
    return f"{b.rstrip('/')}/{p.lstrip('/')}"

def delete_airport(uid: str | int, auth_headers: dict, *, timeout: int = 10) -> None:
    url = _join(_join(BASE_URL_API, AIRPORT), str(uid))
    r = api_request("DELETE", url, headers=auth_headers, timeout=timeout)
    assert r.status_code  == 204

def test_borrar_un_airport(auth_headers):
    delete_airport("ÑÑÑ", auth_headers)  # reemplaza por el id real






