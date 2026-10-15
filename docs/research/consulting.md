# Research consultation

This is the standard's standalone, concern-oriented lookup path. It does not
depend on any personal lab or another repository. The normative protocol is
[`STANDARD.md` §The anti-rot core](../../STANDARD.md#the-anti-rot-core); this
file makes its existing records discoverable before a researcher looks outward.

## Consult first

For a research-sensitive concern, in order:

1. Search [`../decisions.md`](../decisions.md) for an accepted, superseded, or
   deferred decision.
2. Search [`../evidence-urls.json`](../evidence-urls.json) by `domain_tag` for
   registered primary sources and check their `last_verified` date.
3. Search [`index.md`](index.md) for the append-only finding that enables the
   decision.
4. Reuse a current, applicable result with a link; otherwise research official
   guidance, append a finding, then record any behaviour-changing decision.

The machine-readable evidence index is the source registry. This guide owns
only the query order and concern map; it must not become a second source list.

## Appraise before deciding

Before a behaviour-changing decision, state the question and scope, compare the
source's authority and applicability to the repository, name material
limitations, and record the recheck trigger. For a material multi-option choice,
record the alternatives and consequences in the decision rationale. Use the
[evidence-appraisal profile](evidence-appraisal.md) for a new
behaviour-changing decision, and the [trade-study template](trade-study.md)
only when its materiality warrants it. The validator enforces source
provenance, freshness, the research-to-decision link, and an opted-in profile's
shape; it deliberately cannot score the truth or weight of prose evidence.

## Concern map

| Concern | `domain_tag` | Read first | Recheck when |
|---------|--------------|------------|--------------|
| Research-first, evidence-baked decisions | `research-consultation` | R-019 and D22 | a primary source changes or a new consultation flow is proposed |
| Repository security, secrets, and ignore rules | `repository-security` | R-019 and D22 | GitHub changes the guidance or the target uses another hosting platform |
| Evidence appraisal and material trade studies | `research-consultation` | R-020 and D23 | a decision needs a multi-option comparison or its evidence changes |
| Evidence-appraisal profile and source sufficiency | `research-consultation` | R-021 and D24 | a profile is incomplete or a primary source is unavailable |

Use the concern map to locate sources, not to apply a generic policy. The target
repository owns the decision and may have a narrower scope.
