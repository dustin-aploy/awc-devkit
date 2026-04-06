from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from awc_runtime.runtime import AWCRuntime
from awc_runtime.validator.validator import SchemaValidationError

DEFAULT_AUDIT_LOG = "awc-runtime.audit.jsonl"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="awc-runtime", description="AI Work Contract (AWC) reference runtime CLI")
    parser.add_argument("--agent", required=True, help="Path to an AWC-compatible YAML declaration")
    parser.add_argument("--task", required=True, help="Task description to evaluate")
    parser.add_argument("--action", required=True, help="Action name to evaluate")
    parser.add_argument("--confidence", required=True, type=float, help="Model confidence in the proposed action")
    parser.add_argument("--audit-log", default=DEFAULT_AUDIT_LOG, help="JSONL audit log path (defaults to ./awc-runtime.audit.jsonl)")
    parser.add_argument("--report", action="store_true", help="Print a report after evaluation")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        runtime = AWCRuntime(args.agent, audit_path=args.audit_log)
        decision = runtime.evaluate(task=args.task, action=args.action, confidence=args.confidence)
        decision["audit_log"] = str(Path(args.audit_log).resolve())
        print(json.dumps(decision, indent=2, sort_keys=True))
        if args.report:
            print(json.dumps(runtime.build_report(), indent=2, sort_keys=True))
        return 0
    except SchemaValidationError as exc:
        parser.error(str(exc))
    except Exception as exc:  # pragma: no cover - CLI safety
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
