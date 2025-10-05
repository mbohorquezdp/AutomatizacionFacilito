
from utils.api_helpers import api_request
from config.settings import BASE_URL_API, AIRCRAFTS



def test_borrar_un_AIRCRAFT(auth_headers):
    delete_AIRCRAFT("acf-64a72aec", auth_headers)  # reemplaza por el id real

    # Validar creación de Aircraft
    def test_airport(aircraft):
        # airport es el JSON creado por el fixture
        assert "id" in aircraft and aircraft["id"]
        assert aircraft["model"] != ""