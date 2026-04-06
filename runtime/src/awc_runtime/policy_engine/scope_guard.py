from __future__ import annotations

import re

from awc_runtime.types import DecisionRecord, DecisionStatus, TaskRequest


def evaluate_scope(agent_config: dict, request: TaskRequest) -> DecisionRecord:
    text = f"{request.task} {request.action}".strip()
    reasons: list[str] = []
    matched: list[str] = []
    for prohibited in agent_config.get("scope", {}).get("prohibited_tasks", []):
        if _matches_prohibited_scope(text, prohibited):
            reasons.append(f"task matches prohibited scope: {prohibited}")
            matched.append(prohibited)
    if reasons:
        return DecisionRecord(status=DecisionStatus.BLOCKED, reasons=reasons, matched_rules=matched)

    confidence_thresholds = agent_config.get("scope", {}).get("confidence_thresholds", [])
    for threshold in confidence_thresholds:
        minimum = threshold.get("minimum")
        if minimum is not None and request.confidence < float(minimum):
            reasons.append(
                f"confidence {request.confidence:.2f} below scope threshold {minimum} for {threshold.get('name', 'unnamed-threshold')}"
            )
            matched.append(threshold.get("name", "confidence-threshold"))
    if reasons:
        return DecisionRecord(status=DecisionStatus.ESCALATED, reasons=reasons, matched_rules=matched)

    return DecisionRecord(status=DecisionStatus.COMPLETED, reasons=["task is within declared scope"])


def _matches_prohibited_scope(text: str, prohibited: str) -> bool:
    if prohibited.lower() in text.lower():
        return True
    text_tokens = set(re.findall(r"[a-z0-9]+", text.lower()))
    prohibited_tokens = set(re.findall(r"[a-z0-9]+", prohibited.lower()))
    return len(text_tokens & prohibited_tokens) >= max(2, len(prohibited_tokens))
