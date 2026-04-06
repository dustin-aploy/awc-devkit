# LangGraph Adapter Notes

## Conceptual mapping

LangGraph-style systems expose graph nodes and edges as the main lifecycle shape. AWC should attach to node transitions that produce side effects, tool calls, external communication, or irreversible state changes.

## Where pre-action scope/authority checks should happen

Before entering a node that will call tools, mutate systems, or emit user-facing output.

## Where escalation should happen

When the graph reaches a node or branch representing uncertainty, policy conflict, restricted action, or explicit human review.

## Where audit should happen

At graph transition boundaries: proposed node entry, blocked transition, escalated handoff, and completed side-effecting node execution.

## Where budget checks should happen

Before loops, retries, expensive branches, or fan-out patterns that can materially increase resource usage.

## What is intentionally not implemented here

This directory does not implement a LangGraph runtime binding, graph compiler plugin, or durable execution layer. It only shows the shape of a lightweight AWC-aware wrapper.
