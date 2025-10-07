from utils.schemas import  user_schema
import pytest
from jsonschema import Draft7Validator, FormatChecker  # <-- añade FormatChecker

validator = Draft7Validator(user_schema)


# activar format_checker para validar emails
validator = Draft7Validator(user_schema, format_checker=FormatChecker())

def _errors(instance: dict):
    return list(validator.iter_errors(instance))

def _readable(errors):
    return [f"({'.'.join(map(str, e.path)) or '(root)'}) {e.message} [validator={e.validator}]"
            for e in errors]

# CASOS POSITIVOS
valid_cases = [
    {"id": "usr-001", "email": "juan@example.com", "full_name": "Juan Pérez", "role": "admin"},
    {"id": "usr-002", "email": "ana@example.com", "full_name": "Ana García", "role": "passenger", "phone": "999999999"},
]

@pytest.mark.parametrize("payload", valid_cases, ids=["admin", "passenger"])
def test_user_schema_valid(payload):
    errs = _errors(payload)
    assert not errs, f"No debería fallar. Errores: {_readable(errs)}"

# CASOS NEGATIVOS
invalid_cases = [
    pytest.param({"id": 123, "email": "juan@example.com", "full_name": "Juan Pérez", "role": "admin"},
                 "id", "type", id="id-not-string"),
    pytest.param({"id": "usr-004", "email": "noemail", "full_name": "Juan Pérez", "role": "admin"},
                 "email", "format", id="email-missing-at"),
    pytest.param({"id": "usr-006", "email": "maria@example.com", "full_name": "María López", "role": "manager"},
                 "role", "enum", id="role-invalid-value"),
    pytest.param({"email": "test@example.com", "full_name": "Carlos Torres", "role": "admin"},
                 "(root)", "required", id="missing-id"),
    pytest.param({"id": "usr-007", "full_name": "Carlos Torres", "role": "admin"},
                 "(root)", "required", id="missing-email"),
    pytest.param({"id": "usr-008", "email": "carlos@example.com", "role": "admin"},
                 "(root)", "required", id="missing-full_name"),
    pytest.param({"id": "usr-009", "email": "carlos@example.com", "full_name": "Carlos Torres"},
                 "(root)", "required", id="missing-role"),
]

@pytest.mark.parametrize("payload, expected_path, expected_validator", invalid_cases)
def test_user_schema_invalid(payload, expected_path, expected_validator):
    errs = _errors(payload)
    assert errs, "Se esperaban errores de validación."
    def path_of(e):
        return ".".join(map(str, e.path)) or "(root)"
    matched = any(path_of(e) == expected_path and e.validator == expected_validator for e in errs)
    assert matched, f"No se encontró error esperado path={expected_path}, validator={expected_validator}. Errores: {_readable(errs)}"