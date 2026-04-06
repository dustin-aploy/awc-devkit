# Lifecycle Hooks

## Core hook moments

Across most frameworks, AWC logic should be attached at the following moments.

### 1. Before a meaningful action

Before a tool call, outbound message, workflow transition, or external side effect, the adapter should run scope, authority, and budget checks.

### 2. When the framework detects uncertainty or blocked execution

When confidence falls, policy conflicts appear, or an action needs approval, the adapter should trigger an AWC escalation path rather than silently continuing.

### 3. When the framework emits an event worth reconstructing later

Audit hooks should capture action proposals, blocked actions, escalations, approvals, and relevant policy references.

### 4. After the framework finishes a decision cycle

A post-decision hook can emit summary metadata for reporting, counters, or downstream compliance evidence.

## Mapping to the reference runtime

`../runtime` demonstrates this lifecycle shape already:

- `HookRegistry.run_before()` is the pre-action insertion point.
- `evaluate_scope()`, `evaluate_authority()`, and `check_budget()` are pre-execution guard examples.
- `match_escalation()` is the escalation decision point.
- `AuditLedger.append()` is the audit persistence point.
- `HookRegistry.run_after()` is the post-decision/reporting insertion point.

Framework adapters in this directory should mirror those stages conceptually, even if the host framework uses different callback names.
