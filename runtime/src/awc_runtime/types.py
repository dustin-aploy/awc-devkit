from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DecisionStatus(str, Enum):
    COMPLETED = "completed"
    BLOCKED = "blocked"
    ESCALATED = "escalated"


@dataclass(slots=True)
class TaskRequest:
    task: str
    action: str
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class DecisionRecord:
    status: DecisionStatus
    reasons: list[str]
    matched_rules: list[str] = field(default_factory=list)
    approvals_required: list[str] = field(default_factory=list)
    budget_warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "reasons": self.reasons,
            "matched_rules": self.matched_rules,
            "approvals_required": self.approvals_required,
            "budget_warnings": self.budget_warnings,
        }


@dataclass(slots=True)
class ValidationResult:
    valid: bool
    errors: list[str]


@dataclass(slots=True)
class BudgetResult:
    exhausted: bool
    warnings: list[str] = field(default_factory=list)
    consumed: dict[str, float] = field(default_factory=dict)
