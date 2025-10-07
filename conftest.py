
import pytest
import faker
import requests
from dotenv import load_dotenv

from config.settings import BASE_URL_API,ADMIN_USER_API,ADMIN_PASS_API,AUTH_LOGIN

load_dotenv()

fake = faker.Faker()

#Obtener Token
@pytest.fixture(scope="session")
def admin_token() -> str:

    r = requests.post(BASE_URL_API + AUTH_LOGIN,
                      data = {"username": ADMIN_USER_API,"password": ADMIN_PASS_API},timeout=5)
    r.raise_for_status()
    return r.json()["access_token"]

#Obtener Autorización
@pytest.fixture
def auth_headers(admin_token):
    headers = {"Authorization": "Bearer {}".format(admin_token)}
    return headers








