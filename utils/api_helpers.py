import os
import time, random, requests
from urllib.parse import urlparse
import config.settings as config

class ApiClient:
    RETRIES = 7
    BACKOFF = 0.9
    TIMEOUT = (5, 15)

    def __init__(self, base_url: str | None = None, verify_ssl: bool | None = None):
        self.base_url = (base_url or config.BASE_URL_API).rstrip("/")
        if not self.base_url:
            raise RuntimeError("ApiClient: base_url vacío. Revisa BASE_URL_API en .env")
        self.session = requests.Session()
        self.session.headers.update({"accept": "application/json"})
        # Permite controlar verificación SSL por env si te hace falta:
        self.verify_ssl = True if verify_ssl is None else bool(verify_ssl)

    def url(self, path_or_url: str) -> str:
        parsed = urlparse(path_or_url)
        if parsed.scheme in ("http", "https"):
            return path_or_url
        return f"{self.base_url}/{path_or_url.lstrip('/')}"

    def _request(self, method: str, path_or_url: str, **kw) -> requests.Response:
        url = self.url(path_or_url)
        kw.setdefault("timeout", self.TIMEOUT)
        kw.setdefault("verify", self.verify_ssl)
        last_exc = None
        for i in range(self.RETRIES):
            try:
                resp = self.session.request(method.upper(), url, **kw)
            except requests.RequestException as e:
                last_exc = e
                if i < self.RETRIES - 1:
                    time.sleep(self.BACKOFF * (2**i) + random.uniform(0, 0.2))
                    continue
                # Log útil antes de lanzar
                raise RuntimeError(f"HTTP {method.upper()} {url} falló: {e}") from e

            # Reintenta solo 5xx
            if 500 <= resp.status_code < 600 and i < self.RETRIES - 1:
                time.sleep(self.BACKOFF * (2**i) + random.uniform(0, 0.2))
                continue

            return resp

        if last_exc:
            raise last_exc

    # Métodos públicos
    def get(self, path_or_url: str, **kw):    return self._request("GET", path_or_url, **kw)
    def post(self, path_or_url: str, **kw):   return self._request("POST", path_or_url, **kw)
    def put(self, path_or_url: str, **kw):    return self._request("PUT", path_or_url, **kw)
    def delete(self, path_or_url: str, **kw): return self._request("DELETE", path_or_url, **kw)

    def login_admin(self) -> str:
        # Lee credenciales desde config o env
        try:
            import config
            username = getattr(config, "ADMIN_USER_API", os.getenv("ADMIN_USER_API"))
            password = getattr(config, "ADMIN_PASS_API", os.getenv("ADMIN_PASS_API"))
            login_path = getattr(config, "AUTH_LOGIN", "auth/login")
        except Exception:
            username = os.getenv("ADMIN_USER_API")
            password = os.getenv("ADMIN_PASS_API")
            login_path = "auth/login"

        if not username or not password:
            raise RuntimeError("Faltan credenciales ADMIN_USER_API/ADMIN_PASS_API")

        candidates = []

        # Con/sin slash final
        paths = [login_path.rstrip("/"), f"{login_path.rstrip('/')}/"]

        # 1) JSON email/password
        for p in paths:
            candidates.append(("POST", p, {"json": {"email": username, "password": password}}))

        # 2) JSON username/password
        for p in paths:
            candidates.append(("POST", p, {"json": {"username": username, "password": password}}))

        # 3) FORM username/password
        for p in paths:
            candidates.append(("POST", p, {
                "data": {"username": username, "password": password},
                "headers": {"Content-Type": "application/x-www-form-urlencoded"}
            }))

        # 4) FORM OAuth2 style
        for p in paths:
            candidates.append(("POST", p, {
                "data": {"username": username, "password": password, "grant_type": "password"},
                "headers": {"Content-Type": "application/x-www-form-urlencoded"}
            }))

        last_resp: requests.Response | None = None
        last_error_detail = ""

        for method, path, kw in candidates:
            resp = self._request(method, path, **kw)
            last_resp = resp

            if resp.status_code in (200, 201):
                try:
                    data = resp.json()
                except Exception:
                    raise ValueError(f"Login OK pero body no es JSON: {resp.text}")

                token = data.get("access_token") or data.get("token")
                if not token:
                    # algunos devuelven {access_token:..., token_type: bearer}
                    # o {jwt: ...}
                    token = data.get("jwt")
                if not token:
                    raise ValueError(f"Login OK pero no vino token en el body: {data}")

                self.session.headers.update({"Authorization": f"Bearer {token}"})
                return token

            # Si 422, guarda detalle para diagnóstico
            if resp.status_code == 422:
                try:
                    last_error_detail = json.dumps(resp.json(), ensure_ascii=False)
                except Exception:
                    last_error_detail = resp.text

        # Si ninguno funcionó:
        if last_resp is not None:
            if last_resp.status_code == 422:
                raise requests.HTTPError(
                    f"422 en login. La API rechazó el payload. Detalle: {last_error_detail} | "
                    f"URL usada: {last_resp.url}"
                )
            else:
                raise requests.HTTPError(
                    f"Login falló. Último status {last_resp.status_code} ({last_resp.reason}) "
                    f"para URL: {last_resp.url}. Body: {last_resp.text}"
                )

        raise RuntimeError("No se pudo ejecutar ninguna variante de login.")



from typing import Any, Dict, Tuple, List, Optional

class VectorUtils:
    def __init__(self, allowed_fields: Optional[set] = None):
        #allowed_fields: conjunto de campos válidos para armar el payload.
        #Si no se pasa, acepta todos los campos.

        self.allowed_fields = allowed_fields

    def build_payload(self, case: Dict[str, Any]) -> Dict[str, Any]:
        #Construye el payload para la API filtrando solo los campos permitidos.

        if not self.allowed_fields:
            return {k: v for k, v in case.items()}
        return {k: v for k, v in case.items() if k in self.allowed_fields}

    def normalize_expected(self, case: Dict[str, Any]) -> Tuple[int | None, List[int] | None]:
        #Devuelve (expected_status, expected_status_any).
        #Soporta tanto 'expected_status'/'expected_status_any'
        #como 'Resultado esperado XYZ': XYZ.

        #Caso estándar
        if "expected_status" in case:
            try:
                return int(case["expected_status"]), None
            except Exception:
                pass

        if "expected_status_any" in case and isinstance(case["expected_status_any"], list):
            try:
                return None, [int(x) for x in case["expected_status_any"]]
            except Exception:
                pass

        #Soporte "Resultado esperado ..."
        for k, v in case.items():
            if isinstance(k, str) and k.lower().startswith("resultado esperado"):
                try:
                    return int(v), None
                except Exception:
                    break

        return None, None


from jsonschema import validate, ValidationError
import pytest

class SchemaValidator:
    #Helper genérico para validar respuestas API contra esquemas JSON."""

    @staticmethod
    def assert_schema(instance: dict, schema: dict, *, msg: str = ""):
        #Valida un diccionario contra un schema JSON.
        #Si no cumple, lanza pytest.fail con detalle.

        try:
            validate(instance=instance, schema=schema)
        except ValidationError as e:
            pytest.fail(
                f"Validación de schema falló: {e.message}\n"
                f"Path: {'/'.join(map(str, e.path))}\n"
                f"Schema path: {'/'.join(map(str, e.schema_path))}\n"
                f"Respuesta: {instance}\n"
                f"{msg}"
            )

