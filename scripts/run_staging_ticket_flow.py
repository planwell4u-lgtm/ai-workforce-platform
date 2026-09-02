"""Run one interactive Auth0-to-Supabase FAQ support-answer staging verification flow."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import secrets
import time
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from typing import ClassVar
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

from ai_workforce_backend.app import create_app


class CallbackHandler(BaseHTTPRequestHandler):
    code: ClassVar[str | None] = None
    state: ClassVar[str | None] = None
    error: ClassVar[str | None] = None
    error_description: ClassVar[str | None] = None

    def do_GET(self) -> None:
        values = parse_qs(urlparse(self.path).query)
        code = values.get("code", [None])[0]
        state = values.get("state", [None])[0]
        if urlparse(self.path).path != "/callback":
            self.send_error(404)
            return
        type(self).state = state
        type(self).error = values.get("error", [None])[0]
        type(self).error_description = values.get("error_description", [None])[0]
        if type(self).error:
            body = b"Authentication failed. Return to Codex for the safe error category."
            self.send_response(400)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if not code or not state:
            self.send_error(400)
            return
        type(self).code = code
        body = b"Authentication complete. You can close this tab and return to Codex."
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client-id", required=True, help="Auth0 SPA client ID")
    parser.add_argument(
        "--result-file", required=True, help="Local JSON output path; never contains a token"
    )
    arguments = parser.parse_args()
    domain = _required_environment("AUTH0_DOMAIN")
    audience = _required_environment("AUTH0_AUDIENCE")
    redirect_uri = "http://localhost:8765/callback"
    verifier = secrets.token_urlsafe(64)
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    )
    state = secrets.token_urlsafe(32)
    query = urlencode(
        {
            "response_type": "code",
            "client_id": arguments.client_id,
            "redirect_uri": redirect_uri,
            "scope": "openid profile agent.context.read",
            "audience": audience,
            "state": state,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        }
    )
    CallbackHandler.code = None
    CallbackHandler.state = None
    CallbackHandler.error = None
    CallbackHandler.error_description = None
    server = HTTPServer(("127.0.0.1", 8765), CallbackHandler)
    print("Opening Auth0 sign-in in your browser. Sign in with the verified staging user.")
    webbrowser.open(f"https://{domain}/authorize?{query}")
    server.timeout = 1
    deadline = time.monotonic() + 300
    while (
        CallbackHandler.code is None
        and CallbackHandler.error is None
        and time.monotonic() < deadline
    ):
        server.handle_request()
    server.server_close()
    if CallbackHandler.error:
        _write_result(
            {
                "outcome": "auth_failed",
                "reason": CallbackHandler.error,
                "detail": CallbackHandler.error_description,
            },
        )
        raise SystemExit("Auth0 denied the authorization request")
    if CallbackHandler.state != state or CallbackHandler.code is None:
        _write_result(
            arguments.result_file, {"outcome": "runner_error", "reason": "callback_invalid"}
        )
        raise SystemExit("sign-in was cancelled, expired, or failed state validation")
    token_permissions: list[str] = []
    try:
        access_token = _exchange_code(
            domain, arguments.client_id, redirect_uri, verifier, CallbackHandler.code
        )
        token_permissions = _safe_token_permissions(access_token)
        result = _submit_support_question(access_token)
    except Exception as error:
        _write_result(
            arguments.result_file,
            {
                "outcome": "runner_error",
                "reason": type(error).__name__,
                "token_permissions": token_permissions,
            },
        )
        raise
    _write_result(arguments.result_file, result)
    print("Staging flow completed. Result written to the configured local result file.")


def _required_environment(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"{name} is required")
    return value


def _write_result(path: str, result: object) -> None:
    with open(path, "w", encoding="utf-8") as result_file:
        json.dump(result, result_file, separators=(",", ":"))


def _exchange_code(domain: str, client_id: str, redirect_uri: str, verifier: str, code: str) -> str:
    body = json.dumps(
        {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "code": code,
            "redirect_uri": redirect_uri,
            "code_verifier": verifier,
        }
    ).encode()
    request = Request(
        f"https://{domain}/oauth/token",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=15) as response:
        token = json.loads(response.read().decode()).get("access_token")
    if not isinstance(token, str) or not token:
        raise SystemExit("Auth0 did not return an API access token")
    return token


def _safe_token_permissions(access_token: str) -> list[str]:
    """Return only non-secret scope names for local staging diagnostics."""
    claims_segment = access_token.split(".")[1]
    claims = json.loads(base64.urlsafe_b64decode(claims_segment + "=" * (-len(claims_segment) % 4)))
    scope = claims.get("scope", "")
    permissions = claims.get("permissions", [])
    names = scope.split() if isinstance(scope, str) else []
    if isinstance(permissions, list):
        names.extend(value for value in permissions if isinstance(value, str))
    return sorted(set(names))


def _submit_support_question(access_token: str) -> object:
    marker = uuid.uuid4().hex[:12]
    payload = json.dumps(
        {
            "agent_ref": "customer-support-worker",
            "session_ref": f"staging-verification-{marker}",
            "event_ref": f"staging-event-{marker}",
            "sequence": 1,
            "question": "How can I reset my password?",
        }
    ).encode()
    captured: dict[str, object] = {}

    def start_response(status: str, headers: list[tuple[str, str]]) -> None:
        captured["status"] = status

    app = create_app()
    try:
        body = b"".join(
            app(
                {
                    "REQUEST_METHOD": "POST",
                    "PATH_INFO": "/v1/support-answers",
                    "HTTP_AUTHORIZATION": f"Bearer {access_token}",
                    "CONTENT_LENGTH": str(len(payload)),
                    "wsgi.input": BytesIO(payload),
                },
                start_response,
            )
        )
    finally:
        app.close()
    response = json.loads(body)
    if captured["status"] != "200 OK":
        raise RuntimeError(f"staging flow failed: {captured['status']} {response}")
    return response


if __name__ == "__main__":
    main()
