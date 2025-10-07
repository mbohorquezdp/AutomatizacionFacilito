import pytest
from utils.api_helpers import ApiClient
from config.settings import AIRPORTS
import random,string
from faker import Faker

fake = Faker()


def _create_airport(api_client: ApiClient) -> dict:
    payload = {
        "iata_code": ''.join(random.choices(string.ascii_uppercase, k=3)),
        "city": fake.city(),
        "country": fake.country(),
    }
    r = api_client.post(AIRPORTS, json=payload)
    assert r.status_code == 201 , f"Error en creación ({r.status_code}): {r.text}"
    body = r.json()
    assert body.get("iata_code"), f"Respuesta de creación sin iata_code: {body}"
    return body

def _warn_if_tolerated(name: str, got: int, preferred: tuple[int, ...], tolerated_only: tuple[int, ...] = ()):
    if got in tolerated_only:
        print(f"[{name}] Aviso: status {got} tolerado (backend inconsistente). Preferido: {preferred}")

#CASOS DE PRUEA POSITIVO Y NEGATIVOS
CASES = [
    # name         auth   id_source  preferred      tolerated
    ("ok-Delete 204",     True,  "create",  (204,),        ()),
    ("NO AUTORIZADO 401", False, "nocrea",  (401,),        ()),
    ("ID invalid-id 422/204", True,  "invalid", (422,204),         (204,)),
]
IDS = [name for name, *_ in CASES]

@pytest.mark.parametrize("name,auth,id_source,preferred,tolerated", CASES, ids=IDS)
def test_delete_airports_validations(api_client: ApiClient, admin_token: str,
                                 name: str, auth: bool, id_source: str,
                                 preferred: tuple[int, ...], tolerated: tuple[int, ...]):
    delete_client = api_client if auth else ApiClient()

    if id_source == "create":
        target_id = _create_airport(api_client)["iata_code"]
    elif id_source == "nocrea":
        target_id = "unauth-401"
    elif id_source == "invalid":
        target_id = "not-a-valid-id"  # el backend lo acepta como str
    else:
        pytest.fail(f"id_source desconocido: {id_source}")

    resp = delete_client.delete(f"{AIRPORTS}/{target_id}")
    status = resp.status_code

    if status in preferred:
        pass
    elif status in tolerated:
        _warn_if_tolerated(name, status, preferred, tolerated)
    else:
        assert False, f"[{name}] Esperado {preferred} (tolerado {tolerated}), recibido {status}: {resp.text}"

    # logs útiles
    if name == "ok-Delete 204" and status == 204:
        print(f"[{name}] Borrado OK → status {status}")
    elif name == "unauth-NO AUTORIZADO 401" and status == 401:
        print(f"[{name}] DELETE sin token → 401")
    elif name == "invalid-id" and status in (204, 404, 400):
        print(f"[{name}] ID inválido → status {status} ")







