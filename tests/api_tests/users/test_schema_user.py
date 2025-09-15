from jsonschema import validate

#Validar schema usuario
#email string email
#password string>= 6 characters
#full_name string
#role Expand all string

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


def test_usuario_tiene_email(user):
    assert "email" in user
