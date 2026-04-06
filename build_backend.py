"""Minimal offline build backend for the grouped awc-devkit package."""

from __future__ import annotations

import base64
import csv
import hashlib
from io import StringIO
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
DIST_NAME = "awc_devkit"
PROJECT_NAME = "awc-devkit"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
DIST_INFO = f"{DIST_NAME}-{VERSION}.dist-info"
WHEEL_NAME = f"{DIST_NAME}-{VERSION}-py3-none-any.whl"


def _metadata_text() -> str:
    return "\n".join(
        [
            "Metadata-Version: 2.1",
            f"Name: {PROJECT_NAME}",
            f"Version: {VERSION}",
            "Summary: Grouped developer toolkit workspace for AI Work Contract (AWC), formerly ARP.",
            "Requires-Python: >=3.10",
            "License: Apache-2.0",
            "",
        ]
    )


def _wheel_text() -> str:
    return "\n".join(
        [
            "Wheel-Version: 1.0",
            "Generator: awc-devkit-build-backend",
            "Root-Is-Purelib: true",
            "Tag: py3-none-any",
            "",
        ]
    )


def _record_line(path: str, content: bytes) -> tuple[str, str, str]:
    digest = hashlib.sha256(content).digest()
    b64 = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    return path, f"sha256={b64}", str(len(content))


def _build_metadata_dir(metadata_directory: str) -> str:
    metadata_dir = Path(metadata_directory) / DIST_INFO
    metadata_dir.mkdir(parents=True, exist_ok=True)
    (metadata_dir / "METADATA").write_text(_metadata_text(), encoding="utf-8")
    (metadata_dir / "WHEEL").write_text(_wheel_text(), encoding="utf-8")
    (metadata_dir / "top_level.txt").write_text("", encoding="utf-8")
    (metadata_dir / "RECORD").write_text("", encoding="utf-8")
    return DIST_INFO


def prepare_metadata_for_build_wheel(metadata_directory: str, config_settings=None) -> str:
    return _build_metadata_dir(metadata_directory)


def prepare_metadata_for_build_editable(metadata_directory: str, config_settings=None) -> str:
    return _build_metadata_dir(metadata_directory)


def get_requires_for_build_wheel(config_settings=None) -> list[str]:
    return []


def get_requires_for_build_editable(config_settings=None) -> list[str]:
    return []


def _write_wheel(wheel_directory: str) -> str:
    wheel_path = Path(wheel_directory) / WHEEL_NAME
    entries = [
        (f"{DIST_INFO}/METADATA", _metadata_text().encode("utf-8")),
        (f"{DIST_INFO}/WHEEL", _wheel_text().encode("utf-8")),
        (f"{DIST_INFO}/top_level.txt", b""),
    ]

    record_path = f"{DIST_INFO}/RECORD"
    rows = [_record_line(path, content) for path, content in entries]
    rows.append((record_path, "", ""))

    with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path, content in entries:
            zf.writestr(path, content)
        sio = StringIO()
        writer = csv.writer(sio, lineterminator="\n")
        writer.writerows(rows)
        zf.writestr(record_path, sio.getvalue().encode("utf-8"))

    return WHEEL_NAME


def build_wheel(wheel_directory: str, config_settings=None, metadata_directory=None) -> str:
    return _write_wheel(wheel_directory)


def build_editable(wheel_directory: str, config_settings=None, metadata_directory=None) -> str:
    return _write_wheel(wheel_directory)
