
#Validar creación de usuario
def test_created_user(user):
    # user es el JSON creado por el fixture
    assert user["email"] != ""

