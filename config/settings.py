# config central, tipada y validada

from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL_API = os.environ.get("BASE_URL_API")
ADMIN_USER_API = os.environ.get("ADMIN_USER_API")
ADMIN_PASS_API = os.environ.get("ADMIN_PASS_API")

AUTH_LOGIN = "/auth/login/"
AIRPORT="/airports"
USERS="/users"



