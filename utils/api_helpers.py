import os, time, random, requests
from urllib.parse import urlparse

BASE = os.getenv("BASE_URL_API")
RETRIES = 3
BACKOFF = 0.5

def _join(base: str, path: str) -> str:
    return f"{base.rstrip('/')}/{path.lstrip('/')}"

def api_request(method: str, path_or_url: str, *, timeout=(5,15), **kw) -> requests.Response:
    method = method.upper()
    # Si viene URL absoluta, úsala tal cual; si no, une BASE + path.
    parsed = urlparse(path_or_url)
    if parsed.scheme in ("http", "https"):
        url = path_or_url
    else:
        if not BASE:
            raise RuntimeError("BASE_URL_API no está configurada y se recibió un path relativo")
        url = _join(BASE, path_or_url)

    last_exc = None
    for i in range(RETRIES):
        try:
            resp = requests.request(method, url, timeout=timeout, **kw)
        except requests.RequestException as e:
            last_exc = e
            if i < RETRIES - 1:
                time.sleep(BACKOFF * (2**i) + random.uniform(0, 0.2))
                continue
            raise
        # Reintenta solo en 5xx
        if 500 <= resp.status_code < 600 and i < RETRIES - 1:
            time.sleep(BACKOFF * (2**i) + random.uniform(0, 0.2))
            continue
        return resp
    # Si llegara aquí con excepción capturada:
    if last_exc:
        raise last_exc



