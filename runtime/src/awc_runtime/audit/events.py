from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class AuditEvent:
    event_id: str
    event_type: str
    timestamp: str
    agent_id: str
    protocol_version: str
    decision_id: str
    outcome: str
    action: dict[str, Any]
    policy_references: list[str]
    request_id: str | None = None
    escalated_to: str | None = None
    redactions_applied: list[str] | None = None

    @classmethod
    def from_decision(
        cls,
        *,
        event_id: str,
        decision_id: str,
        agent_id: str,
        protocol_version: str,
        outcome: str,
        action_name: str,
        policy_references: list[str],
        escalated_to: str | None,
    ) -> "AuditEvent":
        return cls(
            event_id=event_id,
            event_type="action-proposed",
            timestamp=datetime.now(timezone.utc).isoformat(),
            agent_id=agent_id,
            protocol_version=protocol_version,
            decision_id=decision_id,
            outcome=outcome,
            action={"name": action_name, "approved": outcome == "completed"},
            policy_references=policy_references,
            escalated_to=escalated_to,
            redactions_applied=[],
        )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        return {key: value for key, value in payload.items() if value is not None}
