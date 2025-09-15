import random
import string

import pytest
import requests
import faker
from dotenv import load_dotenv

from config.settings import BASE_URL_API,AIRPORT
from utils.api_helpers import api_request

load_dotenv()
fake = faker.Faker()

#Creación de Airport
@pytest.fixture
def airport(auth_headers):
    airport_data = {
            "iata_code": "".join(random.choices(string.ascii_uppercase,k=3)),
            "city": fake.country(),
            "country": fake.country_code()
        }

    r = api_request("post", BASE_URL_API + AIRPORT, json=airport_data, headers=auth_headers)

    r.raise_for_status()
    airport_response = r.json()
    yield airport_response
    r = api_request("delete", BASE_URL_API + AIRPORT + '{airport_response["iata_code"]}', headers=auth_headers
                    )
    #requests.delete(BASE_URL_API + AIRPORT + '{airport_response["iata_code"]}',headers=auth_headers,timeout=5)











