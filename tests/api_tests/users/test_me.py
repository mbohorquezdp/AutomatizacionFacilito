import pytest
from config.settings import USERS_ME
from utils.api_helpers import ApiClient

@pytest.mark.parametrize(
    "auth",
    [True, False],
    ids=lambda val: f"Muestra AUTH={val}"
)
def test_me(api_client: ApiClient, admin_token: str, auth: bool):
    #Si auth=True: debe devolver 200 y datos del usuario.
    #Si auth=False: debe devolver 401 Unauthorized.
    client = api_client if auth else ApiClient()

    response = client.get(USERS_ME)
    data = response.text

    if auth:
        # Validar éxito
        assert response.status_code == 200, f"[Auth={auth}] Esperado 200, recibido {response.status_code}: {data}"
        assert data != "", f"[Auth={auth}] Respuesta vacía en /users/me"
        body = response.json()
        print(f"\n[Auth={auth}] Usuario: {body.get('email', 'sin email')} | Rol: {body.get('role', 'sin rol')}")
    else:
        # Validar no autenticado
        assert response.status_code == 401, f"[Auth={auth}] Esperado 401, recibido {response.status_code}: {data}"
        print(f"\n[Auth={auth}] /users/me sin token devolvió correctamente 401 Unauthorized.")
