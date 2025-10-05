#Validar creación de Aircraft
def test_airport(aircraft):
    # airport es el JSON creado por el fixture
    assert "id" in aircraft and aircraft["id"]
    assert aircraft["model"] != ""
