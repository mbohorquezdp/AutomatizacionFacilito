import pytest
from utils.api_helpers import ApiClient
from config.settings import BOOKINGS  # BOOKINGS = "/bookings"

def _pick_existing_booking_id(api_client: ApiClient) -> str | None:
    try:
        r = api_client.get(BOOKINGS, params={"skip": 0, "limit": 1})
    except Exception:
        return None

    if r.status_code != 200:
        return None

    try:
        data = r.json()
    except Exception:
        return None

    if isinstance(data, list) and data:
        return data[0].get("id")
    if isinstance(data, dict) and data.get("items"):
        # por si tu API devuelve {"items":[...]}
        items = data["items"]
        if items:
            return items[0].get("id")
    return None

#CASOS POSITIVOS Y NO VALIDOS
# name,        auth,   id_source,     preferred,          tolerated
CASES = [
    ("ok-delete",  True,  "existing",  (201, 200, 204),    (404,)),
    ("unauth-401", False, "existing",  (401,),             ()),
    ("invalid-422",True,  "invalid",   (422,),             (400, 404, 204))
]
IDS = [name for name, *_ in CASES]


@pytest.mark.parametrize("name,auth,id_source,preferred,tolerated", CASES, ids=IDS)
def test_delete_booking_validations(api_client: ApiClient, admin_token: str,
                                    name: str, auth: bool, id_source: str,
                                    preferred: tuple[int, ...], tolerated: tuple[int, ...]):

    # Elegir cliente según autenticación
    client = api_client if auth else ApiClient()

    # Preparar target_id
    if id_source == "existing":
        target_id = _pick_existing_booking_id(api_client)
        if not target_id:
            pytest.skip("No se encontró ningún booking existente para probar DELETE.")
    elif id_source == "invalid":
        target_id = "not-a-valid-id"  # malformado para provocar 422 (o 400/404)
    else:
        pytest.fail(f"id_source desconocido: {id_source}")

    # Ejecutar DELETE
    resp = client.delete(f"{BOOKINGS}/{target_id}")
    status = resp.status_code

    # Aserción
    if status in preferred:
        pass
    elif status in tolerated:
        print(f"[{name}] status {status} tolerado (preferido {preferred}).")
    else:
        assert False, (
            f"[{name}] Esperado {preferred} (tolerado {tolerated}), "
            f"recibido {status}: {resp.text}"
        )

    # Logs útiles
    if name == "ok-delete" and status in preferred:
        print(f"[{name}] DELETE OK → {status}.")
    if name == "unauth-401" and status == 401:
        print(f"[{name}] DELETE sin token → 401.")
    if name == "invalid-422" and status in (422, 400, 404, 204):
        print(f"[{name}] DELETE con id inválido → {status} (blindado).")
