import uuid
import pytest
from utils.api_helpers import api_request
from config.settings import BASE_URL_API, USERS
from utils.data_loader import USUARIOS

#Pruebas STATUS CODE 201,422
#Pruebas TIPOS DE DATOS
#Pruebas Entradas validas y extremas

def _join(b, p):  # une URLs sin duplicar/omitir '/'
    return f"{b.rstrip('/')}/{p.lstrip('/')}"

@pytest.mark.parametrize("caso", USUARIOS, ids=["user1","user2","user3"])
def test_crear_usuario(caso, auth_headers):
    payload = {**caso}
    url = _join(BASE_URL_API, USERS)

    r = api_request("POST", BASE_URL_API + USERS, json=payload, headers=auth_headers, timeout=10)
    assert r.status_code == 201, f"POST {url} → {r.status_code}\n{r.text}"
    body = r.json()

    #Pruebas TIPOS DE DATOS
    email = body.get("email")
    assert isinstance(email, str), "email debe ser string"
    assert email.strip(), "email vacío o solo espacios"

    full_name = body.get("full_name")
    assert isinstance(full_name, str), "full_name debe ser string"
    assert full_name.strip(), "full_name vacío o solo espacios"

    role = body.get("role")
    assert isinstance(role, str), "role debe ser string"
    assert role.strip(), "role vacío o solo espacios"

    uid = body.get("id") or body.get("_id")
    assert uid not in (None, ""), f"Respuesta sin id: {body}"



    # Eliminar
    api_request("DELETE", _join(url, str(uid)), headers=auth_headers, timeout=10)





