from __future__ import annotations

from collections import Counter


def summarize_decisions(decisions: list[dict]) -> dict:
    counts = Counter(item.get("status", "unknown") for item in decisions)
    total = sum(counts.values())
    return {
        "total_decisions": total,
        "completed": counts.get("completed", 0),
        "blocked": counts.get("blocked", 0),
        "escalated": counts.get("escalated", 0),
        "escalation_rate": (counts.get("escalated", 0) / total) if total else 0.0,
    }
