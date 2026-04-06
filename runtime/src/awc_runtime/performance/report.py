from __future__ import annotations

from datetime import datetime, timezone

from awc_runtime.loader.schema_loader import load_protocol_version
from awc_runtime.performance.metrics import summarize_decisions


def build_daily_report(agent_config: dict, decisions: list[dict]) -> dict:
    metrics = summarize_decisions(decisions)
    highlights = [
        f"processed {metrics['total_decisions']} decisions",
        f"escalations: {metrics['escalated']}",
    ]
    report = {
        "kind": "AWCReport",
        "report_id": f"daily-{agent_config['identity']['id']}",
        "report_type": "operational",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "agent_id": agent_config["identity"]["id"],
        "protocol_version": load_protocol_version(),
        "period": {
            "start": datetime.now(timezone.utc).isoformat(),
            "end": datetime.now(timezone.utc).isoformat(),
        },
        "summary": {
            "status": "ok" if metrics["blocked"] == 0 else "warning",
            "highlights": highlights,
            "risks": ["blocked decisions present"] if metrics["blocked"] else [],
        },
        "metrics": [
            {"name": key, "value": value, "status": "met" if key != "blocked" or value == 0 else "missed"}
            for key, value in metrics.items()
        ],
        "events": [],
        "recommended_actions": ["review escalation reasons"] if metrics["escalated"] else [],
    }
    return report
