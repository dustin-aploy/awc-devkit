import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "awc-devkit" / "runtime" / "src"))
sys.path.insert(0, str(ROOT / "awc-spec" / "src"))

from awc_runtime.escalation.matcher import match_escalation
from awc_runtime.loader.yaml_loader import load_yaml_file
from awc_runtime.types import TaskRequest


class EscalationTests(unittest.TestCase):
    def test_discount_request_matches_sales_escalation(self):
        config = load_yaml_file(ROOT / "awc-spec" / "examples" / "sales-agent.yaml")
        matches = match_escalation(config, TaskRequest(task="Customer asks for a discount", action="reply_inbound_dm", confidence=0.65))
        self.assertTrue(matches)


if __name__ == "__main__":
    unittest.main()
