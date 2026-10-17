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
| R-019 | Whether recurring concerns need a standalone, concern-oriented consultation path so official guidance is located before a project decision | Complete | 2026-10-15 | D22 |
| R-020 | Which evidence-first controls are enforceable in a proportionate skill-repository standard | Complete | 2026-10-15 | D23 |
| R-021 | Which evidence-appraisal, source-sufficiency, and material-trade-study controls improve decisions without inventing a universal score | Complete | 2026-10-15 | D24 |
| R-022 | Whether the consultation map covers recurring maintenance concerns and distinguishes repository security from distributed-skill trust and runtime compatibility | Complete | 2026-10-16 | D25 |
| R-023 | What primary platform guidance establishes about executable skills, installation consent, and the evidence needed for runtime compatibility claims | Complete | 2026-10-16 | D25 |
| R-024 | Whether a coverage-review request should trigger a local evidence audit before targeted official web research | Complete | 2026-10-16 | D26 |
| R-025 | Whether a concern map that routes fewer domains than the evidence index declares should be a checked failure | Complete | 2026-10-16 | D27 |
| R-026 | Whether the change lifecycle should name the full artifact set a machine-checkable standard change must ship | Complete | 2026-10-16 | D28 |
| R-027 | Whether a maintainer agent's cold-boot read order and state pre-flight are complete enough to avoid acting on an incomplete picture | Complete | 2026-10-16 | D29 |
| R-028 | Whether the corpus's coverage promise needs a computed check once a prose-visible omission is known to have failed elsewhere | Complete | 2026-10-16 | D30 |
| R-029 | Whether release history needs an explicit one-version-per-commit rule after two migration notes shipped together | Complete | 2026-10-16 | D31 |
| R-030 | Whether a draft standard needs immutable release artifacts and an event-driven release cadence | Complete | 2026-10-16 | D32 |
| R-031 | Whether a fleet of related repositories drifts when gating is advisory, and which git/VCS and release-surface hygiene a maintainer standard should require | Complete | 2026-10-17 | D33 |

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
Sources: https://agents.md/ ,
https://llmstxt.org/

## R-028 — Computed corpus coverage over prose-visible omission

R-018 answered the question "must the corpus cover every check the validator
performs" with yes, and deliberately chose five more fixtures plus a sentence in
`STANDARD.md` over a mechanism, on the grounds that the sentence makes a future
omission visible to a reader. A coverage review of that same class of claim
found the premise does not hold: the consultation concern map had been routing
fewer domains than the evidence index declared while every sentence asserting
completeness still read true. Visibility was not enforcement, and the omission
was only found by a review nobody was forced to run.

The gap is therefore not whether the corpus must cover the validator — R-018
settled that — but whether the covering claim is checked by anything at all.
Standards guidance treats coverage as computed data rather than prose: the W3C
test method requires at least one test case for every conformance requirement
and binds each to a stable identifier precisely so that coverage can be
assessed, and the W3C QA test guidelines require the percentage of assertions
with at least one test case to be calculated and published. A repository that
asserts fixture coverage without computing it is doing exactly what those
guidelines were written to prevent.

The proportionate control is a second pass in the runner that already exists.
The corpus is thirteen tiny fixtures, so recording which checks each fixture
reaches, and which of them return a finding the manifest records, costs
negligibly and needs no new file, no manifest field, and no adopter-facing rule:
no conformance grade requires an adopter to ship a corpus, so the guard belongs
with the repository's own self-assurance rather than in the validator. What it
cannot do is prove branch coverage, only that a check is wired in and that its
output appears somewhere in the expected results — enough to turn D21's
unverified sentence into a failing command.

Sources: https://www.w3.org/TR/test-methodology/ ,
https://www.w3.org/QA/WG/2003/10/TestGL-20031020.html

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

## R-019 — Research-first, concern-oriented consultation

Evidence-Based Software Engineering frames evidence use as asking an answerable
question, locating the best available evidence, critically appraising it, and
integrating it with practitioner judgment. GOV.UK's evidence-led assurance
guidance makes the operational chain explicit: signals and metrics become
evidence, assertions, and decisions. MADR then preserves the context, options,
outcome, and consequences of the resulting decision.

The recurring repository-security concern demonstrates why a lookup must be
discoverable. GitHub documents that `.gitignore` does not remove tracked files,
maintains reusable ignore templates, and recommends a security baseline that
includes secret scanning, push protection, code scanning, dependency alerts, and
`SECURITY.md`. A target repository still decides which controls fit its scope;
the consultation guide merely ensures official guidance is found before that
decision, rather than repeatedly rediscovered.

Sources: https://ebse.webspace.durham.ac.uk/ ,
https://www.gov.uk/government/publications/evidence-led-assurance-for-the-software-development-lifecycle ,
https://adr.github.io/madr/ ,
https://docs.github.com/en/get-started/git-basics/ignoring-files ,
https://docs.github.com/en/enterprise-cloud%40latest/repositories/creating-and-managing-repositories/best-practices-for-repositories ,
https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention/push-protection-on-the-command-line ,
https://github.com/github/gitignore

## R-020 — Proportionate enforcement of evidence-first decisions

Evidence-Based Software Engineering requires an answerable question, the best
available evidence, critical appraisal, and a decision integrated with local
judgment. GOV.UK's assurance model makes the chain explicit: signals and
metrics become evidence, assertions, and decisions; evidence is perishable.
AWS ADR guidance requires a context, decision, and consequences in an immutable
record. FHWA trade studies add alternatives and objective comparison when a
choice is material and has multiple options.

For this standard, source provenance, check dates, unique identifiers, and the
research-to-decision link are objective repository facts, so they are
machine-enforced once both records use the recognised shapes. Appraisal quality,
stakeholder judgment, and trade-study weights remain human review: the validator
cannot assess their truth, and no repository failure shows that a mechanical
rubric would improve the result. A material multi-option choice is instead
guided to record alternatives and consequences in its rationale.

Sources: https://ebse.webspace.durham.ac.uk/ ,
https://www.gov.uk/government/publications/evidence-led-assurance-for-the-software-development-lifecycle ,
https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html ,
https://ops.fhwa.dot.gov/seits/sections/section3/3_4_5.html

## R-021 — Structured appraisal without a universal evidence score

The 2025 EBSE guidelines revisit the need for guidance that reflects changed
software practice. The credible-evidence framework describes validity,
relevance, and fit-for-purpose as distinct concerns, and warns consumers not to
repeat claims without evaluating their credibility. EBSE's five-stage process
requires appraisal of validity, impact, and applicability, integration with
stakeholder circumstances, and review of effectiveness. AWS ADR guidance adds
context and consequences; FHWA trade studies add alternatives, criteria, and
validation of a material choice.

The smallest justified control is an opt-in profile for new behaviour-changing
decisions: context, a human evidence appraisal, an outcome check, and a source
sufficiency declaration. A `primary` profile requires an official source; a
`constrained` profile records why one is unavailable. This makes missing fields
and source provenance machine-checkable without pretending that an automated
score can establish evidence quality. A Grade C trade-study template is supplied
for material multi-option choices. Evidence hierarchy, recommendation strength,
universal weights, and sensitivity scoring remain deferred: no observed failure
shows that their universal enforcement would improve this repository class.

Sources: https://ebse.webspace.durham.ac.uk/ ,
https://doi.org/10.1109/TSE.2025.3526730 ,
https://doi.org/10.1016/j.infsof.2021.106555 ,
https://www.gov.uk/government/publications/evidence-led-assurance-for-the-software-development-lifecycle ,
https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html ,
https://ops.fhwa.dot.gov/seits/sections/section3/3_4_5.html

## R-022 — Consultation coverage, distributed-skill trust, and runtime compatibility

The consultation map exposed only four concerns even though the evidence registry
already held sources for decision records, documentation freshness, dependency
automation, conformance, discovery, lifecycle, licensing, and maintainer memory.
Those existing findings are reusable but were not reachable by concern.

The Agent Skills specification permits executable `scripts/` and an optional
`compatibility` declaration. It therefore defines an artifact format, not a
proof that a named runtime installs, authorizes, or executes a skill safely.
Claude Code documents additional invocation, dynamic-context, and permission
features beyond the portable format. Its workspace trust requirement for plugin
loading is further evidence that host approval and executable support files are
deployment concerns rather than properties inferred from `SKILL.md` alone.

The appropriate response is a complete lookup map and a distinct research
concern for runtime compatibility and distributed-skill trust. It does not add a
universal safety or compatibility control: a target repository decides whether
its executable support, adapter, or runtime claim creates that failure mode.

Sources: https://agentskills.io/specification ,
https://code.claude.com/docs/en/skills

## R-023 — Evidence boundary for executable skills and runtime claims

**Question and scope.** What can a shared skill-repository standard responsibly
say about executable support, distribution trust, and runtime compatibility
without treating one host's safety model as portable policy? This finding covers
skills that ship scripts, adapters, plugin metadata, hooks, MCP configuration,
or a claim about a named runtime. It does not prescribe a runtime's installation
path or permission model.

**Evidence and appraisal.** The Agent Skills specification defines a portable
directory format that may contain scripts and an optional compatibility
declaration, but it leaves supported languages and host behavior to the agent
implementation. OpenAI documents that a plugin can package skills with MCP
configuration, so instruction files and controlled actions remain separate
surfaces. Claude Code likewise follows the common format but adds invocation,
dynamic-context, and permission extensions. Gemini CLI documents remote-install
confirmation and per-activation consent because skills can execute scripts and
access files. Hermes documents source provenance, content scanning, quarantine,
and update checks for installed skills.

**Finding.** Format validity, installation/discovery, and representative runtime
workflow are separate claims; success at one level does not establish the next.
Executable support, an adapter, or a distribution package therefore creates a
repository-specific trust boundary. The evidence supports requiring an explicit
target, version, installation or discovery procedure, and recorded limitations
before a repository upgrades a compatibility claim. It does not support a common
mandatory scanner, consent flow, or trust policy, because the hosts deliberately
implement those controls differently.

**Limitations and recheck.** This is official documentation for current intended
behavior, not an installation test. Recheck it when a repository adds executable
support or a runtime-specific adapter, makes a portability or safety claim, or a
named host changes its skill/distribution model. Reuse the format evidence only
for format questions; record a named-runtime test before asserting installation
or workflow compatibility.

Sources: https://agentskills.io/specification ,
https://developers.openai.com/plugins/concepts/skills ,
https://code.claude.com/docs/en/skills ,
https://geminicli.com/docs/cli/using-agent-skills/ ,
https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/

## R-024 — Coverage review as an evidence-first research trigger

A concern map prevents repeated research only while it remains aligned with the
evidence registry and the decisions it supports. Evidence-based software
engineering begins with an answerable question and available evidence before
looking outward; GOV.UK's assurance guidance makes the sequence explicit by
turning evidence into an accountable decision. For this repository, a coverage
review is the answerable question: whether a recurring, decision-worthy concern
can be located through current, applicable recorded evidence.

The smallest reliable workflow is to compare the concern map with registered
source domains and recent decisions first. Only an unmatched concern, stale or
inapplicable finding, or absent authoritative source warrants targeted official
web research. The resulting `R-###` finding records the scope, applicability,
limitations, and recheck trigger; a `D#` follows only if the finding changes
repository behaviour. This avoids both silent re-research and adopting a control
merely because a coverage review named a concern.

Sources: https://ebse.webspace.durham.ac.uk/ ,
https://www.gov.uk/government/publications/evidence-led-assurance-for-the-software-development-lifecycle

## R-025 — Consultation-map coverage as a checked failure

A concern map can silently route fewer domains than the evidence index declares.
The demonstrated case mapped four routes over fourteen declared domains. A narrow
check turns that drift into a failure without turning the coverage review itself
into a control.

Sources: https://www.gov.uk/government/publications/evidence-led-assurance-for-the-software-development-lifecycle

## R-026 — The change lifecycle should name every shipped artifact

A procedure that states only its first artifact lets a later one be forgotten.
Step 4 of the change lifecycle named the validator and its self-test but left the
conformance fixture, the version bump, and the paired records implicit, so a
machine-checkable change could satisfy the step while leaving the corpus
unexercised. Stating the whole artifact set at the point of change turns the
corpus's fixture promise from a separate assertion into a step the process itself
demands.

Sources: https://www.gov.uk/government/publications/evidence-led-assurance-for-the-software-development-lifecycle

## R-027 — Cold-boot coverage for maintainer agents

The durable-context survey (R-004) established agent discoverability as a
building block: a repository exposes one entry file an agent reads first. This
repository already had `AGENTS.md` with a read order, but nothing recorded
whether that entry is complete enough for a cold first run — the read order did
not name the consultation guide or the conformance claim, and nothing told an
agent to check working-tree and CI state or to run the gates before changing
anything. A coverage review found the discoverability concern routed only in its
skill-format sense, so maintainer onboarding was adjacent prior art, not
coverage. The registered `agent-discoverability` sources support the premise that
one discoverable entry file governs how an agent starts; acting on an incomplete
entry is the failure mode, so the proportionate control is prose in the entry
file, not a new validator check.

Sources: https://agents.md/ ,
https://llmstxt.org/

## R-029 — One released version per version-changing commit

The 2.4 release introduced both a 2.3 migration note and a 2.4 migration note,
so the history contains no checkout labelled 2.3. The resulting release is
coherent, but a reader cannot inspect the two migrations independently. The
repository's change lifecycle already treats a version bump as a named artifact;
the remaining gap is that the standard lifecycle did not say whether one commit
could represent multiple released versions.

For future version-changing commits, one commit represents one released version.
Independently reviewable changes either land as sequential versioned commits or
share one deliberate release version and migration note. The historical 2.3 note
is retained and explicitly marked as published with 2.4, rather than rewriting
shared history or inventing an unavailable version.

Sources: https://www.gov.uk/government/publications/evidence-led-assurance-for-the-software-development-lifecycle

## R-030 — Draft-release artifact and cadence

The public standard had a versioned document and a passing conformance snapshot,
but no tag or GitHub release. A reader could locate the draft only by navigating
moving branch history, so the claimed version was not a named adoption artifact.

Git distinguishes annotated tags, which carry tagger metadata and a message,
from lightweight labels, and identifies annotated tags as release objects.
GitHub releases are based on tags and support a prerelease state. Those mechanics
support one annotated tag and one prerelease for every normative draft version;
they do not justify calendar releases or tags for ordinary maintenance commits.

The rule is limited to publication mechanics. `STANDARD.md` retains ownership of
what a version means, and a status transition is rechecked before a stable release
is claimed. Existing history remains untagged because a retrospective tag would
invent a release date and publication decision that did not occur.

Sources: https://git-scm.com/docs/git-tag ,
https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository

## R-031 — Fleet CI rot and state-changing git/VCS hygiene

**Question and scope.** Which recurring failures appear when a group of related
repositories gate on advisory checks rather than a conformance claim, and which
git/VCS and release-surface controls a maintainer standard can require without a
universal `MUST` that no failure justifies. The scope covers the default-branch
gate, branch lifecycle, and the release surface (package version, git tag, and
published registry artifact). It does not prescribe a hosting provider or a
specific CI vendor.

**Evidence and appraisal.** A first-party incident across four sibling
repositories on one date. The findings were: an expired evidence check alongside
merges performed with the default `GITHUB_TOKEN`, which do not trigger a workflow
run, so the default branch rotted while every visible pull request looked green;
a deleted upstream repository turning a soft link into a definite `404` that
failed a non-waivable hard check; an evidence-freshness window shorter than the
scheduled job's cadence, so the gate went red periodically with no code change; a
required status check name that matched no job in the workflow matrix, so every
pull request was blocked by a check that could never report; a duplicated lineage
whose trees were byte-identical, making a reset safe but making a naive
"diverged, therefore unsafe" reading permanently stuck; and a release surface
where the published package version and the source's declared version disagreed
with nothing reconciling them. The full narrative, including the behavioural
failures and the options considered, is recorded in
`docs/research/incident-reports/2026-10-17-fleet-ci-rot-and-agent-drift.md`.

Git documents `status`, `branch`, `log`, `fetch`, and `merge-base` as the
read-only facts a merge or delete decision rests on. GitHub documents branch
protection — which verifies a pull request rather than the default branch over
time — and the token-originated event that does not start a workflow run. Those
sources establish the objective facts locally, so the gaps are checkable rather
than a matter of judgment.

**Finding.** Three gaps are machine-observable and belong in a gating check: a
required check name that resolves to no job in any workflow; an evidence
freshness window that does not exceed the schedule cadence; and a publish
workflow whose package version, git tag, and registry version disagree. Two
further obligations are not machine-checkable and therefore stay advisory: a
state-changing git action should first read the target repository's own document
chain and the read-only git facts (working-tree status, all branches with their
tips, pruned fetch, recent history, and an ancestry or tree comparison), and a
scheduled job should be able to run the full gate on the default branch regardless
of how a commit arrived. The advisory half is what the incident shows a purely
advisory standard cannot compel; it is recorded here as evidence, not adopted as
a universal control.

**Limitations and recheck.** This is a single-fleet, first-party observation, not
a survey. The checks detect declared drift — a name that resolves to nothing, a
window shorter than a cadence, a version that disagrees with its artifact — and
cannot judge intent or whether a repository deliberately diverges. Recheck when
GitHub changes branch-protection or merge semantics, when the check blocks a
conforming repository, or when a second fleet-wide incident exposes a failure
mode these assertions do not reach.

Sources: https://git-scm.com/docs/git-status ,
https://git-scm.com/docs/git-branch ,
https://git-scm.com/docs/git-log ,
https://git-scm.com/docs/git-fetch ,
https://git-scm.com/docs/git-merge-base ,
https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication ,
https://docs.github.com/en/actions/reference/events-that-trigger-workflows ,
https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
