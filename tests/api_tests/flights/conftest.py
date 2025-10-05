import pytest
import faker
from dotenv import load_dotenv
from selenium.webdriver.support.expected_conditions import none_of

from config.settings import BASE_URL_API,FLIGHTS
from tests.api_tests.flights.test_create_flight import _iso_now_plus
from utils.api_helpers import api_request

load_dotenv()
fake = faker.Faker()

#Creación de Flights
@pytest.fixture
def flights(auth_headers):
    flights_data = {
        "origin": "MYK",
        "destination": "MMQ",
        "departure_time": _iso_now_plus(1),
        "arrival_time": _iso_now_plus(4),   # llegada > salida
        "base_price": 199.99,               # number
        }

    r = api_request("post", BASE_URL_API + FLIGHTS, json=flights_data, headers=auth_headers)

    r.raise_for_status()
    flights_response = r.json()
    yield flights_response
    r = api_request("delete", BASE_URL_API + FLIGHTS + '{flights_response["flight_id"]}', headers=auth_headers   )



#Validar creación de Airport
def test_flight(flights):
    # airport es el JSON creado por el fixture
    assert "flight_id" in flights and flights["flight_id"]
    assert flights["destination"] != ""











