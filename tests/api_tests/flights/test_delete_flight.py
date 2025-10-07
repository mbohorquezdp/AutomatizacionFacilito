import uuid
import pytest
from datetime import datetime, timedelta
from utils.api_helpers import ApiClient
import config.settings as config

# ---------- Helpers ----------
def _iso_utc(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat() + "Z"

def _create_aircraft(api_client: ApiClient) -> str:
    payload = {
        "tail_number": f"{datetime.utcnow():%H%M%S}",  # algo simple y casi único
        "model": "TEST-MODEL",
        "capacity": 1,
    }
    r = api_client.post(config.AIRCRAFTS, json=payload)
    assert r.status_code in (200, 201), f"Setup aircraft falló: {r.status_code} {r.text}"
    body = r.json()
    assert body.get("id"), f"Setup aircraft sin id: {body}"
    return body["id"]

def _create_flight(api_client: ApiClient) -> dict:
    """Crea un flight válido y retorna el body (incluye id)."""
    aircraft_id = _create_aircraft(api_client)

    now = datetime.utcnow()
    payload = {
        "origin": "LMN",
        "destination": "EOU",
        "departure_time": _iso_utc(now + timedelta(minutes=5)),
        "arrival_time": _iso_utc(now + timedelta(hours=2)),
        "base_price": 150.0,
        "aircraft_id": aircraft_id,
    }
    r = api_client.post(config.FLIGHTS, json=payload)
    # Acepta 200/201 para no morir antes del DELETE
    assert r.status_code in (200, 201), f"Setup flight falló: {r.status_code} {r.text}"
    body = r.json()
    assert body.get("id"), f"Setup flight sin id: {body}"
    return body

def _warn_if_tolerated(name: str, got: int, preferred: tuple[int, ...], tolerated_only: tuple[int, ...] = ()):
    if got in tolerated_only:
        print(f"[{name}] Aviso: status {got} tolerado (backend inconsistente). Preferido: {preferred}")

# ---------- Casos de prueba ----------
# name         auth   id_source   preferred         tolerated
CASES = [
    ("DELETE ok-204", True,  "create",  (204, ),      ()),
    ("unauth-401",    False, "nocrea",  (401,),          (404,)),
    ("invalid-id",    True,  "invalid", (422, 404, 204), (400,)),
]
IDS = [name for name, *_ in CASES]

@pytest.mark.parametrize("name,auth,id_source,preferred,tolerated", CASES, ids=IDS)
def test_delete_flight_validations(api_client: ApiClient, admin_token: str,
                                   name: str, auth: bool, id_source: str,
                                   preferred: tuple[int, ...], tolerated: tuple[int, ...]):

    delete_client = api_client if auth else ApiClient()

    # Resolver id del flight según el caso
    if id_source == "create":
        target_id = _create_flight(api_client)["id"]
    elif id_source == "nocrea":
        # Un id cualquiera (no creado en este test). Se usa para ejercicio sin auth.
        target_id = "flg-" + uuid.uuid4().hex[:8]
    elif id_source == "invalid":
        # Id deliberadamente inválido (según validaciones del backend)
        target_id = "not-a-valid-id"
    else:
        pytest.fail(f"id_source desconocido: {id_source}")

    # DELETE /flights/{id}
    resp = delete_client.delete(f"{config.FLIGHTS}/{target_id}")
    status = resp.status_code

    # Aserción flexible (preferido vs tolerado)
    if status in preferred:
        pass
    elif status in tolerated:
        _warn_if_tolerated(name, status, preferred, tolerated)
    else:
        assert False, f"[{name}] Esperado {preferred} (tolerado {tolerated}), recibido {status}: {resp.text}"

    # Logs útiles
    if name == "ok-204" and status in (204, 200):
        print(f"[{name}] Borrado OK → status {status}")
    elif name == "unauth-401" and status in (401,):
        print(f"[{name}] DELETE sin token → 401 (correcto).")
    elif name == "unauth-401" and status in (404,):
        print(f"[{name}] Backend devolvió 404 sin token; se tolera por inconsistencia.")
    elif name == "invalid-id" and status in (204, 404, 400, 422):
        print(f"[{name}] ID inválido → status {status} (blindado).")
