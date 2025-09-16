from utils.api_helpers import api_request
from config.settings import BASE_URL_API, USERS
import faker

fake = faker.Faker()

def _join(b, p):
    return f"{b.rstrip('/')}/{p.lstrip('/')}"

def put_user(uid: str | int, auth_headers: dict, *, timeout: int = 10) -> None:
    # Si tu API requiere todos los campos en PUT, agrega 'role'
    user_data = {
        "email": fake.email(),
        "password": fake.password(),
        "full_name": fake.name(),
        "role": "passenger",   # <-- incluye los obligatorios para PUT
    }

    url = _join(_join(BASE_URL_API, USERS), str(uid))
    r = api_request("PUT", url, headers=auth_headers, json=user_data, timeout=timeout)

    # Acepta 200 (body) o 204 (sin contenido)
    assert r.status_code == 200, f"PUT {url} → {r.status_code}\n{r.text}"

    # Si fue 200, puedes validar el body
    if r.status_code == 200:
        body = r.json()
        assert body.get("full_name"), "full_name no volvió en la respuesta"

def test_put_un_usuario(auth_headers):
    put_user("usr-9ec36590", auth_headers)  # usa un id real

