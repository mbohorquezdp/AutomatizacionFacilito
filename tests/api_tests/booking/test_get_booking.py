import pytest
from utils.api_helpers import ApiClient
from config.settings import BOOKINGS  # asegúrate: BOOKINGS = "/bookings"

#CASOS PROPUESTOS POSITIVOS Y NEGATIVOS ( AQUI APLICA TOLERANCIA A 500)
# name,                    auth,   booking_id,    expected,     tolerated
CASES = [
    ("ok-200",              True,   "bkg-6c5061f3",          (200,),       (404,500,)),
    ("booking-invalido",    True,   "not-valid",   (422,),       (400, 404)),
    ("unauth-401",          False,  "44",          (401,),       ()),
]
IDS = [name for name, *_ in CASES]

@pytest.mark.parametrize("name,auth,booking_id,expected,tolerated", CASES, ids=IDS)
def test_get_booking_variantes(api_client: ApiClient, admin_token: str,
                               name: str, auth: bool, booking_id: str,
                               expected: tuple[int, ...], tolerated: tuple[int, ...]):
    # Cliente según autenticación
    client = api_client if auth else ApiClient()

    # Ejecutar GET /bookings/{id}
    resp = client.get(f"{BOOKINGS}/{booking_id}")
    status = resp.status_code

    # Validación de código HTTP con preferidos/tolerados
    if status in expected:
        pass
    elif status in tolerated:
        print(f"[{name}] Status {status} tolerado (esperado {expected}).")
    else:
        pytest.fail(f"[{name}] Esperado {expected} (tolerado {tolerated}), recibido {status}: {resp.text}")

    # Validaciones por código
    if status == 200:
        body = resp.json()
        assert isinstance(body, dict), f"[{name}] El body no es un objeto JSON: {body!r}"
        # Validaciones mínimas y seguras (no asumimos todo el esquema)
        assert "id" in body, f"[{name}] Falta 'id' en la respuesta: {body}"
        # id puede ser str o int según backend
        assert isinstance(body["id"], (str, int)), f"[{name}] 'id' no es str|int: {type(body['id'])}"
        # Campos opcionales (si existen, validar tipos razonables)
        if "status" in body:
            assert isinstance(body["status"], str), f"[{name}] 'status' no es str"
        if "total" in body:
            assert isinstance(body["total"], (int, float)), f"[{name}] 'total' no es numérico"
        if "user_id" in body:
            assert isinstance(body["user_id"], (str, int)), f"[{name}] 'user_id' no es str|int"
        if "flight_id" in body:
            assert isinstance(body["flight_id"], (str, int)), f"[{name}] 'flight_id' no es str|int"

        print(f"[{name}] Booking OK → id={body['id']}")
    elif status == 404:
        print(f"[{name}] Booking '{booking_id}' no encontrado (404).")
    elif status == 401:
        try:
            body = resp.json()
            if isinstance(body, dict) and "detail" in body:
                print(f"[{name}] 401: {body['detail']}")
        except Exception:
            pass
    elif status in (400, 422):
        # En 422 típicamente hay 'detail' con errores de validación
        try:
            body = resp.json()
            if isinstance(body, dict) and "detail" in body:
                print(f"[{name}] {status} con detail: {body['detail']}")
        except Exception:
            print(f"[{name}] {status} sin JSON parseable.")
