# tests/api_tests/airports/test_update_airport.py
import pytest
from utils.api_helpers import ApiClient
from config.settings import AIRPORTS

@pytest.mark.parametrize(
    "path_iata, payload, expected_status",
    [
        # Caso OK (200)
        (
            "ANE",
            {
                "iata_code": "ANE",
                "city": "Dennisville",
                "country": "Cape Verde"
            },
            200,
        ),
        # Caso inválido (422)
        (
            "ANE",
            {
                "iata_code": "",   # inválido
                "city": "",        # inválido
                "country": ""      # inválido
            },
            422,
        ),
    ],
    ids=["Update_200", "Update_422"]
)
def test_update_airport_simple(api_client: ApiClient, admin_token: str, path_iata: str, payload: dict, expected_status: int):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {admin_token}",
    }

    resp = api_client.put(f"{AIRPORTS}/{path_iata}", json=payload, headers=headers)

    assert resp.status_code == expected_status, (
        f"Esperado {expected_status}, recibido {resp.status_code}: {resp.text}"
    )

    if expected_status == 200:
        data = resp.json()
        # Validaciones mínimas del update
        assert data.get("iata_code") == "ANE", "No coincide iata_code."
        assert data.get("city") == payload["city"], "city no se actualizó."
        assert data.get("country") == payload["country"], "country no se actualizó."
        print(f"[OK] Aeropuerto ANE actualizado: {data['city']}, {data['country']}")
