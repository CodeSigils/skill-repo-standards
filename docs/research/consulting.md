# Research consultation

This is the standard's standalone, concern-oriented lookup path. It does not
depend on any personal lab or another repository. The normative protocol is
[`STANDARD.md` §The anti-rot core](../../STANDARD.md#the-anti-rot-core); this
file makes its existing records discoverable before a researcher looks outward.

## Evidence-first workflow

For every research-sensitive concern or coverage review, in order:

1. **Classify the request.** Identify the concern and whether the user is asking
   for a decision, an implementation, or a review of the concern map itself.
2. **Consult local evidence first.** Use the concern map, then search
   [`../decisions.md`](../decisions.md),
   [`../evidence-urls.json`](../evidence-urls.json) by `domain_tag`, and
   [`index.md`](index.md). Check source freshness and the finding's scope.
3. **Reuse or revalidate.** Link to a current, applicable result. Revalidate a
   volatile, version-sensitive, or decision-critical fact at the point of use;
   do not repeat a search silently.
4. **Audit coverage when asked.** Compare the concern map against the evidence
   registry and recent decisions. If a recurring, decision-worthy concern has
   no route, no current applicable finding, or no authoritative source, research
   official guidance on the web. A coverage review is not by itself a reason to
   add a control.
5. **Record the finding.** Append an `R-###` entry with the question and scope,
   sources and applicability, material limitations, check date, and recheck
   trigger. Register every cited source in the evidence index.
6. **Decide only when behaviour changes.** Create a linked `D#` record with the
   [evidence-appraisal profile](evidence-appraisal.md) and an observable outcome
   check. For a material multi-option choice, also record alternatives and
   consequences; use the [trade-study template](trade-study.md) only when its
   materiality warrants it.
7. **Implement and verify proportionately.** Add only the control justified by
   the observed failure mode, update the machine-checkable validator and its
   self-test where applicable, then run the documented deterministic checks.

The machine-readable evidence index is the source registry. This guide owns the
workflow and concern map; it must not become a second source list or a generic
policy catalogue.

## Concern map

| Concern | `domain_tag` | Read first | Recheck when |
|---------|--------------|------------|--------------|
| Research-first, evidence-baked decisions | `research-consultation` | R-019 and D22 | a primary source changes or a new consultation flow is proposed |
| Repository security, secrets, and ignore rules | `repository-security` | R-019 and D22 | GitHub changes the guidance or the target uses another hosting platform |
| Evidence appraisal and material trade studies | `research-consultation` | R-020 and D23 | a decision needs a multi-option comparison or its evidence changes |
| Evidence-appraisal profile and source sufficiency | `research-consultation` | R-021 and D24 | a profile is incomplete or a primary source is unavailable |
| Decision records and ownership of repository facts | `decision-records` | R-002, R-012, D2, and D15 | a record shape, owner, or status-transition rule changes |
| Documentation freshness and verification-surface drift | `documentation-freshness`, `executable-governance` | R-003, R-013, R-015, D3, D16, and D18 | a source becomes stale, a gate is undocumented, or a command is dropped from a surface |
| Dependency automation and CI supply-chain maintenance | `dependency-automation` | R-016 and D19 | a dependency ecosystem is added or the update mechanism changes |
| Conformance claims and validator assurance | `conformance` | R-017, R-018, R-028, D20, D21, and D30 | a validator check lacks fixture coverage, the corpus's own coverage claim goes uncomputed, or a claim needs reproducible evidence |
| Skill format and agent discovery | `skill-format`, `agent-discoverability` | R-004, R-010, and D13 | the format or a supported discovery path changes |
| Maintainer cold boot: read order and state pre-flight | `agent-discoverability` | R-004, R-027, and D29 | the entry file, the read order, or a supported discovery surface changes |
| Runtime compatibility claims and distributed-skill trust | `skill-runtime-trust` | R-022 and D25 | a skill adds executable support, a platform-specific adapter, or a named-runtime claim |
| Specification lifecycle, governance, and licensing | `specification-lifecycle`, `specification-governance`, `licensing` | R-005, R-006, R-008, D6, D7, D9, D10, and D11 | publication, a version/status transition, or licence scope changes |
| Maintainer memory services and external research aids | `agent-memory` | R-003, R-004, and D3 | repeated research defeats the local records, or a hosted service is proposed |
| State-changing git/VCS actions, branch lifecycle, and the release surface | `vcs-hygiene` | R-031 and D33 | GitHub changes branch-protection or merge semantics, or the gate check blocks a repository that conforms |

Use the concern map to locate sources, not to apply a generic policy. The target
repository owns the decision and may have a narrower scope.
