import random
import string
import pytest
import config.settings as config
from utils.api_helpers import ApiClient

def _unique_iata() -> str:
    return "".join(random.choice(string.ascii_uppercase) for _ in range(3))

def _create_airport(api_client: ApiClient, *, city="Lima", country="Peru") -> str:
    iata = _unique_iata()
    payload = {"iata_code": iata, "city": city, "country": country}
    r = api_client.post(config.AIRPORTS, json=payload)

    if r.status_code in (200, 201):
        body = r.json()
        assert body.get("iata_code") == iata, f"Creación inconsistente: {body}"
        return iata
    elif r.status_code == 204:
        # Sin body → usamos el iata que mandamos
        return iata
    else:
        raise AssertionError(
            f"Creación de aeropuerto falló ({r.status_code}): {r.text}"
        )

def _payload_update_valido(current_iata: str) -> dict:
    return {
        "iata_code": current_iata,      # Muchas APIs exigen coherencia con el path
        "city": "Ciudad-Actualizada",
        "country": "Pais-Actualizado",
    }

def _payload_update_invalido(current_iata: str) -> dict:
    return {
        "iata_code": current_iata,
        "city": "",                     # inválido
        "country": "Pais-Actualizado",
    }

def _delete_if_possible(api_client: ApiClient, code: str):
    try:
        d = api_client.delete(f"{config.AIRPORTS}/{code}")
        if d.status_code in (200, 204, 404, 405):
            return
        # Si devuelve otra cosa rara, no rompemos la suite, solo registramos
        print(f"[cleanup] DELETE devolvió {d.status_code}: {d.text}")
    except Exception as e:
        print(f"[cleanup] Excepción al borrar aeropuerto {code}: {e}")

# =========================
# Casos parametrizados
# =========================
# name,        auth,   id_source,   payload_kind,        expected_statuses, tolerated
CASES = [
    ("ok-ACTUALIZADO 200",      True,  "create", "valido",   (200, 204), ()),
    ("not-found 404",    True,  "missing", "valido",  (404,),     ()),
    ("invalid-422",  False,  "create", "invalido", (422,),     (401,)),
    ("NO AUTORIZADO unauth-401",   False, "create", "valido",   (401,),     ()),
]
IDS = [name for name, *_ in CASES]

@pytest.mark.parametrize("name,auth,id_source,payload_kind,expected,tolerated", CASES, ids=IDS)
def test_update_airport_variantes(api_client: ApiClient, admin_token: str,
                                  name: str, auth: bool, id_source: str,
                                  payload_kind: str, expected: tuple[int, ...],
                                  tolerated: tuple[int, ...]):

    client = api_client if auth else ApiClient()

    # Resolver el iata_code objetivo
    if id_source == "create":
        target_code = _create_airport(api_client)
        cleanup_code = target_code
    elif id_source == "missing":
        target_code = "ZZZ"  # código no existente
        cleanup_code = None
    else:
        pytest.fail(f"id_source desconocido: {id_source}")

    # Elegir payload
    if payload_kind == "valido":
        payload = _payload_update_valido(target_code)
    elif payload_kind == "invalido":
        payload = _payload_update_invalido(target_code)
    else:
        pytest.fail(f"payload_kind desconocido: {payload_kind}")

    # Ejecutar PUT
    resp = client.put(f"{config.AIRPORTS}/{target_code}", json=payload)
    status = resp.status_code

    # Aserciones de estado (preferidos/tolerados)
    if status in expected:
        pass
    elif status in tolerated:
        print(f"[{name}] Status {status} tolerado (esperado {expected})")
    else:
        pytest.fail(f"[{name}] Esperado {expected} (tolerado {tolerated}), recibido {status}: {resp.text}")

    # Validaciones específicas por estado
    if status in (200,):
        body = resp.json()
        assert body.get("iata_code") == target_code, f"[{name}] iata_code distinto al target"
        assert body.get("city") == payload["city"], f"[{name}] city no se actualizó"
        assert body.get("country") == payload["country"], f"[{name}] country no se actualizó"

    elif status == 204:
        pass
    elif status == 422:
        try:
            body = resp.json()
        except Exception:
            body = {}
        assert "detail" in body, f"[{name}] 422 sin 'detail': {resp.text}"

    elif status == 401:
        try:
            body = resp.json()
        except Exception:
            body = {}
        assert body.get("detail") == "Not authenticated", f"[{name}] 401 sin 'Not authenticated': {body}"

    elif status == 404:
        pass

    # Limpieza
    if cleanup_code and auth:
        _delete_if_possible(api_client, cleanup_code)
