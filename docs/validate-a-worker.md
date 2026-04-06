# Validate A Worker

Validation in `awc-devkit` is incremental. Start with the smallest checks, then move to runtime and test-suite coverage.

## Step 1: Validate Self-Hosted Onboarding Artifacts

Run the onboarding validator against your contract and example request payloads:

```bash
python ./awc-devkit/scripts/validate_self_hosted_onboarding.py \
  --agent ./awc-devkit/examples/agents/self-hosted-support-worker.yaml \
  --invoke-example ./awc-devkit/examples/self_hosted/http_invoke_request.json \
  --healthcheck-example ./awc-devkit/examples/self_hosted/healthcheck_request.json
```

This script checks:

- the contract loads successfully
- the contract satisfies the self-hosted declaration requirements
- the invoke request example matches the contract shape
- the healthcheck request example matches the contract shape

## Step 2: Run The Runtime Smoke Path

Use the runtime to evaluate a contract against a representative task:

```bash
python -m awc_runtime.cli \
  --agent ./awc-devkit/examples/agents/support-agent.yaml \
  --task "Customer asks for a refund after a failed renewal" \
  --action "reply_inbound_dm" \
  --confidence 0.65 \
  --report
```

This is useful for catching policy issues in scope, authority, escalation, budget, or reporting behavior.

## Step 3: Run The Test Suite

Use the repository smoke tests first:

```bash
./awc-devkit/scripts/smoke_test.sh
```

Then run the deeper tests if you are changing runtime or compliance behavior:

```bash
pytest awc-devkit/runtime/tests
python -m pytest awc-devkit/test-suite/tests
```

## Validation Outcome

For a public submission, a worker should have:

- a valid contract
- stable example artifacts
- a clean local validation run
- reproducible compliance evidence when required by the registry
