#Pruebas STATUS CODE 201,422
#Pruebas TIPOS DE DATOS
#Pruebas Entradas validas y extremas


#Pruebas Positivas : Creación/Validación de recursos adecuadamente
def test_create_user_completo(user):
    body = user

    email = body.get("email")
    assert isinstance(email, str), "email debe ser string"
    assert email.strip(), "email vacío o solo espacios"

    full_name = body.get("full_name")
    assert isinstance(full_name, str), "full_name debe ser string"
    assert full_name.strip(), "full_name vacío o solo espacios"

    role = body.get("role")
    assert isinstance(role, str), "role debe ser string"
    assert role.strip(), "role vacío o solo espacios"

    uid = body.get("id") or body.get("_id")
    assert uid not in (None, ""), f"Respuesta sin id: {body}"


