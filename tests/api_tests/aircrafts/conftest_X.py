
import pytest
import faker
from dotenv import load_dotenv

from config.settings import BASE_URL_API, AIRCRAFTS
from utils.api_helpers import api_request

load_dotenv()
fake = faker.Faker()

#Creación de aircraft
@pytest.fixture
def aircraft(auth_headers):
    aircraft_data = {
            "tail_number": "string",
            "model": "string",
            "capacity": 0
        }

    r = api_request("post", BASE_URL_API + AIRCRAFTS, json=aircraft_data, headers=auth_headers)

    r.raise_for_status()
    aircraft_response = r.json()
    yield aircraft_response
    r = api_request("delete", BASE_URL_API + AIRCRAFTS + '{aircraft_response["id]}', headers=auth_headers   )













