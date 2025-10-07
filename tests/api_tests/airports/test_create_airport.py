
import pytest
import config.settings as config
from utils.api_helpers import ApiClient, VectorUtils
from utils.data_loader import VUELOS  # <-- tu vector de casos para flights

# Acepta únicamente los campos válidos del contrato de /flights
flights_utils = VectorUtils(allowed_fields={
    "origin", "destination", "departure_time", "arrival_time", "base_price", "aircraft_id"
})

# IDs legibles para cada caso (si no trae 'id' en el vector, asigna uno genérico)
CASE_IDS = [c.get("id", f"case-{i}") for i, c in enumerate(VUELOS)]

class TestCreateFlights:
    @pytest.mark.parametrize("case", VUELOS, ids=CASE_IDS)
    def test_create_flights_from_vector(self, api_client: ApiClient, admin_token: str, case: dict):
        case_id = case.get("id", "sin-id")

        # 1) Construir payload desde el vector, solo con los campos permitidos
        payload = flights_utils.build_payload(case)

        # 2) Normalizar expectativas del vector
        expected, expected_any = flights_utils.normalize_expected(case)

        # 3) Elegir cliente (con/sin auth) según el caso
        client = api_client if case.get("auth", True) else ApiClient()

        # 4) Ejecutar POST /flights
        resp = client.post(config.FLIGHTS, json=payload)

        # 5) Asserts de estado (igual que en Airports, pero soportando expected_any si se usa)
        if expected is not None:
            assert resp.status_code == expected, (
                f"[{case_id}] Esperado {expected}, recibido {resp.status_code}: {resp.text}"
            )
        else:
            assert expected_any, f"[{case_id}] Define expected_status o expected_status_any en el vector"
            assert resp.status_code in expected_any, (
                f"[{case_id}] Esperaba {expected_any}, recibido {resp.status_code}: {resp.text}"
            )

        # 6) Si fue creado (201 o 200 según backend): validar body mínimo y cleanup opcional
        if resp.status_code in (201, 200):
            body = resp.json()

            # Validaciones
            assert body.get("origin") == payload.get("origin"), f"[{case_id}] 'origin' inconsistente"
            assert body.get("destination") == payload.get("destination"), f"[{case_id}] 'destination' inconsistente"
            assert "aircraft_id" in body and body["aircraft_id"], f"[{case_id}] 'aircraft_id' vacío"
            flight_id = body.get("id")
            assert flight_id, f"[{case_id}] Respuesta sin 'id': {body}"

            # Cleanup opcional
            if case.get("cleanup"):
                d = client.delete(f"{config.FLIGHTS}/{flight_id}")
                assert d.status_code in (204, 200), (
                    f"[{case_id}] DELETE esperaba 204/200, recibido {d.status_code}: {d.text}"
                )

        # 7) Logs para negativos (401/422, etc.)
        elif resp.status_code == 401:
            print(f"[{case_id}] Correcto: 401 Not authenticated (sin token o inválido).")
        elif resp.status_code == 422:
            print(f"[{case_id}] Correcto: 422 Validation Error → {resp.text[:200]}")
        else:
            # Si definiste explícitamente expected/expected_any, ya se validó arriba.
            print(f"[{case_id}] Status {resp.status_code}: {resp.text[:200]}")
