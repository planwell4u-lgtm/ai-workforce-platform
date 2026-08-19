"""Structural checks for the B0 repository foundation."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class WorkspaceBoundaryTests(unittest.TestCase):
    def test_required_workspace_areas_exist(self) -> None:
        for area in (
            "apps",
            "packages",
            "protocols",
            "config",
            "infrastructure",
            "tests",
            "scripts",
            "docs",
        ):
            self.assertTrue((ROOT / area).is_dir(), f"missing workspace area: {area}")

    def test_safe_local_configuration_example_exists(self) -> None:
        example = ROOT / "config" / "local.env.example"
        self.assertTrue(example.is_file())
        self.assertNotRegex(example.read_text(encoding="utf-8"), r"(?m)^SECRET=")

    def test_shared_package_has_no_domain_or_provider_dependency(self) -> None:
        shared_source = ROOT / "packages" / "shared" / "python" / "src"
        prohibited = ("fastapi", "sqlalchemy", "livekit", "twilio", "openai")
        for source_file in shared_source.rglob("*.py"):
            content = source_file.read_text(encoding="utf-8").lower()
            for dependency in prohibited:
                self.assertNotIn(
                    dependency, content, f"{source_file} imports or names {dependency}"
                )
