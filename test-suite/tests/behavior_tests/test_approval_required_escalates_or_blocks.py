import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "awc-devkit" / "test-suite" / "src"))
sys.path.insert(0, str(ROOT / "awc-devkit" / "runtime" / "src"))
sys.path.insert(0, str(ROOT / "awc-spec" / "src"))

from awc_test_suite.loader import load_fixture
from awc_test_suite.runner import ComplianceRunner


def test_approval_required_escalates_or_blocks():
    result = ComplianceRunner().check_approval_required_escalates_or_blocks(load_fixture("valid_agent.yaml"))
    assert result.passed
