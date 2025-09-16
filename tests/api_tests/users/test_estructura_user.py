from jsonschema import validate

#Pruebas Positivas : Creación/Validación de recursos adecuadamente
#Pruebas CONTRATO: Estructura
#Pruebas STATUS CODE 201,422
#Pruebas TIPOS DE DATOS
#Pruebas Entradas validas y extremas

#Pruebas CONTRATO: Estructura
user_schema = {
    "type": "object",
    "required": ["id","email", "full_name", "role"],
    "properties": {
        "id": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "full_name": {"type": "string"},
        "role": {"type": "string", "enum": ["admin", "passenger"]},
    },
    "additionalProperties": True,
}

def test_create_user_schema(user):
    validate(instance=user, schema=user_schema)





