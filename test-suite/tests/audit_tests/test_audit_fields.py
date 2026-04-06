import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "awc-devkit" / "test-suite" / "src"))
sys.path.insert(0, str(ROOT / "awc-devkit" / "runtime" / "src"))
sys.path.insert(0, str(ROOT / "awc-spec" / "src"))

from awc_test_suite.loader import load_fixture
from awc_test_suite.runner import ComplianceRunner


def test_audit_fields():
    result = ComplianceRunner().check_audit_fields(load_fixture("valid_agent.yaml"))
    assert result.passed
