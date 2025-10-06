import pytest
from utils.api_helpers import ApiClient
from config.settings import AIRPORTS

# --- Escenarios de prueba ---
CASES = [
    # name,    auth,   iata_code,  expected,  tolerated
    ("ok-caso positivo 200",     True,  "DNZ",  (200,),   ()),
    ("aeropuerto inexistente 404",  True,  "ZZZ",  (404,),   ()),
    ("unauth-401", False, "IMC",  (401,),   (404,)),           #
]

IDS = [name for name, *_ in CASES]

@pytest.mark.parametrize("name,auth,iata_code,expected,tolerated", CASES, ids=IDS)
def test_get_airport_variantes(api_client: ApiClient, admin_token: str,
                               name: str, auth: bool, iata_code: str,
                               expected: tuple[int, ...], tolerated: tuple[int, ...]):

    # Cliente autenticado o sin autenticación
    client = api_client if auth else ApiClient()

    # Ejecución de la petición
    resp = client.get(f"{AIRPORTS}/{iata_code}")
    status = resp.status_code

    # Aserción flexible (preferido / tolerado)
    if status in expected:
        pass
    elif status in tolerated:
        print(f"[{name}] Status {status} tolerado (esperado {expected})")
    else:
        pytest.fail(f"[{name}] Esperado {expected} (tolerado {tolerated}), recibido {status}: {resp.text}")

    # Validaciones adicionales solo para casos 200
    if status == 200:
        body = resp.json()
        assert isinstance(body.get("iata_code"), str) and body["iata_code"].strip(), f"[{name}] iata_code inválido"
        assert isinstance(body.get("city"), str) and body["city"].strip(), f"[{name}] city inválido"
        assert isinstance(body.get("country"), str) and body["country"].strip(), f"[{name}] country inválido"
        print(f"[{name}] Aeropuerto obtenido correctamente: {body['iata_code']} - {body['city']}, {body['country']}")

    elif status == 401:
        print(f"[{name}] Acceso no autorizado (token ausente o inválido).")

    elif status == 404:
        print(f"[{name}] Aeropuerto '{iata_code}' no encontrado (404 correcto).")
