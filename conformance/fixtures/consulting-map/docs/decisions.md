# Decision log

Entries are immutable. Each carries a stable `ID`, which is how a research entry
points at the decision it enables.

## Decision: Keep the fixture minimal

- ID: D1
- Status: accepted
- Decided: {{TODAY}}
- Sources: https://example.invalid/alpha
- Recheck: if the fixture stops exercising the coverage check

Rationale: the fixture exists so the corpus can prove that a concern map which
misses a registered evidence domain is reported as a failure.
