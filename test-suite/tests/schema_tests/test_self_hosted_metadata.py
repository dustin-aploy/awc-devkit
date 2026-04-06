import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "awc-devkit" / "test-suite" / "src"))
sys.path.insert(0, str(ROOT / "awc-devkit" / "runtime" / "src"))
sys.path.insert(0, str(ROOT / "awc-spec" / "src"))

from awc_test_suite.self_hosted import validate_self_hosted_declaration


def test_self_hosted_metadata_present():
    errors = validate_self_hosted_declaration(ROOT / "awc-devkit" / "examples" / "agents" / "self-hosted-support-worker.yaml")
    assert not errors
