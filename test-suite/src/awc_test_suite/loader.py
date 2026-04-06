from __future__ import annotations

import hashlib
import json
from pathlib import Path

from awc_protocol import PROTOCOL_VERSION
from awc_runtime.loader.schema_loader import load_schema
from awc_runtime.loader.yaml_loader import load_yaml_file

ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = ROOT / "fixtures"
SCHEMAS_DIR = ROOT / "schemas"


def load_agent(path: str | Path) -> dict:
    return load_yaml_file(path)


def load_fixture(name: str) -> dict:
    return load_yaml_file(FIXTURES_DIR / name)


def load_json_fixture(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


def load_report_schema() -> dict:
    return load_schema("compliance-report.schema.json")


def load_local_report_schema_copy() -> dict:
    return json.loads((SCHEMAS_DIR / "compliance-report.schema.json").read_text(encoding="utf-8"))


def load_protocol_version() -> str:
    return PROTOCOL_VERSION


def declaration_digest(path: str | Path) -> str:
    data = Path(path).read_bytes()
    return hashlib.sha256(data).hexdigest()
