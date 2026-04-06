import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "awc-devkit" / "test-suite" / "src"))
sys.path.insert(0, str(ROOT / "awc-devkit" / "runtime" / "src"))
sys.path.insert(0, str(ROOT / "awc-spec" / "src"))

from awc_test_suite.self_hosted import (
    load_declaration,
    load_json,
    validate_healthcheck_example,
    validate_invoke_example,
)


def test_self_hosted_http_artifacts_match_platform_hints():
    declaration = load_declaration(ROOT / "awc-devkit" / "examples" / "agents" / "self-hosted-support-worker.yaml")
    invoke_payload = load_json(ROOT / "awc-devkit" / "examples" / "self_hosted" / "http_invoke_request.json")
    healthcheck_payload = load_json(ROOT / "awc-devkit" / "examples" / "self_hosted" / "healthcheck_request.json")

    assert not validate_invoke_example(declaration, invoke_payload)
    assert not validate_healthcheck_example(declaration, healthcheck_payload)
