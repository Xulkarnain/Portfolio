
from starlette.requests import Request
from fastapi import HTTPException

from app.api.dependencies import require_admin_origin


def make_request(origin=None):
    headers = []

    if origin is not None:
        headers.append((b"origin", origin.encode("utf-8")))

    scope = {
        "type": "http",
        "asgi": {
            "version": "3.0",
            "spec_version": "2.3",
        },
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/test",
        "raw_path": b"/test",
        "query_string": b"",
        "headers": headers,
        "client": ("127.0.0.1", 12345),
        "server": ("127.0.0.1", 8000),
    }

    return Request(scope)


def test_origin(origin):
    try:
        require_admin_origin(make_request(origin))
        return "Accepted"
    except HTTPException as exc:
        return f"Rejected ({exc.status_code})"


print("Localhost:", test_origin("http://localhost:5500"))
print("127.0.0.1:", test_origin("http://127.0.0.1:5500"))
print("Production frontend:", test_origin("https://zulkarnain.vercel.app"))
print("Untrusted origin:", test_origin("https://attacker.example"))
print("Missing origin:", test_origin(None))
