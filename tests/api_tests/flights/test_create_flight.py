from datetime import datetime, timedelta, timezone
import pytest
from utils.api_helpers import api_request
from config.settings import BASE_URL_API, FLIGHTS

def _join(b, p):  # une URLs sin duplicar/omitir '/'
    return f"{b.rstrip('/')}/{p.lstrip('/')}"

def _iso_now_plus(hours: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()

@pytest.fixture
def flights(auth_headers):
    flights_data = {
        "origin": "MYK",
        "destination": "MMQ",
        "departure_time": _iso_now_plus(1),
        "arrival_time": _iso_now_plus(4),  # llegada > salida
        "base_price": 199.99,
        "aircraft_id": "A320-PE-001",
    }

    url = _join(BASE_URL_API, FLIGHTS)
    r = api_request("POST", url, json=flights_data, headers=auth_headers, timeout=10)
    r.raise_for_status()
    body = r.json()

    # intenta obtener el id para el teardown
    uid = body.get("id") or body.get("_id") or body.get("flight_id") or body.get("code")
    if not uid:
        loc = r.headers.get("Location")
        if isinstance(loc, str):
            uid = loc.rstrip("/").split("/")[-1]

    yield body

    if uid:
        api_request("DELETE", _join(url, str(uid)), headers=auth_headers, timeout=10)


# tests/api_tests/flights/test_flights.py
def test_flight(flights):
    # contrato mínimo
    assert flights.get("origin") == "LIM"
    assert flights.get("destination") == "MIA"
    # id presente con alguna de las claves conocidas
    assert any(k in flights and flights[k] for k in ("id", "_id", "flight_id", "code"))
