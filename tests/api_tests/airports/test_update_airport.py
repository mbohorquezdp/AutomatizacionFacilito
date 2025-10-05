import random
import string
import faker

from utils.api_helpers import api_request
from config.settings import BASE_URL_API, AIRPORT


fake = faker.Faker()

def put_airport(uid: str , auth_headers) -> None:

    user_data = {
        "iata_code": "".join(random.choices(string.ascii_uppercase, k=3)),
        "city": fake.country(),
        "country": fake.country_code()
    }

    r = api_request("PUT", BASE_URL_API + AIRPORT + "/" + str(uid), headers=auth_headers, json=user_data, timeout=10)

    # Acepta 200 (body)
    assert r.status_code == 200, f"PUT {r.url} → {r.status_code}\n{r.text}"

    # Si fue 200, puedes validar el body
    if r.status_code == 200:
        body = r.json()
        assert body.get("city"), "city no volvió en la respuesta"

# Caso Positivo 200
def test_put_un_usuario(auth_headers):
    put_airport("EBD", auth_headers)  # usa un id real, debe existir


# Caso negativo: payload inválido → espera 422
def test_put_airport_negativo(auth_headers):
    uid = "ZXR"  # un IATA existente
    url = BASE_URL_API + AIRPORT + "/" + str(uid)

    user_data = {
        "iata_code": "DX",   # inválido (<3)
        "city": "x",          # vacío
        "country": "x"        # vacío
    }

    r = api_request("PUT", url, headers=auth_headers, json=user_data, timeout=10)
    assert r.status_code == 422, "Esperaba 422 y fue {r.status_code}\n{r.text}"

