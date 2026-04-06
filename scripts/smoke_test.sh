#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SPEC_DIR="${ROOT_DIR}/../awc-spec"
REGISTRY_DIR="${ROOT_DIR}/../awc-registry"
cd "${ROOT_DIR}"

ARTIFACT_DIR="${ARTIFACT_DIR:-$(mktemp -d "${TMPDIR:-/tmp}/awc-devkit-smoke.XXXXXX")}"
AUDIT_LOG="${ARTIFACT_DIR}/awc-runtime.audit.jsonl"
COMPLIANCE_REPORT="${ARTIFACT_DIR}/compliance-report.json"

clean_stale_editable_metadata() {
  python - <<'PY'
import site
import shutil
from pathlib import Path

patterns = (
    "~rp_protocol-*.dist-info",
    "~rp_devkit-*.dist-info",
    "~rp_runtime-*.dist-info",
    "~rp_test_suite-*.dist-info",
)

for site_dir in [Path(p) for p in site.getsitepackages()] + [Path(site.getusersitepackages())]:
    if not site_dir.exists():
        continue
    for pattern in patterns:
        for path in site_dir.glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"[awc-devkit] removed stale editable metadata: {path}")
PY
}

clean_workspace_caches() {
  python - <<'PY'
import shutil
from pathlib import Path

targets = [Path("../awc-spec"), Path("."), Path("../awc-registry")]
removed = 0
for root in targets:
    if not root.exists():
        continue
    for path in root.rglob("__pycache__"):
        if path.is_dir():
            shutil.rmtree(path)
            removed += 1
    for path in root.rglob(".pytest_cache"):
        if path.is_dir():
            shutil.rmtree(path)
            removed += 1
print(f"[awc-devkit] removed generated cache directories: {removed}")
PY
}

trap clean_workspace_caches EXIT

clean_stale_editable_metadata

echo "[awc-devkit] bootstrapping grouped packages"
./scripts/bootstrap.sh

echo "[awc-devkit] installing editable runtime and test-suite for integration checks"
python -m pip install --no-build-isolation --no-deps -e ./runtime
python -m pip install --no-build-isolation --no-deps -e ./test-suite

echo "[awc-devkit] validating a protocol example from awc-spec"
python - <<'PY'
from pathlib import Path
from awc_runtime.loader.yaml_loader import load_yaml_file
from awc_runtime.validator.validator import ProtocolValidator

path = Path("../awc-spec/examples/sales-agent.yaml")
validator = ProtocolValidator()
result = validator.validate_agent_config(load_yaml_file(path))
if not result.valid:
    raise SystemExit("\n".join(result.errors))
print(f"validated protocol example {path}")
PY

echo "[awc-devkit] validating self-hosted onboarding artifacts"
python ./scripts/validate_self_hosted_onboarding.py \
  --agent ./examples/agents/self-hosted-support-worker.yaml \
  --invoke-example ./examples/self_hosted/http_invoke_request.json \
  --healthcheck-example ./examples/self_hosted/healthcheck_request.json

echo "[awc-devkit] running awc-runtime against a runnable devkit example"
python -m awc_runtime.cli \
  --agent examples/agents/sales-agent.yaml \
  --task "Customer asks for a discount" \
  --action "reply_inbound_dm" \
  --confidence 0.65 \
  --audit-log "${AUDIT_LOG}" \
  --report

test -f "${AUDIT_LOG}"

echo "[awc-devkit] running awc-test-suite"
pytest test-suite/tests

echo "[awc-devkit] generating compliance report"
python -m awc_test_suite.runner \
  --project ./runtime \
  --agent ./examples/agents/sales-agent.yaml \
  --output "${COMPLIANCE_REPORT}"

test -f "${COMPLIANCE_REPORT}"

echo "[awc-devkit] checking registry/report conceptual alignment"
python - <<'PY' "${COMPLIANCE_REPORT}"
import json
import sys
from pathlib import Path

generated_report = json.loads(Path(sys.argv[1]).read_text())
registry_report_example = json.loads(Path("../awc-registry/reports/compliance-report.example.json").read_text())
registry_entry = json.loads(Path("../awc-registry/certified/sample-certified-project.json").read_text())

for report in (generated_report, registry_report_example, registry_entry["evidence"]["compliance_report"]):
    assert report["kind"] == "AWCComplianceReport"
    assert report["protocol_version"]
    assert report["report_id"]
    assert "summary" in report

assert registry_entry["references"]["report_id"] == registry_entry["evidence"]["compliance_report"]["report_id"]
print("registry compliance-report references conceptually match generated compliance reports")
PY

echo "[awc-devkit] validating registry entries against the registry schema"
python - <<'PY'
import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

registry_schema_path = Path("../awc-registry/schemas/registry-entry.schema.json")
compliance_schema_path = Path("../awc-spec/schemas/compliance-report.schema.json")

registry_schema = json.loads(registry_schema_path.read_text())
compliance_schema = json.loads(compliance_schema_path.read_text())
registry_schema_local = copy.deepcopy(registry_schema)
registry_schema_local["properties"]["evidence"]["properties"]["compliance_report"]["$ref"] = compliance_schema["$id"]

registry = Registry().with_resource(registry_schema["$id"], Resource.from_contents(registry_schema_local))
registry = registry.with_resource(compliance_schema["$id"], Resource.from_contents(compliance_schema))
validator = Draft202012Validator(registry_schema_local, registry=registry)

for path in sorted(Path("../awc-registry/certified").glob("*.json")) + sorted(Path("../awc-registry/compatible").glob("*.json")):
    payload = json.loads(path.read_text())
    validator.validate(payload)
    print(f"validated registry entry {path}")
PY

echo "[awc-devkit] smoke test complete"
echo "[awc-devkit] artifacts:"
echo "  audit log: ${AUDIT_LOG}"
echo "  compliance report: ${COMPLIANCE_REPORT}"
