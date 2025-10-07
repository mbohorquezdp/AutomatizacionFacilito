import uuid
import pytest
import faker
from utils.api_helpers import ApiClient
from config.settings import USERS

fake = faker.Faker()

#Data Válida 200
def payload_valido() -> dict:
    return {
        "email": f"upd_{uuid.uuid4().hex[:8]}@test.com",
        "password": "Abc123!xyzK",
        "full_name": fake.name(),
        "role": "passenger",
    }
#Data Invalida 422
def payload_invalido_422() -> dict:
    return {
        "email": "correo_invalido",    # fuerza 422
        "password": "Abc123!xyzK",
        "full_name": fake.name(),
        "role": "passenger",
    }

# crea usuario temporal para tener data
def _create_user(api_client: ApiClient) -> dict:
    payload = {
        "email": f"tmp_{uuid.uuid4().hex[:10]}@test.com",
        "password": "Abc123!xyzK",
        "full_name": "Temporal Update",
        "role": "passenger",
    }
    r = api_client.post(USERS, json=payload)
    assert r.status_code == 201, f"Setup de user falló: {r.status_code} {r.text}"
    body = r.json()
    assert body.get("id"), f"Setup sin id: {body}"
    return body

def _delete_if_exists(api_client: ApiClient, user_id: str):
    try:
        d = api_client.delete(f"{USERS}/{user_id}")
        # éxito flexible (muchos backends dan 204)
        assert d.status_code == 201, f"Cleanup DELETE: {d.status_code} {d.text}"
    except Exception:
        pass  # no dejes caer la suite por el cleanup

# --------- casos ----------
# name,       id_source,      construye payload,              expected_any
CASES = [
    ("ok-auth",     "create",     payload_valido,       (200, 204)),
    ("not-found-404","nonexist",  payload_valido,       (404,)),      # ID inexistente
    ("invalid-422", "create",     payload_invalido_422, (422,)),      # sobre user real
]
IDS = [name for name, *_ in CASES]

@pytest.mark.parametrize("name,id_source,payload_builder,expected_any", CASES, ids=IDS)
def test_update_user_variantes(api_client: ApiClient, admin_token: str,
                               name: str, id_source: str,
                               payload_builder, expected_any: tuple[int, ...]):
    # preparar ID según el caso
    created = None
    if id_source == "create":
        created = _create_user(api_client)
        user_id = created["id"]
    elif id_source == "nonexist":
        user_id = "usr-" + uuid.uuid4().hex[:8]  # casi seguro no existe
    else:
        pytest.fail(f"id_source desconocido: {id_source}")

    # ejecutar PUT
    payload = payload_builder()
    resp = api_client.put(f"{USERS}/{user_id}", json=payload)

    # validar
    assert resp.status_code in expected_any, (
        f"[{name}] Esperado {expected_any}, recibido {resp.status_code}: {resp.text}"
    )

    # si fue éxito 200, validar algo mínimo del body
    if resp.status_code == 200:
        body = resp.json()
        assert isinstance(body, dict) and body, f"[{name}] Body vacío/no JSON en 200"
        assert "full_name" in body, f"[{name}] 'full_name' no presente en respuesta 200"

    # cleanup si se creó
    if created:
        _delete_if_exists(api_client, created["id"])



