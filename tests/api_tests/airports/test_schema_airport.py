import pytest
from jsonschema import Draft7Validator
from utils.schemas import airport_schema

validator = Draft7Validator(airport_schema)

def _errors(instance: dict):
    return list(validator.iter_errors(instance))

def _readable(errors):
    return [f"({'.'.join(map(str, e.path)) or '(root)'}) {e.message} [validator={e.validator}]"
            for e in errors]


#CASOS POSITIVOS
valid_cases = [
    {"iata_code": "LIM", "city": "Lima", "country": "Peru"},
    {"iata_code": "JFK", "city": "New York", "country": "USA"},
]

@pytest.mark.parametrize("payload", valid_cases, ids=["LIM", "JFK"])
def test_airport_schema_valid(payload):
    errs = _errors(payload)
    assert not errs, f"No debería fallar. Errores: {_readable(errs)}"


#CASOS NEGATIVOS
invalid_cases = [
    # iata_code: longitud incorrecta
    pytest.param({"iata_code": "LI", "city": "Lima", "country": "Peru"},
                 "iata_code", "pattern", id="iata-2-caracteres"),
    pytest.param({"iata_code": "LIMA", "city": "Lima", "country": "Peru"},
                 "iata_code", "pattern", id="iata-4-caracteres"),
    # city / country vacíos
    pytest.param({"iata_code": "LIM", "city": "", "country": "Peru"},
                 "city", "minLength", id="city-empty"),
    pytest.param({"iata_code": "LIM", "city": "Lima", "country": ""},
                 "country", "minLength", id="country-Vacia sin datos"),
    # tipos incorrectos
    pytest.param({"iata_code": 123, "city": "Lima", "country": "Peru"},
                 "iata_code", "type", id="iata-No string"),
    pytest.param({"iata_code": "LIM", "city": 100, "country": "Peru"},
                 "city", "type", id="city-no string"),
    # faltan campos requeridos
    pytest.param({"city": "Lima", "country": "Peru"},
                 "(root)", "required", id="Faltan campos requeridos iata"),
    pytest.param({"iata_code": "LIM", "country": "Peru"},
                 "(root)", "required", id="Faltan campos requeridos city"),
    pytest.param({"iata_code": "LIM", "city": "Lima"},
                 "(root)", "required", id="Falta campos requeridos country"),

]

@pytest.mark.parametrize("payload, expected_path, expected_validator", invalid_cases)
def test_airport_schema_invalid(payload, expected_path, expected_validator):
    errs = _errors(payload)
    assert errs, "Se esperaban errores de validación."
    # Buscar al menos un error que coincida con path y validador esperados
    def path_of(e):
        return ".".join(map(str, e.path)) or "(root)"
    matched = any(path_of(e) == expected_path and e.validator == expected_validator for e in errs)
    assert matched, f"No se encontró error esperado path={expected_path}, validator={expected_validator}. Errores: {_readable(errs)}"