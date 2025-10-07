import time
import random
import pytest
from utils.api_helpers import ApiClient
from config.settings import BOOKINGS  # BOOKINGS = "/bookings"

# --- Helper: pequeño retry contra 5xx en lecturas ---
def _get_with_retry(client: ApiClient, path: str, *, retries: int = 2, backoff: float = 0.6, **kw):
    last = None
    for i in range(retries + 1):
        resp = client.get(path, **kw)
        if resp.status_code < 500:
            return resp
        last = resp
        if i < retries:
            time.sleep(backoff * (2**i) + random.uniform(0, 0.2))
    return last

#CASOS PROPUESTOS VALIDOS E INVALIDOS
# name,           auth,   params,                             expected,   tolerated
CASES = [
    ("ok-default",  True,  {},                                 (200,),     ()),
    ("ok-limit-5",  True,  {"skip": 0, "limit": 5},            (200,),     ()),
    ("bad-limit-str",True, {"skip": 0, "limit": "x"},          (422,),     (400,)),
    ("unauth-401",  False, {"skip": 0, "limit": 3},            (401,),     ()),            # sin token
]
IDS = [name for name, *_ in CASES]


@pytest.mark.parametrize("name,auth,params,expected,tolerated", CASES, ids=IDS)
def test_list_bookings(api_client: ApiClient, admin_token: str,
                       name: str, auth: bool, params: dict,
                       expected: tuple[int, ...], tolerated: tuple[int, ...]):

    client = api_client if auth else ApiClient()

    resp = _get_with_retry(client, BOOKINGS, params=params)
    status = resp.status_code

    # Manejo de estado esperado / tolerado / 5xx
    if status in expected:
        pass
    elif status in tolerated:
        print(f"[{name}] Status {status} tolerado (esperado {expected}).")
    elif status >= 500:
        # Diagnóstico fuerte si persiste 5xx tras el retry
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        pytest.fail(f"[{name}] 5xx del backend → {status}. Body={body} Headers={dict(resp.headers)}")
    else:
        pytest.fail(f"[{name}] Esperado {expected} (tolerado {tolerated}), recibido {status}: {resp.text}")

    # Validaciones por código
    if status == 200:
        # La API puede devolver una lista directa o un objeto con 'items'
        try:
            data = resp.json()
        except Exception:
            pytest.fail(f"[{name}] 200 pero la respuesta no es JSON parseable: {resp.text!r}")

        if isinstance(data, list):
            items = data
        elif isinstance(data, dict) and isinstance(data.get("items"), list):
            items = data["items"]
        else:
            pytest.fail(f"[{name}] 200 pero el body no es lista ni contiene 'items': {data!r}")

        # Si enviamos limit, la cantidad no debe excederlo (cuando aplique)
        lim = params.get("limit")
        if isinstance(lim, int) and lim >= 0:
            assert len(items) <= lim, f"[{name}] len(items)={len(items)} excede limit={lim}"

        # Validaciones ligeras por elemento (si hay al menos uno)
        if items:
            first = items[0]
            assert isinstance(first, dict), f"[{name}] item no es objeto JSON: {first!r}"
            # Campos típicos (condicionales)
            if "id" in first:      assert isinstance(first["id"], (str, int))
            if "user_id" in first: assert isinstance(first["user_id"], (str, int))
            if "flight_id" in first: assert isinstance(first["flight_id"], (str, int))
            if "status" in first:  assert isinstance(first["status"], str)

        print(f"[{name}] OK 200 → items={len(items)}")

    elif status == 401:
        # Algunos backends devuelven detail explícito
        try:
            body = resp.json()
            if isinstance(body, dict) and "detail" in body:
                print(f"[{name}] 401: {body['detail']}")
        except Exception:
            pass

    elif status in (400, 422):
        # Mostrar el detalle de validación si existe
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        print(f"[{name}] {status} → detail={body}")
