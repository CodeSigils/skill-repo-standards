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
| R-012 | Whether truth needs one owner, and which document owns repository facts versus installed behaviour | Complete | 2026-10-15 | D15 |
| R-013 | Whether a verification-command list duplicated across the README, the hooks, and CI warrants a shared manifest now | Complete | 2026-10-15 | D16 |
| R-014 | Whether the standard should explain its relationship to the established practice families and publish a next-steps list | Complete | 2026-10-15 | D17 |
| R-015 | Whether a gate can be added to a hook or workflow without the README documenting it, and whether a definite HTTP status must not be mistaken for an environmental failure | Complete | 2026-10-15 | D18 |
| R-016 | Whether a repository that pins Actions by SHA should adopt Dependabot, and whether it should adopt uv and Python dependencies | Complete | 2026-10-15 | D19 |
| R-017 | Whether a claimed conformance grade should be backed by a checked-in corpus that proves the validator behaves correctly across known shapes | Complete | 2026-10-15 | D20 |
| R-018 | Whether a corpus must exercise every check the validator performs, so a regression in an unchecked branch cannot pass in silence | Complete | 2026-10-15 | D21 |

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

## R-012 — One owner of truth

The documentation-drift sources agree that a document rots when it hand-duplicates
a source of truth, and that what can be derived should be derived while what cannot
should be watched. Separately, the agentskills specification ships each skill as a
self-contained directory whose files are copied into a host where the authoring
repository does not exist. Together they imply two owners of truth that must not
cross: the mutable current-state document owns what is true about the repository,
and the runtime payload owns what an installed skill does, with the payload kept
from linking into the repository's documents. Recorded as the basis for the
one-owner-of-truth bullet in `STANDARD.md` §The anti-rot core.
Sources: https://artel.run/docs/documentation/ ,
https://agentskills.io/specification

## R-013 — The duplicated verification-command list

The verification commands appear in the README, the reference-validator section of
`STANDARD.md`, the git hooks, and the CI workflow. The same duplication class was
solved in a sibling repository by sourcing the list from one module and asserting
that CI contains it — but this standard already defers "a shared stage manifest
spanning more than two surfaces", and fitness-function practice says a control is
adopted only when its failure mode is observed. The failure mode here, a
verification command silently dropped from one surface, has not been observed, so
the proportionate response is to record the duplication and keep the control
deferred. Recorded so the gap is visible rather than rediscovered.
Sources: https://continuous-architecture.org/practices/fitness-functions

## R-014 — Explaining the standard and publishing a next-steps list

A reader who arrives at the repository learns what it is but not why it exists
beside ADR practice, fitness functions, freshness tooling, and the agent-discovery
formats; the agent-instruction and discovery conventions both expect a front door
that orients a human or an agent. Separately, committed-but-unbuilt work needs one
discoverable place for both audiences, and a second forward-looking document would
be another rot surface. Recorded as the basis for a front-door explanation in the
README and a `## What is next` section in the mutable current-state document.
Sources: https://agents.md/ , https://llmstxt.org/

## R-015 — Documented gates and definite HTTP statuses

A repository can add a gate to a hook or a workflow and never add it to the
README verification block, so a reader cannot see what actually runs. And a URL
check that treats any non-2xx reply as an environmental failure hides a definite
drift behind a "could not check". Both are the failure the anti-rot core exists to
catch — a machine-checkable fact that no check treats as a finding. The
proportionate response is detection, not a new manifest: a soft cross-surface
check, and classifying a definite HTTP status as drift rather than as an
environmental error. Recorded as the basis for the cross-surface check and the
`HTTPError`-aware URL verifier.
Sources: https://continuous-architecture.org/practices/fitness-functions

## R-016 — Dependabot, and why uv is declined

Pinning an Action to a full commit SHA is what makes it immutable, and it is also
what makes it go stale in silence: nothing in the repository reports that the tag
moved. That is a named failure mode the repository already has, so it is the one
optional control worth adopting here. The shape is taken from the fleet's own
research note, `repo-architecture-skill/docs/research/automation-bots-and-workflows.md`
(reviewed 2026-09-08): `github-actions` only, weekly, grouped minor and patch,
capped at two open pull requests, no auto-merge, and major updates taken
deliberately.

That note also records a subtlety worth keeping. The official documentation says a
dependency joins the *first* group it matches; the note states that the updater
implements *most-specific*-match. Its disjoint `update-types` design makes the two
readings indistinguishable, which is more robust than relying on either one. It
also records why `exclude-patterns` is unused: excluding a dependency from a group
does not skip it — it becomes an ungrouped pull request, including for majors,
which increases review load rather than reducing it.

Two facts postdate that note (2026-09-08). `cooldown` now applies a default
three-day cooldown to version updates even when unconfigured, and it does not apply
to security updates; its support for the `github-actions` ecosystem could not be
confirmed from the fetched documentation, so it is not used. And
`open-pull-requests-limit: 0` disables version updates for an ecosystem, which is
the documented way to take security updates only. A separate documentation
contradiction — whether a fixed limit applies to security-update pull requests —
is unresolved upstream and does not affect this configuration.

`uv` and Python dependencies are declined rather than deferred. They would add a
package manager, a lockfile, a linter and type checker, their pre-commit wiring, a
second SHA-pinned action in CI, and a weekly stream of tooling pull requests — to a
repository whose three scripts import only the standard library and have nothing to
install. A type checker would not have caught the two real defects a review found
here (an exception-hierarchy bug and a control-flow bug), so the control fails the
standard's own proportionality rule.
Sources: https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference , https://github.com/CodeSigils/repo-architecture-skill

## R-017 — Back the grade claim with a checked-in corpus

The validator's `--self-test` builds fixtures in a temporary directory, asserts
that the expected findings fire, and deletes them. That proves the checks can
fail, but nothing survives the run and no fixture asserts the result a real
repository would see. So a claimed grade rested on a self-check that was never
itself reproducible by a reader.

Published conformance practice treats that as the weak case. The W3C QA
guidelines call for a conformance clause plus a pro forma implementation
conformance statement; HushSpec requires a statement to name the claimed level,
the specification version, and a machine-readable report, on the grounds that a
statement without the report is an assertion, not evidence; AXL grades
conformance in levels from self-attested through verified review and gives the
statement a validity period.

The proportionate response here is a small corpus checked into the repository:
fixture repositories in known shapes, an expected-results manifest, and a runner
that reproduces each result. Two questions were settled while building it. The
corpus asserts the exact set of hard and soft findings and the exit code, rather
than inventing a grade letter the validator does not compute. And fixtures carry
date tokens that the runner renders at run time, because a checked-in fixture
with a fixed date would rot into failure once it fell outside the freshness
window.

Sources: https://hushspec.org/docs/conformance-statement , https://axlspec.org/conformance , https://www.w3.org/TR/qaframe-spec/specgl-ics.html

## R-018 — Covering every validator check

The first corpus was built from the shapes the adoption survey had already
exposed: a grade A repository, a grade B repository, a repository whose decision
log and research record use unparsed shapes, a repository with stale evidence,
and a broken repository. Reading the validator against that list showed the
corpus exercised four of its seven checks. `check_standard`,
`check_payload_boundary`, and `check_consistency` had no fixture at all, and two
branches of covered checks — a skill whose frontmatter name does not match its
directory, and an evidence index that is malformed rather than stale — were
untested.

A conformance corpus that checks part of a validator while presenting itself as
the evidence for the validator's behaviour has the same defect it was built to
remove, one level up: the claim outruns the check. HushSpec's guidance is that a
statement without its report is an assertion; the same reasoning applies to a
corpus with silent blind spots. The proportionate response was five more
fixtures rather than a new mechanism, and a sentence in `STANDARD.md` stating
that every check is exercised, so a future check arriving without a fixture is a
visible omission instead of an invisible one.

Single-line edge cases inside a check — a duplicate research id, an `Enables`
target naming no decision, a duplicate decision id — stay with the validator's
own `--self-test`, which builds a fixture, mutates one input, and asserts the
rejection. Duplicating them in the corpus would add files without adding
coverage of a distinct failure mode.

Sources: https://hushspec.org/docs/conformance-statement , https://www.w3.org/TR/qaframe-spec/specgl-ics.html
