import pytest
from utils.api_helpers import ApiClient

#Cliente HTTP para toda la sesión (mantiene headers y token).
#Crea una instancia de la clase ApiClient
#encapsula las funciones para hacer GET, POST, PUT, DELETE contra la API (usando requests internamente).
#Devuelve ese cliente para ser usado en los tests
@pytest.fixture(scope="session")
def api_client() -> ApiClient:
    return ApiClient()

#Login una vez por sesión y deja Authorization configurado en api_client."""
@pytest.fixture(scope="session")
def admin_token(api_client: ApiClient) -> str:
    return api_client.login_admin()









