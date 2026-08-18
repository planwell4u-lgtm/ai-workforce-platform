"""Run repository-structure checks without third-party dependencies."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DIRECTORIES = (
    "apps",
    "packages",
    "protocols",
    "config",
    "infrastructure",
    "tests",
    "scripts",
    "docs",
)
REQUIRED_FILES = (
    ".gitignore",
    ".editorconfig",
    "pyproject.toml",
    "config/local.env.example",
    "apps/README.md",
    "protocols/README.md",
)


def main() -> int:
    missing = [path for path in REQUIRED_DIRECTORIES if not (ROOT / path).is_dir()]
    missing.extend(path for path in REQUIRED_FILES if not (ROOT / path).is_file())
    if missing:
        print("Workspace check failed; missing:")
        for path in missing:
            print(f"- {path}")
        return 1

    if (ROOT / "config" / "local.env").exists():
        print("Workspace check failed: config/local.env must remain untracked and local-only.")
        return 1

    print("Workspace check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
