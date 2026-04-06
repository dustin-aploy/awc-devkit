from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(slots=True)
class GraphTransition:
    from_node: str
    to_node: str
    task: str
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TransitionDecision:
    status: str
    reasons: list[str] = field(default_factory=list)
    escalated_to: str | None = None


DecisionHook = Callable[[GraphTransition], TransitionDecision]
AuditHook = Callable[[dict[str, Any]], None]


class LangGraphARPAdapter:
    """Thin node-transition wrapper for ARP governance checks in graph workflows."""

    def __init__(self, decision_hook: DecisionHook, audit_hook: AuditHook | None = None) -> None:
        self.decision_hook = decision_hook
        self.audit_hook = audit_hook

    def before_transition(self, transition: GraphTransition) -> TransitionDecision:
        decision = self.decision_hook(transition)
        if self.audit_hook:
            self.audit_hook(
                {
                    "framework": "langgraph",
                    "event": "before-transition",
                    "from_node": transition.from_node,
                    "to_node": transition.to_node,
                    "status": decision.status,
                }
            )
        return decision

    def should_route_to_human(self, decision: TransitionDecision) -> bool:
        return decision.status == "escalated"
