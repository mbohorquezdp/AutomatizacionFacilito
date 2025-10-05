# tests/api_tests/users/test_delete_multiple_users.py
import pytest
from utils.api_helpers import ApiClient
from config.settings import USERS

# Lista de IDs a eliminar — reemplaza por tus IDs reales
USER_IDS = [
    "usr-998e1738",
    "usr-30166849",

]


@pytest.mark.parametrize("user_id", USER_IDS, ids=lambda uid: f"DELETE-{uid}")
def test_delete_multiple_users(api_client: ApiClient, admin_token: str, user_id: str):

    resp = api_client.delete(f"{USERS}/{user_id}")
    code = resp.status_code

    if code == 204:
        print(f"OK [{user_id}] eliminado correctamente.")
    elif code in (404, 400):
        print(f"NO-OK [{user_id}] no existe o formato inválido (status {code}).")
    else:
        pytest.fail(f"INESPERADO [{user_id}] respuesta inesperada {code}: {resp.text}")

    # Validación final
    assert code in (204, 404, 400), (
        f"[{user_id}] Esperaba 204/404/400, recibido {code}: {resp.text}"
    )