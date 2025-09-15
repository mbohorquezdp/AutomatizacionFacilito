
from jsonschema import validate

#Validar creación de Airport
def test_airport(airport):
    # airport es el JSON creado por el fixture
    assert "iata_code" in airport and airport["iata_code"]
    assert airport["city"] != ""


def test_admin_token(admin_token):
    assert isinstance(admin_token, str) and admin_token  # no vacío


