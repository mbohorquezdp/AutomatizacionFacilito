# Data para crear USERS
import uuid

from config.settings import BOOKINGS


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

AVIONES = [
    #CASOS POSITIVOS (201) ---
    {
        "id": "ok-basico 201",
        "tail_number": "TN001",
        "model": "Boeing 737",
        "capacity": 150,
        "expected_status": 201,
        "auth": True,
        "cleanup": True,  # para borrarlo si lo deseas luego
    },
    {
        "id": "ok-minimo 201",
        "tail_number": "TN002",
        "model": "Airbus A320",
        "capacity": 1,
        "expected_status": 201,
        "auth": True,
        "cleanup": True,  # para borrarlo si lo deseas luego
    },

    # CASO NO AUTENTICADO (401) ---
    {
        "id": "unauthorized-401",
        "tail_number": "TN003",
        "model": "Cessna 172",
        "capacity": 4,
        "expected_status": 401,
        "auth": False,  # sin token → 401
    },

    #CASOS NEGATIVOS (422) ---
    {
        "id": "invalid-tail_number 422",
        "tail_number": "",  # vacío
        "model": "Boeing 747",
        "capacity": 300,
        "expected_status": 422,
        "auth": True,
    },
    {
        "id": "invalid-model-null 422",
        "tail_number": "TN005",
        "model": None,  # nulo
        "capacity": 180,
        "expected_status": 422,
        "auth": True,
    },
    {
        "id": "invalid-capacity-string 422",
        "tail_number": "TN006",
        "model": "Airbus A350",
        "capacity": "cien",  # tipo incorrecto
        "expected_status": 422,
        "auth": True,
    },

]


VUELOS = [
    {
        "id": "ok-Caso positivo 201",
        "auth": True,
        "origin": "LMN",
        "destination": "EOU",
        "departure_time": "2025-10-06T10:00:00Z",
        "arrival_time": "2025-10-06T12:00:00Z",
        "base_price": 150.0,
        "aircraft_id": "acf-5ef76b7a",   # Debe existir
        "expected_status": 201,
        "cleanup": True
    },
    {
        "id": "unauth-No autorizado 401",
        "auth": False,
        "origin": "LMN",
        "destination": "EOU",
        "departure_time": "2025-10-06T10:00:00Z",
        "arrival_time": "2025-10-06T12:00:00Z",
        "base_price": 150.0,
        "aircraft_id": "acf-f8da3c9d",
        "expected_status": 401
    },
    {
        "id": "Data invalida-422",
        "auth": True,
        "origin": "",
        "destination": "EOU",
        "departure_time": "fecha_mala",
        "arrival_time": "2025-13-99T99:99:99Z",
        "base_price": -5,
        "aircraft_id": "",
        "expected_status": 422
    },
]


BOOKINGS_CASOS = [
    {
        "id": "Booking_200",
        "auth": True,
        "expected_status": 200,      # cambia a 201 si tu API crea con 201
        "flight_id": "bkg-ec3266f3",     # se resolverá con _first_flight_id
        "passengers": [
            {"full_name": "Marco", "passport": "XP1234567", "seat": "12A"}
        ],
        "cleanup": True
    },
    {
        "id": "Booking_401",
        "auth": False,
        "expected_status": 401,
        "flight_id": "bkg-ec3266f3",
        "passengers": [
            {"full_name": "Marco", "passport": "XP1234567", "seat": "12A"}
        ],
    },
    {
        "id": "Booking_422",
        "auth": False,
        "expected_status": 422,
        "flight_id": "bkg-ec3266f3",     # mantenemos flight válido; forzamos error por contenido
        "passengers": [
            {"full_name": "", "passport": "", "seat": ""}  # inválido
        ],
    },
]



