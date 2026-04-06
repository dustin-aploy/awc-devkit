# Claude Skills Adapter Notes

## Conceptual mapping

Claude Skills-style systems center more on bounded task capabilities and invocation patterns than on a monolithic runtime. AWC should therefore wrap skill invocation boundaries and any side-effecting actions a skill may trigger.

## Where pre-action scope/authority checks should happen

Before a skill executes an operation that can mutate state, call tools, or communicate externally.

## Where escalation should happen

When a skill discovers it is outside scope, needs an approval defined by AWC authority rules, or hits a low-confidence/handoff condition.

## Where audit should happen

When a skill invocation starts, when a sensitive step is proposed, and when the skill is blocked or escalated.

## Where budget checks should happen

Before recursive or repeated skill execution, large tool usage bursts, or expensive downstream calls.

## What is intentionally not implemented here

This directory does not implement a Claude runtime, skill installer, hosted sandbox, or tool execution bridge. It only demonstrates where AWC checks could attach.
