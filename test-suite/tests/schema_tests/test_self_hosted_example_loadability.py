import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "awc-devkit" / "test-suite" / "src"))
sys.path.insert(0, str(ROOT / "awc-devkit" / "runtime" / "src"))
sys.path.insert(0, str(ROOT / "awc-spec" / "src"))

from awc_test_suite.self_hosted import load_declaration


def test_self_hosted_example_loads():
    payload = load_declaration(ROOT / "awc-devkit" / "examples" / "agents" / "self-hosted-support-worker.yaml")
    assert payload["identity"]["id"] == "support.self_hosted.tier1"
    assert payload["metadata"]["platform_hints"]["auth_type"] == "bearer"
