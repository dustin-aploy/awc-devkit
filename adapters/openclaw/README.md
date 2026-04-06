# OpenClaw Adapter Notes

## Conceptual mapping

OpenClaw-style agent loops usually expose a central decision/tool-execution path. AWC should wrap that path as a governance layer: translate the candidate tool call or action into an AWC action context, ask AWC for a pre-action decision, and only then let the framework continue.

## Where pre-action scope/authority checks should happen

Immediately before the framework executes a tool call, side effect, or user-visible outbound action.

## Where escalation should happen

When the framework detects low confidence, restricted action classes, or a pending approval requirement. The adapter should convert that into an AWC escalation route rather than encode OpenClaw-specific escalation semantics as the source of truth.

## Where audit should happen

At action proposal time and again on blocked/escalated outcomes so the framework’s decisions remain reconstructable later.

## Where budget checks should happen

Before expensive tool chains, repeated retries, or outward side effects. Budget checks should be advisory or blocking depending on the AWC declaration, not on ad hoc framework defaults.

## What is intentionally not implemented here

This directory does not implement a real OpenClaw connector, tool transport, hosted runtime integration, or policy storage backend. It only shows the minimal structural shape of an AWC hook.
