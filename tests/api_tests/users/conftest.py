import pytest
import faker
from dotenv import load_dotenv
from utils.api_helpers import api_request
from config.settings import BASE_URL_API,USERS

load_dotenv()

fake = faker.Faker()

@pytest.fixture()
def user(auth_headers,role: str = "passenger"):

    user_data = {
            "email": fake.email(),
            "password": fake.password(),
            "full_name": fake.name(),
            "role" : role
    }

    r = api_request("post", BASE_URL_API + USERS , json=user_data, headers=auth_headers)
    r.raise_for_status()
    assert r.status_code == 201
    user_created = r.json()
    yield user_created

    api_request("delete", BASE_URL_API + USERS + "{user_created['id']}", headers=auth_headers)









