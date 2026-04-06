from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(slots=True)
class CrewTaskContext:
    crew_name: str
    task: str
    action: str
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CrewDecision:
    status: str
    reasons: list[str] = field(default_factory=list)
    approvals_required: list[str] = field(default_factory=list)


DecisionHook = Callable[[CrewTaskContext], CrewDecision]
AuditHook = Callable[[dict[str, Any]], None]


class CrewAIARPAdapter:
    """Minimal adapter shape for ARP checks around crew task dispatch."""

    def __init__(self, decision_hook: DecisionHook, audit_hook: AuditHook | None = None) -> None:
        self.decision_hook = decision_hook
        self.audit_hook = audit_hook

    def before_task_dispatch(self, context: CrewTaskContext) -> CrewDecision:
        decision = self.decision_hook(context)
        if self.audit_hook is not None:
            self.audit_hook(
                {
                    "framework": "crewai",
                    "event": "before-task-dispatch",
                    "crew_name": context.crew_name,
                    "action": context.action,
                    "status": decision.status,
                    "approvals_required": decision.approvals_required,
                }
            )
        return decision

    def may_dispatch(self, decision: CrewDecision) -> bool:
        return decision.status == "completed" and not decision.approvals_required
