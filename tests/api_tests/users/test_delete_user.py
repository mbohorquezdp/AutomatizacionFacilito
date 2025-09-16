from utils.api_helpers import api_request
from config.settings import BASE_URL_API, USERS

def _join(b, p):  # une URLs sin duplicar/omitir '/'
    return f"{b.rstrip('/')}/{p.lstrip('/')}"

def delete_user(uid: str | int, auth_headers: dict, *, timeout: int = 10) -> None:
    url = _join(_join(BASE_URL_API, USERS), str(uid))
    r = api_request("DELETE", url, headers=auth_headers, timeout=timeout)
    assert r.status_code == 204

def test_borrar_un_usuario(auth_headers):
        delete_user("usr-17fd7871", auth_headers)  # reemplaza por el id real