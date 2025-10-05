# tests/AIRCRAFTs/test_get_AIRCRAFT.py
import pytest
from utils.api_helpers import api_request
from config.settings import BASE_URL_API, AIRCRAFTS

def get_AIRCRAFT(uid, auth_headers):
    return api_request("GET", BASE_URL_API + AIRCRAFTS + "/" + str(uid), headers=auth_headers, timeout=10)

@pytest.mark.parametrize(
    "uid, expected_status",
    [
        ("acf-923fb730", 200),
        ("acf-1ee5ccf5", 200),
        ("XXXXXX", 422),
    ],
    ids=["positivo", "positivo","Negativo"],
)
def test_get_AIRCRAFT_parametrizado(auth_headers, uid, expected_status):
    r = get_AIRCRAFT(uid, auth_headers)
    assert r.status_code == expected_status, f"GET {r.request.url} → {r.status_code}\n{r.text}"
    if expected_status == 200:
        body = r.json()
        # Valida contrato mínimo solo en el caso positivo
        assert isinstance(body.get("id"), str) and body["id"].strip()
        assert isinstance(body.get("model"), str) and body["model"].strip()