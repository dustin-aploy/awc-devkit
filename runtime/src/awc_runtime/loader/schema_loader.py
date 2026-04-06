from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources
from pathlib import Path


class ProtocolDependencyError(RuntimeError):
    """Raised when the runtime cannot load protocol assets."""


def _protocol_package_root() -> str:
    try:
        import awc_protocol  # noqa: F401
        return "awc_protocol"
    except ImportError as exc:
        raise ProtocolDependencyError(
            "awc_protocol is not installed. Install ../../awc-spec first."
        ) from exc


@lru_cache(maxsize=None)
def load_schema(name: str) -> dict:
    package = _protocol_package_root()
    schema_path = resources.files(package) / "schemas" / name
    return json.loads(schema_path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_protocol_version() -> str:
    try:
        from awc_protocol import PROTOCOL_VERSION
    except ImportError as exc:
        raise ProtocolDependencyError(
            "awc_protocol is not installed. Install ../../awc-spec first."
        ) from exc
    return PROTOCOL_VERSION


def resolve_schema_path(name: str) -> Path:
    package = _protocol_package_root()
    schema_path = resources.files(package) / "schemas" / name
    return Path(str(schema_path))
