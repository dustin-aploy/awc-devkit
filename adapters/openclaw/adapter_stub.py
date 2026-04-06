from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(slots=True)
class OpenClawActionContext:
    task: str
    action: str
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ARPDecision:
    allowed: bool
    status: str
    reasons: list[str] = field(default_factory=list)
    escalated_to: str | None = None


PolicyHook = Callable[[OpenClawActionContext], ARPDecision]
AuditHook = Callable[[dict[str, Any]], None]


class OpenClawARPAdapter:
    """Thin wrapper for invoking ARP checks around an OpenClaw-style action."""

    def __init__(self, pre_action: PolicyHook, audit_hook: AuditHook | None = None) -> None:
        self.pre_action = pre_action
        self.audit_hook = audit_hook

    def before_tool_execution(self, context: OpenClawActionContext) -> ARPDecision:
        decision = self.pre_action(context)
        if self.audit_hook is not None:
            self.audit_hook(
                {
                    "framework": "openclaw",
                    "event": "pre-tool-execution",
                    "task": context.task,
                    "action": context.action,
                    "decision": decision.status,
                    "reasons": decision.reasons,
                }
            )
        return decision

    def should_continue(self, decision: ARPDecision) -> bool:
        return decision.allowed and decision.status == "completed"
