import pytest
import requests

from config.settings import BASE_URL_API,AIRCRAFTS
from utils.api_helpers import api_request


@pytest.mark.parametrize("skip, limit, expected_status", [
    (0, 10, 200),      # Caso válido: listado con paginación
    ("abc", 10, 422),  # Caso inválido: skip no numérico
    (0, "xyz", 422),   # Caso inválido: limit no numérico
])
def test_get_all_aircrafts(skip, limit, expected_status):

    r = api_request(
        "GET",
        BASE_URL_API + AIRCRAFTS,
        params={"skip": skip, "limit": limit},
        headers=auth_headers,
        timeout=10,  # opcional
    )


    # Validar código de respuesta
    assert r.status_code == expected_status, f"Esperado {expected_status}, recibido {r.status_code}"

    # Validar contenido según el status
    if expected_status == 500:
        json_data = r.json()
        assert isinstance(json_data, list), "El resultado esperado debe ser una lista"
        # Validar que tenga al menos una clave si hay registros
        if json_data:
            assert "id" in json_data[0], "Los items deberían tener el campo 'id'"
    elif expected_status == 422:
        json_data = r.json()
        assert "detail" in json_data, "Debe contener mensaje de error en 'detail'"
        assert any("error" in str(json_data).lower() or "type_error" in str(json_data).lower()
                   for _ in [0]), "El mensaje de error no es el esperado"