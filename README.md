# AWC Devkit

`awc-devkit` is the implementation and validation toolkit for working with AI Work Contract (AWC) workers.

Use this repository to:

- run a contract through the reference runtime
- validate a self-hosted worker setup
- generate or inspect compliance evidence
- start from working examples instead of building from scratch

`awc-devkit` depends on `awc-spec` for the contract format. It does not redefine the protocol.

## Repository Layout

```text
awc-devkit/
  runtime/     reference runtime and CLI
  test-suite/  conformance and compliance-report tooling
  examples/    runnable contracts, sample tasks, and sample outputs
  adapters/    integration notes for specific frameworks
  docs/        onboarding and workflow guides
  scripts/     bootstrap, smoke-test, and validation helpers
```

## Minimal Self-Hosted Onboarding

1. Install the workspace dependencies.
2. Start from `examples/agents/self-hosted-support-worker.yaml`.
3. Add your invoke and healthcheck request examples under `examples/self_hosted/`.
4. Run the onboarding validator.
5. Run the runtime and test suite for deeper checks.

```bash
./scripts/bootstrap.sh
python ./scripts/validate_self_hosted_onboarding.py \
  --agent ./examples/agents/self-hosted-support-worker.yaml \
  --invoke-example ./examples/self_hosted/http_invoke_request.json \
  --healthcheck-example ./examples/self_hosted/healthcheck_request.json
./scripts/smoke_test.sh
```

## Examples

- agent contracts: `examples/agents/`
- task inputs: `examples/demo_tasks/`
- sample outputs: `examples/demo_outputs/`
- self-hosted request shapes: `examples/self_hosted/`

## Validation Flow

Use the tools in this order:

1. schema and self-hosted shape checks with `scripts/validate_self_hosted_onboarding.py`
2. policy evaluation with `runtime/`
3. broader compatibility checks with `test-suite/`

## Developer Docs

- `docs/self-hosted-onboarding.md`
- `docs/run-a-self-hosted-worker.md`
- `docs/validate-a-worker.md`
- `examples/README.md`
