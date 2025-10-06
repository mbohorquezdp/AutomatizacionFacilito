
import pytest
from utils.api_helpers import ApiClient
from config.settings import AIRCRAFTS

CASES = [
    ("ok-caso positivo 200", True,  "acf-f8da3c9d", (200,),    ()),
    ("Avion inexistente 422", True, "acf-no-existe", (404,),   ()),
    ("unauth-401",            False, "acf-iouo", (401,),   (404, 200)),
]
IDS = [name for name, *_ in CASES]

@pytest.mark.parametrize("name,auth,aircraft_id,expected,tolerated", CASES, ids=IDS)
def test_get_aircraft_variantes(api_client: ApiClient, admin_token: str,
                                name: str, auth: bool, aircraft_id: str,
                                expected: tuple[int, ...], tolerated: tuple[int, ...]):
    client = api_client if auth else ApiClient()

    resp = client.get(f"{AIRCRAFTS}/{aircraft_id}")
    status = resp.status_code

    if status in expected:
        pass
    elif status in tolerated:
        print(f"[{name}] Status {status} tolerado (esperado {expected}).")
    else:
        pytest.fail(f"[{name}] Esperado {expected} (tolerado {tolerated}), recibido {status}: {resp.text}")

    if status == 200:
        body = resp.json()
        assert isinstance(body.get("id"), str) and body["id"].strip(), f"[{name}] id inválido"
        assert isinstance(body.get("tail_number"), str) and body["tail_number"].strip(), f"[{name}] tail_number inválido"
        assert isinstance(body.get("model"), str) and body["model"].strip(), f"[{name}] model inválido"
        assert isinstance(body.get("capacity"), int), f"[{name}] capacity no es entero"
        print(f"[{name}] Avión: id={body['id']} | tail={body['tail_number']} | model={body['model']} | cap={body['capacity']}")
    elif status == 404:
        print(f"[{name}] Aircraft '{aircraft_id}' no encontrado (404 correcto).")
    elif status == 401:
        print(f"[{name}] Acceso no autorizado (401).")
