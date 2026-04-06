# AWC Runtime

`awc-runtime` is the reference runtime in `awc-devkit`.

It demonstrates how to:
- load AWC declarations
- validate them against protocol-owned schemas from `../../awc-spec`
- evaluate scope, authority, escalation, budget, and memory rules
- emit audit events
- build simple operational reports

`awc-runtime` is **not** the protocol itself. AWC protocol truth remains in `../../awc-spec`.

For V1, the runtime is primarily a local validation and policy-evaluation tool for self-hosted worker onboarding. It does not introduce a hosted execution mode.

## Install locally

```bash
pip install -e ../../awc-spec
pip install -e .
```

## Example CLI run

```bash
awc-runtime \
  --agent ../examples/agents/sales-agent.yaml \
  --task "Customer asks for a discount" \
  --action "reply_inbound_dm" \
  --confidence 0.65 \
  --report
```

## Tests

```bash
python -m unittest discover -s tests
```
