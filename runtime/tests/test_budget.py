import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "awc-devkit" / "runtime" / "src"))
sys.path.insert(0, str(ROOT / "awc-spec" / "src"))

from awc_runtime.budget.checker import check_budget
from awc_runtime.budget.state import BudgetState
from awc_runtime.loader.yaml_loader import load_yaml_file
from awc_runtime.types import TaskRequest


class BudgetTests(unittest.TestCase):
    def test_budget_warning_is_emitted(self):
        config = load_yaml_file(ROOT / "awc-spec" / "examples" / "sales-agent.yaml")
        config["budget"]["limits"] = [{"name": "monthly-usd", "amount": 2, "unit": "count", "period": "P1M", "enforcement": "soft"}]
        config["budget"]["warning_thresholds"] = [{"limit": "monthly-usd", "percent": 50}]
        state = BudgetState()
        result = check_budget(config, state, TaskRequest(task="Draft note", action="draft", confidence=0.9))
        self.assertTrue(result.warnings)


if __name__ == "__main__":
    unittest.main()
