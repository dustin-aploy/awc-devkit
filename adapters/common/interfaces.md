# Thin Adapter Interfaces

## Principle

A thin AWC adapter should expose only the minimum structure needed to:

- describe an action about to happen;
- request a scope/authority/budget decision;
- surface escalation requirements;
- emit audit-friendly events; and
- pass control back to the host framework.

## Suggested conceptual interface

A framework adapter usually needs three kinds of objects:

1. **Action context** — a small record describing the current task, action name, confidence, metadata, and optional framework-native payload.
2. **Policy gateway** — a callable surface that asks the AWC layer for pre-action checks, escalation routing, audit logging, and budget enforcement.
3. **Framework callback wrapper** — a tiny shim that translates framework lifecycle events into AWC-shaped calls.

## What adapters should not own

Adapters should not become the place where:

- AWC schemas are redefined;
- full approval workflows are implemented;
- audit persistence is re-architected;
- budget ledgers are centralized; or
- framework internals are abstracted into a fake universal SDK.

Those concerns belong either to the protocol, a runtime, or a dedicated integration repository.
