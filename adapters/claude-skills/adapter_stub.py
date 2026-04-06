from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(slots=True)
class SkillInvocation:
    skill_name: str
    task: str
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class InvocationDecision:
    status: str
    reasons: list[str] = field(default_factory=list)
    matched_rules: list[str] = field(default_factory=list)


DecisionHook = Callable[[SkillInvocation], InvocationDecision]
AuditHook = Callable[[dict[str, Any]], None]


class ClaudeSkillsARPAdapter:
    """Small structural stub for wrapping skill invocations with ARP policy checks."""

    def __init__(self, decision_hook: DecisionHook, audit_hook: AuditHook | None = None) -> None:
        self.decision_hook = decision_hook
        self.audit_hook = audit_hook

    def before_skill_run(self, invocation: SkillInvocation) -> InvocationDecision:
        decision = self.decision_hook(invocation)
        if self.audit_hook is not None:
            self.audit_hook(
                {
                    "framework": "claude-skills",
                    "event": "before-skill-run",
                    "skill_name": invocation.skill_name,
                    "status": decision.status,
                    "matched_rules": decision.matched_rules,
                }
            )
        return decision

    def blocked(self, decision: InvocationDecision) -> bool:
        return decision.status == "blocked"
