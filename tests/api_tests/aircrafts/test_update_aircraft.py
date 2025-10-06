# tests/api_tests/aircrafts/test_update_aircraft.py
import uuid
import random
import pytest
from utils.api_helpers import ApiClient
import config.settings as config

# --------- payload builders ----------
def payload_valido(current_body: dict | None = None) -> dict:
    return {
        # tail_number puede cambiarse si la API lo permite; si prefieres mantener, usa current_body["tail_number"]
        "tail_number": f"{random.randint(0, 99999):05d}",
        "model": f"MODEL-{uuid.uuid4().hex[:5].upper()}",
        "capacity": random.randint(1, 300),
    }

def payload_invalido_422(current_body: dict | None = None) -> dict:
    return {
        "tail_number": "",        # inválido
        "model": "",              # inválido
        "capacity": -5,           # inválido
    }

# --------- helpers ----------
def _create_aircraft(api_client: ApiClient) -> dict:
    payload = {
        "tail_number": f"{random.randint(0, 99999):05d}",
        "model": "XXXX",
        "capacity": 1,
    }
    r = api_client.post(config.AIRCRAFTS, json=payload)
    assert r.status_code in (200, 201), f"Setup de aircraft falló: {r.status_code} {r.text}"
    body = r.json()
    assert body.get("id"), f"Setup sin id: {body}"
    return body

def _delete_if_exists(api_client: ApiClient, aircraft_id: str):
    """Cleanup tolerante: intenta DELETE y no rompe la suite si falla."""
    try:
        d = api_client.delete(f"{config.AIRCRAFTS}/{aircraft_id}")
        assert d.status_code in (200, 204, 404, 405), f"Cleanup DELETE: {d.status_code} {d.text}"
    except Exception:
        pass

# --------- casos ----------
# name,          id_source,      builder,               expected_any
CASES = [
    ("ok-auth UPDATE 200",       "create",     payload_valido,        (200, 204)),
    ("not-found-404 INVALIDO", "nonexist",   payload_valido,        (404,)),
    ("invalid-422",   "create",     payload_invalido_422,  (422,)),
]
IDS = [name for name, *_ in CASES]

@pytest.mark.parametrize("name,id_source,payload_builder,expected_any", CASES, ids=IDS)
def test_update_aircraft_variantes(api_client: ApiClient, admin_token: str,
                                   name: str, id_source: str,
                                   payload_builder, expected_any: tuple[int, ...]):
    # preparar ID según el caso
    created = None
    current_body = None
    if id_source == "create":
        created = _create_aircraft(api_client)
        aircraft_id = created["id"]
        current_body = created
    elif id_source == "nonexist":
        aircraft_id = "acf-" + uuid.uuid4().hex[:8]   # casi seguro no existe
    else:
        pytest.fail(f"id_source desconocido: {id_source}")

    # ejecutar PUT
    payload = payload_builder(current_body)
    resp = api_client.put(f"{config.AIRCRAFTS}/{aircraft_id}", json=payload)

    # validar código de estado
    assert resp.status_code in expected_any, (
        f"[{name}] Esperado {expected_any}, recibido {resp.status_code}: {resp.text}"
    )

    # validaciones mínimas si fue 200
    if resp.status_code == 200:
        body = resp.json()
        assert isinstance(body, dict) and body, f"[{name}] Body vacío/no JSON en 200"

        assert "id" in body and body["id"], f"[{name}] 'id' no presente en respuesta 200"
        assert "tail_number" in body, f"[{name}] 'tail_number' no presente en 200"
        assert "model" in body, f"[{name}] 'model' no presente en 200"
        assert "capacity" in body, f"[{name}] 'capacity' no presente en 200"

    # cleanup si se creó
    if created:
        _delete_if_exists(api_client, created["id"])
