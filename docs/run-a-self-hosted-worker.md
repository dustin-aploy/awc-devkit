# Run A Self-Hosted Worker

This guide covers the smallest local setup for running a self-hosted AWC worker with the reference tooling in `awc-devkit`.

## Prerequisites

- Python environment ready for editable installs
- local checkout of `awc-spec`
- local checkout of `awc-devkit`

## Install The Local Packages

From the workspace root:

```bash
./awc-devkit/scripts/bootstrap.sh
```

If you want to install manually:

```bash
pip install -e ./awc-spec
pip install -e ./awc-devkit/runtime
pip install -e ./awc-devkit/test-suite
```

## Start From The Self-Hosted Example

Use these files as your template:

- `examples/agents/self-hosted-support-worker.yaml`
- `examples/self_hosted/http_invoke_request.json`
- `examples/self_hosted/healthcheck_request.json`

Update the contract with your worker identity, scope, authority, and endpoint hints.

## Run The Runtime Locally

The reference runtime can evaluate a worker contract against a sample task:

```bash
python -m awc_runtime.cli \
  --agent ./awc-devkit/examples/agents/self-hosted-support-worker.yaml \
  --task "Customer cannot access an account after password reset" \
  --action "prepare_escalation_summary" \
  --confidence 0.82 \
  --report
```

This does not call your live endpoint. It validates the contract and applies the runtime checks locally.

## What To Provide For A Self-Hosted Worker

At minimum:

- an AWC contract that validates
- `metadata.platform_hints` with invoke and healthcheck details
- a mock invoke request example
- a mock healthcheck request example

## Next Step

After the runtime works locally, run the checks in `docs/validate-a-worker.md`.
