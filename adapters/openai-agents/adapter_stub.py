from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(slots=True)
class OpenAIAgentAction:
    task: str
    tool_name: str
    confidence: float
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AdapterOutcome:
    status: str
    reasons: list[str] = field(default_factory=list)
    approvals_required: list[str] = field(default_factory=list)


DecisionHook = Callable[[OpenAIAgentAction], AdapterOutcome]
AuditHook = Callable[[dict[str, Any]], None]


class OpenAIAgentsARPAdapter:
    """Minimal structure for policy checks around an OpenAI agent action."""

    def __init__(self, decision_hook: DecisionHook, audit_hook: AuditHook | None = None) -> None:
        self.decision_hook = decision_hook
        self.audit_hook = audit_hook

    def before_action(self, action: OpenAIAgentAction) -> AdapterOutcome:
        outcome = self.decision_hook(action)
        if self.audit_hook:
            self.audit_hook(
                {
                    "framework": "openai-agents",
                    "event": "before-action",
                    "tool_name": action.tool_name,
                    "status": outcome.status,
                    "approvals_required": outcome.approvals_required,
                }
            )
        return outcome

    def requires_human_review(self, outcome: AdapterOutcome) -> bool:
        return outcome.status == "escalated" or bool(outcome.approvals_required)
