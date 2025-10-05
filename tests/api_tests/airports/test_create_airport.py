import uuid
import pytest
import config.settings as config
from utils.api_helpers import ApiClient,VectorUtils
from utils.data_loader import AEROPUERTOS

airports_utils = VectorUtils(allowed_fields={"iata_code","city", "country"})

CASE_IDS = [c.get("id", f"case-{i}") for i, c in enumerate(AEROPUERTOS)]

class TestCreateAirports:
    @pytest.mark.parametrize("case", AEROPUERTOS, ids=CASE_IDS)
    def test_create_airports_from_vector(self, api_client: ApiClient, admin_token: str, case: dict):
        case_id = case.get("id", "sin-id")

        # 1)Construir payload desde el vector, respetando solo campos permitidos
        payload = airports_utils.build_payload(case)

        # 2) Normalizar expectativas del vector (acepta tus claves “Resultado esperado 201”, etc.)
        expected, expected_any = airports_utils.normalize_expected(case)

        api_client = api_client if case.get("auth", True) else ApiClient()

        # 3) Ejecutar POST
        resp = api_client.post(config.AIRPORTS, json=payload)

        # 4) Asserts de estado
        assert resp.status_code == expected, (
            f"[{case_id}] Esperado {expected}, recibido {resp.status_code}: {resp.text}"
        )

        # 5) Si fue creado (201): validar body mínimo y cleanup opcional
        if resp.status_code == 201:
            body = resp.json()

            assert body.get("city") == payload["city"], f"[{case_id}] city no se encuentra"
            airport_id = body.get("iata_code")
            assert airport_id, f"[{case_id}] Respuesta sin 'id': {body}"

            if case.get("cleanup"):
                d = api_client.delete(f"{config.AIRPORTS}/{airport_id}")
                assert d.status_code == 204, (
                    f"[{case_id}] DELETE esperaba 204, recibido {d.status_code}: {d.text}"
                )
        else:
            print(f"[{case_id}] Esperado {expected}, recibido {resp.status_code}: {resp.text}")


