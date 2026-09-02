"""Check the local backend and frontend runtime endpoints without sending user data."""

from __future__ import annotations

import argparse
import json
import sys
from urllib.error import URLError
from urllib.request import urlopen


REQUIRED_RUNTIME_CONFIG_KEYS = frozenset(
    {"auth0Domain", "auth0ClientId", "auth0Audience", "apiBaseUrl"}
)


def _get(url: str) -> bytes:
    try:
        with urlopen(url, timeout=10) as response:
            if response.status != 200:
                raise RuntimeError(f"{url} returned HTTP {response.status}")
            return response.read()
    except URLError as error:
        raise RuntimeError(f"{url} is unavailable") from error


def _check_runtime_config(url: str) -> None:
    try:
        config = json.loads(_get(url))
    except json.JSONDecodeError as error:
        raise RuntimeError(f"{url} did not return JSON") from error
    if not isinstance(config, dict):
        raise RuntimeError(f"{url} did not return a JSON object")
    missing = sorted(
        key
        for key in REQUIRED_RUNTIME_CONFIG_KEYS
        if not isinstance(config.get(key), str) or not config[key].strip()
    )
    if missing:
        raise RuntimeError(f"{url} is missing runtime configuration: {', '.join(missing)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend-url", default="http://localhost:8080/healthz")
    parser.add_argument("--frontend-url", default="http://localhost:3000/runtime-config")
    arguments = parser.parse_args()
    try:
        _get(arguments.backend_url)
        _check_runtime_config(arguments.frontend_url)
    except RuntimeError as error:
        print(f"Local runtime check failed: {error}", file=sys.stderr)
        return 1
    print("Local runtime check passed: backend health and frontend configuration are ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
