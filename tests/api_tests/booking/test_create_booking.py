import uuid
import pytest
import config.settings as config
from utils.api_helpers import ApiClient,VectorUtils
from utils.data_loader import BOOKINGS_CASOS

bookings_utils = VectorUtils(allowed_fields={"flight_id", "passengers"})

CASE_IDS = [c.get("id", f"case-{i}") for i, c in enumerate(BOOKINGS_CASOS)]

def _unique_email(prefix="ok"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@test.com"

class TestCreateBookings:
    @pytest.mark.parametrize("case", BOOKINGS_CASOS, ids=CASE_IDS)
    def test_create_Bookings_from_vector(self, api_client: ApiClient, admin_token: str, case: dict):
        case_id = case.get("id", "sin-id")

        # 1) Construir payload desde el vector, respetando solo campos permitidos
        payload = bookings_utils.build_payload(case)

        # 2) Normalizar expectativas del vector
        expected, expected_any = bookings_utils.normalize_expected(case)

        # 3) Ejecutar POST
        api_client = api_client if case.get("auth", True) else ApiClient()
        resp = api_client.post(config.BOOKINGS, json=payload)

        # 4) Asserts de estado
        if expected is not None:
            assert resp.status_code == expected, (
                f"[{case_id}] Esperado {expected}, recibido {resp.status_code}: {resp.text}"
            )
        else:
            assert expected_any, f"[{case_id}] No se definió expected_status ni expected_status_any"
            assert resp.status_code in expected_any, (
                f"[{case_id}] Esperaba {expected_any}, obtuve {resp.status_code}: {resp.text}"
            )

        # 5) Si fue creado (201): validar body mínimo y cleanup opcional
        if resp.status_code == 200:
            body = resp.json()
            assert "id" in body and body["id"], f"[{case_id}] Respuesta sin 'id': {body}"

            if case.get("cleanup"):
                booking_id = body["id"]
                d = api_client.delete(f"{config.BOOKINGS}/{booking_id}")
                assert d.status_code == 204, (
                    f"[{case_id}] DELETE esperaba 204, recibido {d.status_code}: {d.text}"
                )
