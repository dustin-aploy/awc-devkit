from __future__ import annotations

from awc_runtime.escalation.patterns import text_matches_rule
from awc_runtime.types import DecisionRecord, DecisionStatus, TaskRequest


COMMUNICATION_ACTIONS = {"reply", "send", "email", "publish", "message", "dm", "post"}


def evaluate_authority(agent_config: dict, request: TaskRequest) -> DecisionRecord:
    action_text = request.action
    reasons: list[str] = []
    matched: list[str] = []
    approvals: list[str] = []

    for restricted in agent_config.get("authority", {}).get("restricted_actions", []):
        if text_matches_rule(action_text, restricted) or text_matches_rule(request.task, restricted):
            reasons.append(f"action matches restricted authority: {restricted}")
            matched.append(restricted)
    if reasons:
        return DecisionRecord(status=DecisionStatus.BLOCKED, reasons=reasons, matched_rules=matched)

    for requirement in agent_config.get("authority", {}).get("approval_requirements", []):
        action_name = requirement.get("action", "")
        if action_name and text_matches_rule(action_text, action_name):
            approvals.append(requirement.get("requirement", "approval-required"))
            matched.append(action_name)

    policy = agent_config.get("authority", {}).get("external_communication_policy", "")
    if policy == "draft-only" and any(token in action_text.lower() for token in COMMUNICATION_ACTIONS):
        approvals.append("external communication requires human-controlled draft review")
        matched.append("external_communication_policy")
    if policy == "approved-template-only" and any(token in action_text.lower() for token in COMMUNICATION_ACTIONS):
        approvals.append("external communication requires approved template or human review")
        matched.append("external_communication_policy")

    if approvals:
        return DecisionRecord(
            status=DecisionStatus.ESCALATED,
            reasons=["authority requires approval before action can proceed"],
            matched_rules=matched,
            approvals_required=approvals,
        )
    return DecisionRecord(status=DecisionStatus.COMPLETED, reasons=["action is within declared authority"])
