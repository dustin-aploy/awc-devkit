import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "awc-devkit" / "test-suite" / "src"))
sys.path.insert(0, str(ROOT / "awc-devkit" / "runtime" / "src"))
sys.path.insert(0, str(ROOT / "awc-spec" / "src"))

from awc_test_suite.loader import load_fixture
from awc_test_suite.runner import ComplianceRunner


def test_report_required_fields(tmp_path):
    runner = ComplianceRunner()
    result = runner.check_report_required_fields(load_fixture("valid_agent.yaml"))
    assert result.passed
    report = runner.run(
        agent_path=ROOT / "awc-devkit" / "test-suite" / "fixtures" / "valid_agent.yaml",
        project="example-project",
        output_path=tmp_path / "compliance-report.json",
    )
    assert report["kind"] == "AWCComplianceReport"
    assert report["summary"]["status"] in {"pass", "conditional-pass", "fail"}
    assert any(note.startswith("compatibility_level=") for note in report["summary"]["notes"])
