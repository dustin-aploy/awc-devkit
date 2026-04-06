from __future__ import annotations

import json
from pathlib import Path

from awc_runtime.audit.events import AuditEvent


class AuditLedger:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path else None
        self.events: list[dict] = []

    def append(self, event: AuditEvent) -> dict:
        payload = event.to_dict()
        self.events.append(payload)
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, sort_keys=True) + "\n")
        return payload
