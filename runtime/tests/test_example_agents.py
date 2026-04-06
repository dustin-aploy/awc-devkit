import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "awc-devkit" / "runtime" / "src"))
sys.path.insert(0, str(ROOT / "awc-spec" / "src"))

from awc_runtime.runtime import AWCRuntime
from awc_runtime.validator.validator import ProtocolValidator
from awc_runtime.loader.yaml_loader import load_yaml_file


class ExampleAgentRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = ProtocolValidator()

    def _audit_path(self, name: str) -> Path:
        return Path(tempfile.gettempdir()) / f"{name}.jsonl"

    def test_workspace_examples_validate_and_complete_low_risk_tasks(self):
        scenarios = [
            (
                "content-agent.yaml",
                "Assemble launch email, landing page bullets, and CTA variants from the approved messaging kit",
                "prepare-editorial-bundle",
                0.94,
                "completed",
            ),
            (
                "operations-agent.yaml",
                "Execute approved staging environment cleanup checklist and attach completion evidence",
                "run-approved-checklist",
                0.91,
                "completed",
            ),
            (
                "recruiting-agent.yaml",
                "Coordinate final round interviews and reserve an approved interviewer panel for next week",
                "reserve-panel-slot",
                0.92,
                "completed",
            ),
            (
                "sales-agent.yaml",
                "Qualify inbound SaaS lead, enrich territory data, and route to enterprise SDR queue",
                "assign-qualified-account",
                0.93,
                "completed",
            ),
            (
                "self-hosted-support-worker.yaml",
                "Classify a password reset request and route the case to the access-support queue",
                "route-ticket",
                0.93,
                "completed",
            ),
            (
                "support-agent.yaml",
                "Classify a login request, attach the approved password reset article, and place the ticket in the correct queue",
                "queue-ticket-for-resolution",
                0.90,
                "completed",
            ),
        ]

        for agent_name, task, action, confidence, expected_status in scenarios:
            with self.subTest(agent=agent_name):
                agent_path = ROOT / "awc-devkit" / "examples" / "agents" / agent_name
                validation = self.validator.validate_agent_config(load_yaml_file(agent_path))
                self.assertTrue(validation.valid, validation.errors)

                audit_path = self._audit_path(agent_name.replace('.yaml', '-complete'))
                if audit_path.exists():
                    audit_path.unlink()
                runtime = AWCRuntime(agent_path, audit_path=audit_path)
                result = runtime.evaluate(task, action, confidence)

                self.assertEqual(result["status"], expected_status)
                self.assertTrue(audit_path.exists())

    def test_workspace_examples_escalate_on_risky_or_low_confidence_inputs(self):
        scenarios = [
            (
                "content-agent.yaml",
                "Prepare a launch editorial bundle from limited approved messaging",
                "prepare-editorial-bundle",
                0.60,
            ),
            (
                "operations-agent.yaml",
                "Route a repetitive internal operations request that has unclear runbook mapping",
                "run-approved-checklist",
                0.60,
            ),
            (
                "recruiting-agent.yaml",
                "Candidate requests accommodation details before the onsite interview",
                "reserve-panel-slot",
                0.90,
            ),
            (
                "sales-agent.yaml",
                "Qualify a lead with incomplete firmographic data and ambiguous intent",
                "assign-qualified-account",
                0.60,
            ),
            (
                "self-hosted-support-worker.yaml",
                "Classify a sparse support ticket with conflicting troubleshooting signals",
                "route-ticket",
                0.60,
            ),
            (
                "support-agent.yaml",
                "Classify a sparse support ticket with conflicting troubleshooting signals",
                "queue-ticket-for-resolution",
                0.60,
            ),
        ]

        for agent_name, task, action, confidence in scenarios:
            with self.subTest(agent=agent_name):
                agent_path = ROOT / "awc-devkit" / "examples" / "agents" / agent_name
                audit_path = self._audit_path(agent_name.replace('.yaml', '-escalate'))
                if audit_path.exists():
                    audit_path.unlink()
                runtime = AWCRuntime(agent_path, audit_path=audit_path)
                result = runtime.evaluate(task, action, confidence)

                self.assertEqual(result["status"], "escalated")
                self.assertTrue(result["matched_rules"])
                self.assertTrue(audit_path.exists())


if __name__ == "__main__":
    unittest.main()
