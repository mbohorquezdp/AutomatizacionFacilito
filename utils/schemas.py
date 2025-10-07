#SCHEMAS PARA VALIDACIONES

user_schema = {
    "type": "object",
    "required": ["id", "email", "full_name", "role"],
    "properties": {
        "id": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "full_name": {"type": "string"},
        "role": {"type": "string", "enum": ["admin", "passenger"]},
    },
    "additionalProperties": True,
}

airport_schema = {
    "type": "object",
    "required": ["iata_code", "city", "country"],
    "properties": {
        "iata_code": {
            "type": "string",
            "pattern": "^[A-Z]{3}$"   # Solo 3 letras mayúsculas (ej: LIM)
        },
        "city": {
            "type": "string",
            "minLength": 1
        },
        "country": {
            "type": "string",
            "minLength": 1
        }
    },
    "additionalProperties": False
}