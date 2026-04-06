from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile
from typing import Callable

from awc_runtime.runtime import AWCRuntime
from awc_runtime.validator.validator import ProtocolValidator

from awc_test_suite.loader import declaration_digest, load_agent, load_json_fixture, load_protocol_version
from awc_test_suite.report import build_report, write_report
from awc_test_suite.result_types import CheckResult


CheckFunc = Callable[[dict], CheckResult]


class ComplianceRunner:
    def __init__(self) -> None:
        self.validator = ProtocolValidator()
        self.catalog: list[CheckFunc] = [
            self.check_identity_required,
            self.check_scope_required,
            self.check_authority_required,
            self.check_memory_required,
            self.check_forbidden_action_block,
            self.check_approval_required_escalates_or_blocks,
            self.check_escalation_trigger,
            self.check_budget_exceeded,
            self.check_audit_fields,
            self.check_audit_event_types,
            self.check_audit_on_block,
            self.check_audit_on_escalation,
            self.check_daily_report_format,
            self.check_report_required_fields,
        ]

    def run(self, *, agent_path: str | Path, project: str, output_path: str | Path = "compliance-report.json") -> dict:
        agent_path = Path(agent_path)
        config = load_agent(agent_path)
        checks = [check(config) for check in self.catalog]
        summary = build_report(
            project=project,
            awc_spec_version=load_protocol_version(),
            agent_id=config["identity"]["id"],
            declaration_digest=declaration_digest(agent_path),
            artifact_uri=agent_path.resolve().as_uri(),
            checks=checks,
        )
        write_report(output_path, summary)
        return summary.to_dict()

    def check_identity_required(self, config: dict) -> CheckResult:
        candidate = dict(config)
        candidate.pop("identity", None)
        result = self.validator.validate_agent_config(candidate)
        return CheckResult("identity-required", "schema", not result.valid, "identity must be required", result.errors)

    def check_scope_required(self, config: dict) -> CheckResult:
        candidate = dict(config)
        candidate.pop("scope", None)
        result = self.validator.validate_agent_config(candidate)
        return CheckResult("scope-required", "schema", not result.valid, "scope must be required", result.errors)

    def check_authority_required(self, config: dict) -> CheckResult:
        candidate = dict(config)
        candidate.pop("authority", None)
        result = self.validator.validate_agent_config(candidate)
        return CheckResult("authority-required", "schema", not result.valid, "authority must be required", result.errors)

    def check_memory_required(self, config: dict) -> CheckResult:
        candidate = dict(config)
        candidate.pop("memory", None)
        result = self.validator.validate_agent_config(candidate)
        return CheckResult("memory-required", "schema", not result.valid, "memory must be required", result.errors)

    def check_forbidden_action_block(self, config: dict) -> CheckResult:
        runtime = self._runtime_with_config(config)
        result = runtime.evaluate("Please negotiate pricing", "reply_inbound_dm", 0.95)
        return CheckResult("forbidden-action-block", "behavior", result["status"] == "blocked", "forbidden actions should block", result["reasons"])

    def check_approval_required_escalates_or_blocks(self, config: dict) -> CheckResult:
        runtime = self._runtime_with_config(config)
        result = runtime.evaluate("Reply to a lead", "reply_inbound_dm", 0.90)
        passed = result["status"] in {"escalated", "blocked"}
        return CheckResult("approval-required", "behavior", passed, "approval-required actions should escalate or block", result["reasons"])

    def check_escalation_trigger(self, config: dict) -> CheckResult:
        runtime = self._runtime_with_config(config)
        result = runtime.evaluate("Customer asks for a discount", "reply_inbound_dm", 0.65)
        return CheckResult("escalation-trigger", "behavior", result["status"] == "escalated", "escalation triggers should escalate", result["matched_rules"])

    def check_budget_exceeded(self, config: dict) -> CheckResult:
        candidate = json.loads(json.dumps(config))
        candidate["budget"]["limits"] = [{"name": "request-count", "amount": 1, "unit": "count", "period": "P1D", "enforcement": "hard"}]
        runtime = self._runtime_with_config(candidate)
        result = runtime.evaluate("Draft a response", "draft_response", 0.95, metadata={"request-count": 1})
        return CheckResult("budget-exceeded", "behavior", result["status"] == "blocked", "hard budget exhaustion should block", result["reasons"])

    def check_audit_fields(self, config: dict) -> CheckResult:
        audit_path = Path(tempfile.gettempdir()) / "awc-test-suite-audit-fields.jsonl"
        runtime = self._runtime_with_config(config, audit_path=audit_path)
        runtime.evaluate("Draft a response", "draft_response", 0.95)
        payload = json.loads(audit_path.read_text(encoding="utf-8").splitlines()[-1])
        expected = load_json_fixture("expected_audit.json")
        missing = [key for key in expected["required_fields"] if key not in payload]
        return CheckResult("audit-fields", "audit", not missing, "audit events must contain required fields", missing or list(payload.keys()))

    def check_audit_event_types(self, config: dict) -> CheckResult:
        audit_path = Path(tempfile.gettempdir()) / "awc-test-suite-audit-types.jsonl"
        runtime = self._runtime_with_config(config, audit_path=audit_path)
        runtime.evaluate("Draft a response", "draft_response", 0.95)
        payload = json.loads(audit_path.read_text(encoding="utf-8").splitlines()[-1])
        return CheckResult("audit-event-type", "audit", payload.get("event_type") == "action-proposed", "audit events should use action-proposed", [payload.get("event_type", "missing")])

    def check_audit_on_block(self, config: dict) -> CheckResult:
        audit_path = Path(tempfile.gettempdir()) / "awc-test-suite-audit-block.jsonl"
        runtime = self._runtime_with_config(config, audit_path=audit_path)
        runtime.evaluate("Please negotiate pricing", "reply_inbound_dm", 0.95)
        payload = json.loads(audit_path.read_text(encoding="utf-8").splitlines()[-1])
        return CheckResult("audit-on-block", "audit", payload.get("outcome") == "blocked", "blocked decisions must be audited", [payload.get("outcome", "missing")])

    def check_audit_on_escalation(self, config: dict) -> CheckResult:
        audit_path = Path(tempfile.gettempdir()) / "awc-test-suite-audit-escalation.jsonl"
        runtime = self._runtime_with_config(config, audit_path=audit_path)
        runtime.evaluate("Customer asks for a discount", "reply_inbound_dm", 0.65)
        payload = json.loads(audit_path.read_text(encoding="utf-8").splitlines()[-1])
        return CheckResult("audit-on-escalation", "audit", payload.get("outcome") == "escalated", "escalated decisions must be audited", [payload.get("outcome", "missing")])

    def check_daily_report_format(self, config: dict) -> CheckResult:
        runtime = self._runtime_with_config(config)
        runtime.evaluate("Draft a response", "draft_response", 0.95)
        report = runtime.build_report()
        passed = report.get("kind") == "AWCReport" and report.get("report_type") == "operational"
        return CheckResult("daily-report-format", "reporting", passed, "runtime daily reports should match protocol report shape", [report.get("kind", "missing")])

    def check_report_required_fields(self, config: dict) -> CheckResult:
        runtime = self._runtime_with_config(config)
        runtime.evaluate("Draft a response", "draft_response", 0.95)
        report = runtime.build_report()
        required = load_json_fixture("sample_daily_report.json")["required_fields"]
        missing = [key for key in required if key not in report]
        return CheckResult("report-required-fields", "reporting", not missing, "daily report should include required fields", missing or required)

    def _runtime_with_config(self, config: dict, audit_path: str | Path | None = None) -> AWCRuntime:
        temp_path = Path(tempfile.gettempdir()) / f"awc-test-suite-{config['identity']['id'].replace('.', '-')}.yaml"
        temp_path.write_text(_dump_yaml(config), encoding="utf-8")
        return AWCRuntime(temp_path, audit_path=audit_path)


def _dump_yaml(value, indent: int = 0) -> str:
    pad = " " * indent
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.append(_dump_yaml(item, indent + 2))
            else:
                lines.append(f"{pad}{key}: {_scalar(item)}")
        return "\n".join(lines)
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                if isinstance(item, dict) and item:
                    first_key = next(iter(item))
                    first_value = item[first_key]
                    rest = dict(item)
                    rest.pop(first_key)
                    if isinstance(first_value, (dict, list)):
                        lines.append(f"{pad}- {first_key}:")
                        lines.append(_dump_yaml(first_value, indent + 4))
                    else:
                        lines.append(f"{pad}- {first_key}: {_scalar(first_value)}")
                    if rest:
                        lines.append(_dump_yaml(rest, indent + 2))
                else:
                    lines.append(f"{pad}-")
                    lines.append(_dump_yaml(item, indent + 2))
            else:
                lines.append(f"{pad}- {_scalar(item)}")
        return "\n".join(lines)
    return f"{pad}{_scalar(value)}"


def _scalar(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str) and any(char in value for char in [":", "#", "[", "]"]):
        return json.dumps(value)
    return str(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="awc-test-suite", description="AI Work Contract (AWC) compliance runner")
    parser.add_argument("--agent", required=True, help="Path to the agent YAML declaration to test")
    parser.add_argument("--project", required=True, help="Project name for the compliance report")
    parser.add_argument("--output", default="compliance-report.json", help="Path to write the compliance report JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    report = ComplianceRunner().run(agent_path=args.agent, project=args.project, output_path=args.output)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
