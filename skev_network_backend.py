"""
skev.network — Python Transpiler Backend
Copyright © 2026 AJ. All Rights Reserved. skev.dev

Uses Python's built-in urllib — zero external dependencies.
In the real Skev compiler this uses native async I/O.
"""
import urllib.request as _req
import urllib.parse   as _parse
import urllib.error   as _err
import socket         as _sock
import json           as _json
from skev_runtime import succeed, fail

class NetworkError:
    timeout            = "timeout"
    connection_refused = "connection_refused"
    dns_failed         = "dns_failed"
    ssl_error          = "ssl_error"
    invalid_url        = "invalid_url"
    server_error       = "server_error"
    parse_error        = "parse_error"
    auth_failed        = "auth_failed"

class HttpResponse:
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body        = body
        self.ok          = 200 <= status_code <= 299

    def __repr__(self):
        return f"HttpResponse(status={self.status_code}, ok={self.ok})"

def _make_request(url, method="GET", body=None, auth_token=None, timeout=5):
    try:
        url = str(url)
        headers = {
            "User-Agent":   "skev/1.0",
            "Content-Type": "application/json",
            "Accept":       "application/json",
        }
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        data = body.encode("utf-8") if body else None
        request = _req.Request(url, data=data, headers=headers, method=method)

        with _req.urlopen(request, timeout=timeout) as resp:
            body_text = resp.read().decode("utf-8", errors="replace")
            return succeed(HttpResponse(resp.status, body_text))

    except _err.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return succeed(HttpResponse(e.code, body_text))
    except _err.URLError as e:
        reason = str(e.reason)
        if "timed out"      in reason: return fail(NetworkError.timeout)
        if "Name or service" in reason: return fail(NetworkError.dns_failed)
        if "Connection refused" in reason: return fail(NetworkError.connection_refused)
        if "SSL"            in reason: return fail(NetworkError.ssl_error)
        return fail(NetworkError.connection_refused)
    except _sock.timeout:
        return fail(NetworkError.timeout)
    except ValueError:
        return fail(NetworkError.invalid_url)
    except Exception:
        return fail(NetworkError.server_error)

def http_get(url):
    return _make_request(str(url), method="GET")

def http_get_headers(url, auth_token):
    return _make_request(str(url), method="GET", auth_token=str(auth_token))

def http_post(url, body, auth_token=""):
    return _make_request(str(url), method="POST",
                         body=str(body),
                         auth_token=str(auth_token) if auth_token else None)

def http_put(url, body, auth_token=""):
    return _make_request(str(url), method="PUT",
                         body=str(body),
                         auth_token=str(auth_token) if auth_token else None)

def http_delete(url, auth_token=""):
    return _make_request(str(url), method="DELETE",
                         auth_token=str(auth_token) if auth_token else None)

def is_online():
    try:
        _req.urlopen("https://skev.dev", timeout=2)
        return True
    except:
        try:
            _sock.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except:
            return False

def url_encode(s):
    return _parse.quote(str(s), safe="")

def build_query(pairs):
    if len(pairs) % 2 != 0:
        return ""
    parts = []
    for i in range(0, len(pairs), 2):
        k = _parse.quote(str(pairs[i]),   safe="")
        v = _parse.quote(str(pairs[i+1]), safe="")
        parts.append(f"{k}={v}")
    return "&".join(parts)
