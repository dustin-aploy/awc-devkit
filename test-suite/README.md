# AWC Test Suite

`awc-test-suite` is the conformance and certification foundation for AI Work Contract (AWC), formerly ARP.

It depends on:
- `../../awc-spec` for protocol schemas and version truth
- `../runtime` for a reference execution path used in local validation flows

It is responsible for building protocol-shaped `AWCComplianceReport` artifacts and validating AWC behavior, audit, and reporting expectations.

For Phase 1 self-hosted onboarding, it also provides lightweight checks for:

- declaration validity;
- minimal self-hosted metadata presence;
- example loadability; and
- mock invocation/healthcheck config shape.

## Install locally

```bash
pip install -e ../../awc-spec
pip install -e ../runtime
pip install -e .
```

## Run tests

```bash
pytest tests
```
