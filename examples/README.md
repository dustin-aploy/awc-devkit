# AWC Runnable Examples

`awc-devkit/examples` contains working examples for local development and validation.

Use `awc-spec/examples` if you want protocol reference contracts. Use this directory if you want runnable inputs, local tasks, and sample outputs.

## Directory Layout

- `agents/` example worker contracts for runtime and validation flows
- `demo_tasks/` representative task prompts for local runs
- `demo_outputs/` sample audit and reporting artifacts
- `self_hosted/` mock request payloads for self-hosted onboarding

## Recommended Starting Points

- `agents/self-hosted-support-worker.yaml` for self-hosted onboarding
- `agents/support-agent.yaml` for a support workflow example
- `agents/sales-agent.yaml` for a sales workflow example

## Typical Validation Flow

```bash
pip install -e ../../awc-spec
pip install -e ../runtime
python -m awc_runtime.cli \
  --agent agents/sales-agent.yaml \
  --task "Customer asks for a discount" \
  --action "reply_inbound_dm" \
  --confidence 0.65 \
  --report
python ../scripts/validate_self_hosted_onboarding.py \
  --agent ./agents/self-hosted-support-worker.yaml \
  --invoke-example ./self_hosted/http_invoke_request.json \
  --healthcheck-example ./self_hosted/healthcheck_request.json
```
