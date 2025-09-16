# tests/airports/test_get_airport.py
import pytest
from utils.api_helpers import api_request
from config.settings import BASE_URL_API, AIRPORT

def get_airport(uid: str | int, auth_headers: dict, *, timeout: int = 10):
    return api_request("GET", BASE_URL_API + AIRPORT + "/" + str(uid), headers=auth_headers, timeout=timeout)

@pytest.mark.parametrize(
    "uid, expected_status",
    [
        ("IMC", 200),
        ("ZZZ", 404),
        ("IMC", 404),
    ],
    ids=["positivo", "negativo","Falla"],
)
def test_get_airport_parametrizado(auth_headers, uid, expected_status):
    r = get_airport(uid, auth_headers)
    assert r.status_code == expected_status, f"GET {r.request.url} → {r.status_code}\n{r.text}"
    if expected_status == 200:
        body = r.json()
        # Valida contrato mínimo solo en el caso positivo
        assert isinstance(body.get("iata_code"), str) and body["iata_code"].strip()
        assert isinstance(body.get("city"), str) and body["city"].strip()
