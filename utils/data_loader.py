# Data para crear USERS
import uuid

def _unique_email(prefix="ok"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@test.com"


USUARIOS = [
    {"id": "Ok- registro de usuario 201",
     "email": _unique_email(), "password": "Abc123!", "full_name": "name_aaaa", "role": "passenger",
     "Resultado esperado 201": 201, "cleanup": True},

    {"id": "Email Ya existe 400",
     "email": "admin@demo.com", "password": "Abc123!", "full_name": "name_aaaa", "role": "passenger",
     "Resultado esperado 400": 400},

    {"id": "email-invalido 422",
     "email": "xxxxxxxxxxx", "password": "Abc123!", "full_name": "name_bbbb", "role": "passenger",
     "Resultado esperado 422": 422},

    {"id": "Email no debe estar vacio 422",
     "email": "", "password": "Abc123!", "full_name": "name_ccc", "role": "passenger",
     "Resultado esperado 422": 422},

    {"id": "Nombre de debe ser un número 422",
     "email": "", "password": "Abc123!", "full_name": "111111", "role": "passenger",
     "Resultado esperado 422": 422}

]


import random
import string

AEROPUERTOS = [
    {
        "id": "ok- Registro de Aeropuerto 201",
        "iata_code": ''.join(random.choices(string.ascii_uppercase, k=3)),
        "city": "Lima",
        "country": "Peru",
        "expected_status": 201,
        "cleanup": True,
    },
    {
        "id": "iata-invalido, Logitud >3 digitos 422",
        "iata_code": "LONG",        # 4 letras → 422
        "city": "Bogota",
        "country": "Colombia",
        "expected_status": 422
    },

    {
        "id": "Invalido sin-auth 401",
        "iata_code": "QIT",
        "city": "Quito",
        "country": "Ecuador",
        "expected_status": 401,
        "auth": False
    },
]



