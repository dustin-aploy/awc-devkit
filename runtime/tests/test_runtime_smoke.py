import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "awc-devkit" / "runtime" / "src"))
sys.path.insert(0, str(ROOT / "awc-spec" / "src"))

from awc_runtime.runtime import AWCRuntime


class RuntimeSmokeTests(unittest.TestCase):
    def test_runtime_loads_protocol_example_and_evaluates(self):
        audit_file = Path(tempfile.gettempdir()) / "awc-runtime-smoke.jsonl"
        if audit_file.exists():
            audit_file.unlink()
        runtime = AWCRuntime(ROOT / "awc-devkit" / "examples" / "agents" / "sales-agent.yaml", audit_path=audit_file)
        result = runtime.evaluate("Customer asks for a discount", "reply_inbound_dm", 0.65)
        self.assertEqual(result["status"], "escalated")
        self.assertTrue(audit_file.exists())


if __name__ == "__main__":
    unittest.main()
