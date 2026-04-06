# AWC Adapters

`awc-devkit/adapters` contains thin integration guidance for mapping external frameworks and environments onto AI Work Contract (AWC) concepts.

Adapters must:
- depend on normative concepts from `../../awc-spec`
- align with reference behavior from `../runtime` when useful
- avoid redefining AWC protocol semantics or turning the workspace into a framework monolith

This phase also includes a minimal self-hosted HTTP adapter stub to show how an integrator could call a third-party worker without introducing a managed runtime layer.
