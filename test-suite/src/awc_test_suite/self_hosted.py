from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from awc_runtime.loader.yaml_loader import load_yaml_file
from awc_runtime.validator.validator import ProtocolValidator


REQUIRED_PLATFORM_HINT_KEYS = ("invoke_url", "healthcheck_url", "auth_type")


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_declaration(path: str | Path) -> dict[str, Any]:
    return load_yaml_file(path)


def validate_self_hosted_declaration(path: str | Path) -> list[str]:
    validator = ProtocolValidator()
    config = load_declaration(path)
    result = validator.validate_agent_config(config)
    errors = list(result.errors)
    metadata = config.get("metadata", {})
    platform_hints = metadata.get("platform_hints")
    if not isinstance(platform_hints, dict):
        errors.append("$.metadata.platform_hints is required for self-hosted onboarding")
        return errors
    for key in REQUIRED_PLATFORM_HINT_KEYS:
        value = platform_hints.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"$.metadata.platform_hints.{key} must be a non-empty string")
    for key in ("invoke_url", "healthcheck_url"):
        value = platform_hints.get(key, "")
        if isinstance(value, str) and value and not value.startswith(("http://", "https://")):
            errors.append(f"$.metadata.platform_hints.{key} must be an http or https URL")
    return errors


def validate_invoke_example(declaration: dict[str, Any], payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    hints = declaration["metadata"]["platform_hints"]
    if payload.get("method") != "POST":
        errors.append("$.method must equal 'POST'")
    if payload.get("url") != hints["invoke_url"]:
        errors.append("$.url must match metadata.platform_hints.invoke_url")
    headers = payload.get("headers")
    if not isinstance(headers, dict):
        errors.append("$.headers must be an object")
    body = payload.get("body")
    if not isinstance(body, dict):
        errors.append("$.body must be an object")
        return errors
    for key in ("task", "action", "confidence"):
        if key not in body:
            errors.append(f"$.body.{key} is required")
    return errors


def validate_healthcheck_example(declaration: dict[str, Any], payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    hints = declaration["metadata"]["platform_hints"]
    if payload.get("method") != "GET":
        errors.append("$.method must equal 'GET'")
    if payload.get("url") != hints["healthcheck_url"]:
        errors.append("$.url must match metadata.platform_hints.healthcheck_url")
    if payload.get("expected_status") != 200:
        errors.append("$.expected_status must equal 200")
    return errors
