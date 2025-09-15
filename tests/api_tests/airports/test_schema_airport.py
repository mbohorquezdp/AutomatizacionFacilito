from jsonschema import validate

#Validar Schemas
#iata_codestringmatches ^[A-Z]{3}$
#citystring
#countrystring
airport_schema = {
    "type" : "object",
    "required": ["iata_code","city","country"],
    "properties" : {
        "iata_code": {"type": "string","minLength":3,"maxLength":3},
        "city": {"type": "string"},
        "country": {"type": "string"},
    },
    "addtionalProperties":False
}

#Validar estructura Schema
def test_create_airport_schema(airport):
    validate(instance=airport, schema=airport_schema)