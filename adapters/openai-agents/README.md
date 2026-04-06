# OpenAI Agents Adapter Notes

## Conceptual mapping

For OpenAI agent-style orchestration, AWC should sit around tool invocation, handoff, and outbound action boundaries. AWC is not meant to replace the framework planner; it is meant to govern what planned actions are allowed to proceed.

## Where pre-action scope/authority checks should happen

Right before tool execution, external API mutation, or user-visible outbound communication.

## Where escalation should happen

At the point where the agent decides it needs human review, encounters restricted actions, or crosses a confidence/risk threshold.

## Where audit should happen

When the framework proposes a tool/action, when AWC blocks it, and when AWC escalates it. That keeps the governance trail attached to the agent lifecycle.

## Where budget checks should happen

Before costly model/tool loops or before side-effecting actions that should respect request, cost, or throughput limits.

## What is intentionally not implemented here

This is not a full OpenAI Agents SDK integration, session manager, tracing backend, or hosted service binding. It is only a thin adapter sketch.
