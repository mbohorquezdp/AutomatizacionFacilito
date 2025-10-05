# Data para crear USERS

USUARIOS = [
    {"id": "ok-basico",
     "email": "xxx195@test.com", "password": "Abc123!", "full_name": "name_aaaa", "role": "passenger",
     "Resultado esperado 201": 201, "cleanup": True},

    {"id": "email-invalido",
     "email": "xxxxxxxxxxx", "password": "Abc123!", "full_name": "name_bbbb", "role": "passenger",
     "Resultado esperado 422": 422},

    {"id": "Email no debe estar vacio",
     "email": "", "password": "Abc123!", "full_name": "name_ccc", "role": "passenger",
     "Resultado esperado 422": 422},

    {"id": "Nombre de debe ser un número",
     "email": "", "password": "Abc123!", "full_name": "111111", "role": "passenger",
     "Resultado esperado 422": 422}

]


import random
import string

AEROPUERTOS = [
    {
        "id": "ok-basico",
        "iata_code": ''.join(random.choices(string.ascii_uppercase, k=3)),
        "city": "Lima",
        "country": "Peru",
        "expected_status": 201,
        "cleanup": True,
    },
    {
        "id": "iata-invalido",
        "iata_code": "LONG",        # 4 letras → 422
        "city": "Bogota",
        "country": "Colombia",
        "expected_status": 422
    },
    {
        "id": "falta-city",
        "iata_code": "BOG",
        "city": "",
        "country": "Colombia",
        "expected_status": 400
    },
    {
        "id": "falta-country",
        "iata_code": "CUN",
        "city": "Cancun",
        "country": "",
        "expected_status": 400
    },
    {
        "id": "sin-auth",
        "iata_code": "QIT",
        "city": "Quito",
        "country": "Ecuador",
        "expected_status": 401,
        "auth": False
    },
]



