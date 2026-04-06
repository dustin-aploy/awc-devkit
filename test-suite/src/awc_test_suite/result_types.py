from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CheckResult:
    name: str
    category: str
    passed: bool
    details: str
    evidence: list[str] = field(default_factory=list)

    def to_protocol_check(self) -> dict[str, Any]:
        pillar = _pillar_for_check(self.name, self.category)
        payload = {
            "id": self.name,
            "pillar": pillar,
            "description": self.details,
            "status": "pass" if self.passed else "fail",
            "evidence": self.evidence,
        }
        if not self.passed:
            payload["remediation"] = f"Address failing {self.category} check: {self.name}."
        return payload


@dataclass(slots=True)
class ComplianceSummary:
    kind: str
    report_id: str
    generated_at: str
    subject: dict[str, Any]
    protocol_version: str
    profile: dict[str, Any]
    summary: dict[str, Any]
    checks: list[CheckResult]
    attestations: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "report_id": self.report_id,
            "generated_at": self.generated_at,
            "subject": self.subject,
            "protocol_version": self.protocol_version,
            "profile": self.profile,
            "summary": self.summary,
            "checks": [check.to_protocol_check() for check in self.checks],
            "attestations": self.attestations,
        }


def _pillar_for_check(name: str, category: str) -> str:
    if name.startswith("identity"):
        return "identity"
    if name.startswith("scope"):
        return "scope"
    if name.startswith("authority") or "approval" in name:
        return "authority"
    if name.startswith("memory"):
        return "memory"
    if name.startswith("audit"):
        return "audit"
    if name.startswith("budget"):
        return "budget"
    if name.startswith("daily-report") or name.startswith("report-"):
        return "performance"
    return "escalation" if "escalation" in name else "scope"
