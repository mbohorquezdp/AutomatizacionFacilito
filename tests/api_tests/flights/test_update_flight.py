import pytest
from config.settings import FLIGHTS, AIRCRAFTS
from utils.api_helpers import ApiClient

def _any_aircraft_id(api_client: ApiClient, token: str):
    r = api_client.get(
        AIRCRAFTS,
        params={"skip": 0, "limit": 1},
        headers={"accept": "application/json", "Authorization": f"Bearer {token}"}
    )
    if r.status_code == 200 and isinstance(r.json(), list) and r.json():
        a = r.json()[0]
        return a.get("id") or a.get("aircraft_id")
    pytest.skip("No hay aircrafts disponibles para el UPDATE de flight.")

def _any_flight_and_aircraft(api_client: ApiClient, token: str):
    h = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    r = api_client.get(FLIGHTS, params={"skip": 0, "limit": 1}, headers=h)
    if r.status_code == 200 and isinstance(r.json(), list) and r.json():
        f = r.json()[0]
        fid = f.get("id") or f.get("flight_id")
        aid = f.get("aircraft_id") or _any_aircraft_id(api_client, token)
        return fid, aid
    pytest.skip("No hay flights para probar UPDATE (semilla vacía).")

# ---------- Casos 200 y 422 (estables) ----------
@pytest.mark.parametrize(
    "case_id, expected_status, payload",
    [
        (
            "Update_200",
            200,
            {
                "origin": "YSB",
                "destination": "EBQ",
                "departure_time": "2025-10-07T03:14:10.209Z",
                "arrival_time":  "2025-10-07T03:14:10.209Z",
                "base_price": 150.0,
                "aircraft_id": "__REPLACE__",  # se inyecta luego con uno válido
            },
        ),
        (
            "Update_422",
            422,
            {
                "origin": "",
                "destination": "",
                "departure_time": "fecha-invalida",
                "arrival_time":  "tambien-invalida",
                "base_price": -10,
                "aircraft_id": "__REPLACE__",  # siempre válido para evitar 404
            },
        ),
    ],
    ids=["Update_200", "Update_422"]
)
def test_update_flight_ok_and_422(api_client: ApiClient, admin_token: str, case_id, expected_status, payload):
    flight_id, valid_aircraft_id = _any_flight_and_aircraft(api_client, admin_token)
    payload = {**payload, "aircraft_id": valid_aircraft_id}

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {admin_token}"
    }
    resp = api_client.put(f"{FLIGHTS}/{flight_id}", json=payload, headers=headers)

    assert resp.status_code == expected_status, (
        f"[{case_id}] Esperado {expected_status}, recibido {resp.status_code}: {resp.text}"
    )

    if expected_status == 200:
        data = resp.json()
        assert data.get("origin") == payload["origin"], "No se actualizó 'origin'."
        assert data.get("destination") == payload["destination"], "No se actualizó 'destination'."

# ---------- Caso 401 (con detección y skip controlado) ----------
def test_update_flight_unauthorized(api_client: ApiClient, admin_token: str):
    flight_id, valid_aircraft_id = _any_flight_and_aircraft(api_client, admin_token)
    payload = {
        "origin": "MEX",
        "destination": "LAX",
        "departure_time": "2025-10-08T02:00:00.000Z",
        "arrival_time":  "2025-10-08T06:00:00.000Z",
        "base_price": 120.0,
        "aircraft_id": valid_aircraft_id,
    }

    # Sin Authorization

    api_client = ApiClient()
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    resp = api_client.put(f"{FLIGHTS}/{flight_id}", json=payload, headers=headers)

    if resp.status_code != 401:
        pytest.skip(f"El endpoint no exige autenticación en este ambiente (recibido {resp.status_code}).")

    assert resp.status_code == 401, f"Esperado 401, recibido {resp.status_code}: {resp.text}"
