from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from awc_runtime.loader.schema_loader import load_schema
from awc_runtime.validator.validator import ProtocolValidator
from awc_test_suite.compatibility import determine_compatibility
from awc_test_suite.result_types import CheckResult, ComplianceSummary


class ReportValidationError(ValueError):
    pass


SUITE_VERSION = (Path(__file__).resolve().parents[2] / "VERSION").read_text(encoding="utf-8").strip()


def build_report(
    *,
    project: str,
    awc_spec_version: str,
    agent_id: str,
    declaration_digest: str,
    artifact_uri: str,
    checks: list[CheckResult],
    timestamp: str | None = None,
) -> ComplianceSummary:
    tests_run = len(checks)
    tests_passed = sum(1 for check in checks if check.passed)
    tests_failed = tests_run - tests_passed
    compatibility_level = determine_compatibility(checks)
    status = _summary_status(compatibility_level, tests_failed)
    timestamp = timestamp or datetime.now(timezone.utc).isoformat()
    report_id = _build_report_id(project, awc_spec_version, checks)
    summary = ComplianceSummary(
        kind="AWCComplianceReport",
        report_id=report_id,
        generated_at=timestamp,
        subject={
            "agent_id": agent_id,
            "declaration_digest": declaration_digest,
            "artifact_uri": artifact_uri,
        },
        protocol_version=awc_spec_version,
        profile={
            "name": project,
            "version": SUITE_VERSION,
            "issuer": "awc-test-suite",
        },
        summary={
            "status": status,
            "passed": tests_passed,
            "failed": tests_failed,
            "warnings": 0,
            "notes": [
                f"project={project}",
                f"compatibility_level={compatibility_level}",
                f"tests_run={tests_run}",
                f"tests_passed={tests_passed}",
                f"tests_failed={tests_failed}",
                f"test_suite_version={SUITE_VERSION}",
            ],
        },
        checks=checks,
        attestations=[
            {
                "name": "awc-test-suite",
                "role": "suite-runner",
                "timestamp": timestamp,
                "statement": f"Generated {compatibility_level} compliance evidence for {project}.",
            }
        ],
    )
    validate_report(summary.to_dict())
    return summary


def write_report(path: str | Path, summary: ComplianceSummary) -> Path:
    path = Path(path)
    path.write_text(json.dumps(summary.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def validate_report(report: dict[str, Any]) -> None:
    schema = load_schema("compliance-report.schema.json")
    validator = ProtocolValidator()
    errors = validator._validate_with_schema(report, schema, "$", schema)  # noqa: SLF001 - reuse protocol-backed validator
    if errors:
        raise ReportValidationError("; ".join(errors))


def _summary_status(compatibility_level: str, tests_failed: int) -> str:
    if tests_failed:
        return "fail"
    if compatibility_level == "certified":
        return "pass"
    return "conditional-pass"


def _build_report_id(project: str, awc_spec_version: str, checks: list[CheckResult]) -> str:
    digest_source = json.dumps(
        {
            "project": project,
            "awc_spec_version": awc_spec_version,
            "checks": [check.to_protocol_check() for check in checks],
            "suite_version": SUITE_VERSION,
        },
        sort_keys=True,
    )
    return hashlib.sha256(digest_source.encode("utf-8")).hexdigest()[:16]
