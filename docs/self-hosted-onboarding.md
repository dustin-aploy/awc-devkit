# Self-Hosted Onboarding

Use this guide when you want to take a worker from contract definition to a locally validated self-hosted setup.

## Required Artifacts

Prepare these files first:

- an AWC contract aligned with `awc-spec`
- a `metadata.platform_hints` block with invoke and healthcheck details
- a mock invoke request example
- a mock healthcheck request example

## Minimal Flow

1. Start from `examples/agents/self-hosted-support-worker.yaml`.
2. Replace the example identity, mission, permissions, and escalation settings with your own.
3. Add the endpoint hints your runtime needs.
4. Create request examples under `examples/self_hosted/`.
5. Run `scripts/validate_self_hosted_onboarding.py`.
6. Run the runtime and smoke tests before publishing or submitting the worker.

## What The Contract Already Covers

Most of the public worker description can come from the contract itself:

- title from `identity.name`
- summary from `identity.summary` and `scope.mission`
- tags from `identity.tags` and `metadata.labels`
- allowed capabilities from `scope.allowed_tasks` and `authority.allowed_actions`
- restrictions from `scope.prohibited_tasks` and `authority.restricted_actions`
- escalation behavior from `scope.handoffs` and `escalation.triggers`

## Companion Docs

- `docs/run-a-self-hosted-worker.md`
- `docs/validate-a-worker.md`
- `examples/README.md`
