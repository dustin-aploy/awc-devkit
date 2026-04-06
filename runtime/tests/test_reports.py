import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "awc-devkit" / "runtime" / "src"))
sys.path.insert(0, str(ROOT / "awc-spec" / "src"))

from awc_runtime.runtime import AWCRuntime


class ReportTests(unittest.TestCase):
    def test_runtime_builds_protocol_shaped_report(self):
        runtime = AWCRuntime(ROOT / "awc-devkit" / "examples" / "agents" / "content-agent.yaml")
        runtime.evaluate("Draft an email headline", "draft_email", 0.95)
        report = runtime.build_report()
        self.assertEqual(report["kind"], "AWCReport")
        self.assertEqual(report["agent_id"], "marketing.content.drafter")


if __name__ == "__main__":
    unittest.main()
