"""Deployable WSGI entry point with health and graceful shutdown."""

from __future__ import annotations

from wsgiref.simple_server import make_server

from .app import create_app


def main() -> None:
    app = create_app()
    try:
        with make_server("0.0.0.0", 8080, app) as server:
            server.serve_forever()
    finally:
        app.close()


if __name__ == "__main__":
    main()
