# config.py
from dotenv import load_dotenv
from urllib.parse import urljoin
import os
import sys

load_dotenv()

def _getenv(name: str, required: bool = True, default: str | None = None) -> str:
    val = os.environ.get(name, default)
    if required and (val is None or str(val).strip() == ""):
        sys.stderr.write(f"[config] FALTA variable de entorno: {name}\n")
        raise RuntimeError(f"Missing required environment variable: {name}")
    return str(val).strip()

# === Variables de entorno obligatorias ===
BASE_URL_API: str = _getenv("BASE_URL_API")           # p.ej. https://cf-automation-airline-api.onrender.com
ADMIN_USER_API: str = _getenv("ADMIN_USER_API")       # usuario admin
ADMIN_PASS_API: str = _getenv("ADMIN_PASS_API")       # password admin

# Normaliza BASE_URL (sin slash final)
BASE_URL_API = BASE_URL_API.rstrip("/")

# === Rutas (sin slash inicial para evitar dobles) ===
AUTH_LOGIN      = "auth/login"
AIRPORT         = "airports"
USERS           = "users"
USERS_ME        = "users/me"
FLIGHTS         = "flights"
BOOKING         = "booking"
PAYMENTS        = "payments"
AIRCRAFTS       = "aircrafts"
GLITCH_EXAMPLES = "glitch-examples"

def api_url(path: str) -> str:
    """Une BASE_URL_API + path de forma segura."""
    # Acepta path con o sin slash inicial
    path = path.lstrip("/")
    return f"{BASE_URL_API}/{path}"
