from __future__ import annotations

from awc_runtime.types import DecisionRecord, DecisionStatus


STATUS_ORDER = {
    DecisionStatus.COMPLETED: 0,
    DecisionStatus.ESCALATED: 1,
    DecisionStatus.BLOCKED: 2,
}


def merge_decisions(*decisions: DecisionRecord) -> DecisionRecord:
    chosen = max(decisions, key=lambda item: STATUS_ORDER[item.status])
    reasons: list[str] = []
    matched: list[str] = []
    approvals: list[str] = []
    warnings: list[str] = []
    for record in decisions:
        reasons.extend(record.reasons)
        matched.extend(record.matched_rules)
        approvals.extend(record.approvals_required)
        warnings.extend(record.budget_warnings)
    return DecisionRecord(
        status=chosen.status,
        reasons=list(dict.fromkeys(reasons)),
        matched_rules=list(dict.fromkeys(matched)),
        approvals_required=list(dict.fromkeys(approvals)),
        budget_warnings=list(dict.fromkeys(warnings)),
    )
