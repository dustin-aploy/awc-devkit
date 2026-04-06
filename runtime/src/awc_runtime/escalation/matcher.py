from __future__ import annotations

from awc_runtime.escalation.patterns import text_matches_rule
from awc_runtime.types import TaskRequest


def match_escalation(agent_config: dict, request: TaskRequest) -> list[str]:
    matches: list[str] = []
    task_text = f"{request.task} {request.action}".strip()
    for trigger in agent_config.get("escalation", {}).get("triggers", []):
        condition = trigger.get("condition", "")
        if condition and text_matches_rule(task_text, condition):
            matches.append(condition)
        if "confidence below" in condition.lower():
            threshold = _extract_threshold(condition)
            if threshold is not None and request.confidence < threshold:
                matches.append(condition)
    for handoff in agent_config.get("scope", {}).get("handoffs", []):
        trigger = handoff.get("trigger", "")
        if trigger and text_matches_rule(task_text, trigger):
            matches.append(trigger)
    return sorted(set(matches))


def _extract_threshold(text: str) -> float | None:
    for chunk in text.replace("=", " ").split():
        try:
            value = float(chunk)
            if 0 <= value <= 1:
                return value
        except ValueError:
            continue
    return None
