# config.py
from dotenv import load_dotenv, find_dotenv
import os, sys

# Carga .env sin depender del cwd
load_dotenv(find_dotenv(usecwd=True), override=False)

def _getenv(name: str, required: bool = True, default: str | None = None) -> str:
    val = os.environ.get(name, default)
    if required and (val is None or str(val).strip() == ""):
        sys.stderr.write(f"[config] FALTA variable de entorno: {name}\n")
        raise RuntimeError(f"Missing required environment variable: {name}")
    return str(val).strip()

BASE_URL_API   = _getenv("BASE_URL_API")  # ej: https://cf-automation-airline-api.onrender.com
ADMIN_USER_API = _getenv("ADMIN_USER_API")
ADMIN_PASS_API = _getenv("ADMIN_PASS_API")

BASE_URL_API = BASE_URL_API.rstrip("/")

# Endpoints (sin slash inicial)
AUTH_LOGIN = "auth/login"      # si tu API exige slash final, probaremos fallback
USERS      = "users"
USERS_ME   = "users/me"
AIRPORTS   = "airports"
AIRCRAFTS = "aircrafts"
