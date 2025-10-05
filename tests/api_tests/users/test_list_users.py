import pytest
from config.settings import USERS  # o from config.settings import USERS si está ahí
from utils.api_helpers import ApiClient


@pytest.mark.parametrize(
    "limit",
    [1, 3, 10],
    ids=lambda val: f"Limit={val}"
)


def test_list_users(api_client: ApiClient, admin_token: str, limit: int):
    skip = 0
    response = api_client.get(USERS, params={"skip": skip, "limit": limit})

    assert response.status_code == 200, f"Esperado 200, recibido {response.status_code}: {response.text}"

    data = response.json()
    assert data, "La respuesta de la API está vacía."

    print(f"\n[Limit={limit}] Se listaron {len(data) if isinstance(data, list) else 'N/A'} usuarios.")







