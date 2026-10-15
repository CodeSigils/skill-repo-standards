# Research record

**Append-only.** Entries are dated and never retro-edited. New evidence is
appended; a superseded entry is marked superseded with a pointer to its
successor, never rewritten. When a finding becomes durable it is promoted into
`docs/current-state.md` or recorded as a decision in `docs/decisions.md`.

The "Last Verified" column records when the entry was last checked, not a claim
that the underlying source has not changed since.

| ID | Concern | Status | Last Verified | Enables |
| --- | --- | --- | --- | --- |
| R-001 | Whether a written specification plus a reference validator is the right shape for a shared standard | Complete | 2026-10-15 | D1 |
| R-002 | Whether decision records should be mutable or immutable | Complete | 2026-10-15 | D2 |
| R-003 | Which external anti-rot tooling to adopt versus defer | Complete | 2026-10-15 | D3 |
| R-004 | Which durable-context building blocks exist, which to adopt or defer, and whether the standard's own change process should be enforced | Complete | 2026-10-15 | D1, D2, D3, D4 |
| R-005 | How a shared standard should version itself, classify its own changes, and schedule its own review | Complete | 2026-10-15 | D6, D11 |
| R-006 | Whether the standard needs normative requirement language, a conformance claim, and a rule that resolves document conflicts | Complete | 2026-10-15 | D5, D7 |
| R-007 | How a repository should carry a validator finding it chooses not to fix, without disabling the check | Complete | 2026-10-15 | D8 |
| R-008 | Which licence and change-record conventions apply when a standard is published for others to implement | Complete | 2026-10-15 | D9, D10 |
| R-009 | Whether a shared standard should grade its validator findings by severity so a deliberately different repository can adopt it | Complete | 2026-10-15 | D12 |
| R-010 | Whether the standard should hard-encode one shape of a decision log, a research register, or a skill payload | Complete | 2026-10-15 | D13 |
| R-011 | Whether a shared standard should be published as a standalone public repository so others can adopt it by copy | Complete | 2026-10-15 | D14 |

## R-001 — Specification plus validator

The agentskills project publishes a canonical specification alongside a reference
validator rather than prose alone. Recorded because this repository mirrors that
shape. Source: https://agentskills.io/specification

## R-002 — Immutable decision records

MADR, AWS prescriptive guidance, and the log4brains tooling agree that a decision
record is immutable after acceptance and superseded rather than rewritten.
Sources: https://adr.github.io/madr/ ,
https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html ,
https://github.com/thomvaill/log4brains

## R-003 — Anti-rot tooling: adopt patterns, defer tools

The documentation-drift and agent-memory sources describe the same recurring
principles: derive what can be derived, watch what cannot, never fail freshness
open, and treat external tooling as evidence rather than a drop-in. Recorded as
the basis for adopting the anti-rot pattern while deferring the tools.
Sources: https://artel.run/docs/documentation/ ,
https://datadef.io/guides/en/docs-checks-in-ci ,
https://docs.thally.io/guides/provenance ,
https://github.com/AgentMemoryWorld/Awesome-Agent-Memory

## R-004 — Durable-context landscape and the enforced change lifecycle

A survey of the durable-context field found five recurring building blocks:
decision records (MADR, AWS, log4brains), executable governance (fitness
functions), freshness and provenance (who checked what, and when), agent
discoverability (AGENTS.md, llms.txt), and agent memory (anti-recurrence stores
for decisions and dead ends). `STANDARD.md` already covers the first, fourth, and
most of the second and fifth; freshness is covered only as HTTP status and a
date, with git-history freshness left deferred. The survey also showed that an
unstated process is not followed, so the standard's own change lifecycle is
written down and its research-to-decision edge is made machine-checkable.
Sources: https://agents.md/ ,
https://llmstxt.org/ ,
https://continuous-architecture.org/practices/fitness-functions ,
https://docs.thally.io/guides/provenance ,
https://artel.run/docs/documentation/ ,
https://github.com/AgentMemoryWorld/Awesome-Agent-Memory

## R-005 — Standard lifecycle: change classes and review cadence

Established specification projects define a lifecycle for the document itself —
draft, review, stable, deprecated, superseded — and tie each class of change to a
version bump: editorial changes bump nothing, compatible clarifications and
extensions bump the minor version, and breaking changes bump the major version
and need migration guidance. The same sources expect a declared last substantive
update and a review trigger, because an unreviewed claim is how rot starts.
Recorded as the basis for the standard's own lifecycle section and its twice-a-
year review cadence.
Sources: https://www.openmanuscript.org/docs/governance/specification-lifecycle ,
https://github.com/TIDES-transit/TIDES

## R-006 — Normative language, conformance claims, and precedence

Specification and conformance guidance agree on three things a written standard
needs: a normative requirement vocabulary (MUST/SHOULD/MAY) separated from
informative prose, a conformance clause that says what a claim means and how it
is evidenced, and a precedence rule that names the document that wins when two
disagree. The W3C QA guidance frames the conformance-claim guidance; opentide's
governance states that its specification is the source of truth and wins on
conflict. Recorded as the basis for `## Normative language`, the conformance
paragraph, and the precedence rule that resolves to `STANDARD.md`.
Sources: https://www.w3.org/TR/qaframe-spec/specgl-ics.html ,
https://opentide.org/docs/specifications/GOVERNANCE

## R-007 — Carrying an accepted finding without disabling the check

Fitness-function practice separates an observed baseline from a time-bound
waiver and expects every accepted exception to expire and be re-evaluated;
provenance guidance adds that an unverifiable result must never be reported as
resolved. Together they give a repository two distinct mechanisms — a baseline
that records what was seen and never waives, and an exception that waives but
expires — so a known finding stays visible instead of being silenced by turning
the check off. Recorded as the basis for `## Accepted findings`.
Sources: https://continuous-architecture.org/practices/fitness-functions ,
https://docs.thally.io/guides/provenance

## R-008 — Licensing and change-record conventions for a published specification

Licensing guidance distinguishes a source-code licence from a documentation or
specification licence, and notes that a specification published for others to
implement often needs its own licence and an explicit IP position. Separately,
some specification projects require a changelog as part of their release
checklist. Recorded so the repository's current single MIT licence and its
deliberate absence of a CHANGELOG are both conscious, deferred-until-published
choices rather than oversights.
Sources: https://www.linuxfoundation.org/licensebestpractices ,
https://github.com/TIDES-transit/TIDES

## R-009 — Grading findings by severity

Dogfooding the reference validator against real repositories showed that a
standard which only ever fails cannot be adopted by one that is deliberately
different: the reference implementation has no research ledger by design, so the
research-to-decision edge and the decision identifier cannot be universal hard
rules. Fitness-function practice keeps a finding visible without disabling the
check, and provenance guidance keeps an open gap reported rather than hidden.
Together they support two severities — a hard finding that fails the run and a
soft finding that is advisory and fails only under `--strict`. Recorded as the
basis for grading findings by severity and downgrading the two rules above.
Sources: https://continuous-architecture.org/practices/fitness-functions ,
https://docs.thally.io/guides/provenance

## R-010 — Widening the accepted shapes

Running the reference validator against twelve repositories separated genuine
gaps from shape mismatches. Six conformed with no findings. Of the five that
failed, one was a real gap (a minimal repository with no `SECURITY.md`); the
other four had the right practice in a different shape: a multi-skill payload
with six skill directories, a decision log headed with prose titles and
`**Decision:**` labels, and two research registers that are dated records rather
than `R-###` tables. The agentskills specification treats a directory of skills
as normal, so demanding exactly one skill directory contradicted the format the
standard is built on. The proportionate response is to widen what satisfies a
requirement while keeping the requirement: accept multiple skill directories
(each named for its skill, each with its own payload boundary), accept the
common ADR heading forms, and report an unrecognised shape as an advisory note
rather than a hard failure. With these changes eleven of the twelve repositories
adopt cleanly or with advisory notes, and the one remaining failure is the
genuine missing `SECURITY.md`. Sources: https://agentskills.io/specification ,
https://continuous-architecture.org/practices/fitness-functions

## R-011 — Publishing the standard

Whether a shared standard should be published as a standalone public repository,
so that a repository that did not help write it can adopt the same document and
validator by copy. A local-only standard cannot be tested for generality: the
only evidence that it serves others is another person adopting it. The format it
builds on is distributed exactly this way — a canonical specification plus a
bundled validator in a public repository — and the adoption survey in R-010 is
the first evidence that the standard transfers beyond the repositories that
inspired it. Enables D14. Sources: https://agentskills.io/specification
