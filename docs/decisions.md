# Decision log

Immutable decisions in the architecture-decision-record model. An entry is never
rewritten to match present reality; when a decision changes, add a new entry and
mark the old one superseded.

Each entry carries a stable `ID` (`D1`, `D2`, ...). The ID is how a research
entry in `docs/research/index.md` points at the decision it enables.

Every source URL here must be registered in `docs/evidence-urls.json`, which
`scripts/verify_urls.py` checks. `scripts/standards_check.py` rejects an entry
with a missing or malformed ID, a missing field, an unknown status, a malformed
date, or an unregistered source, and rejects a decision that no research entry
enables.

Allowed statuses: `proposed`, `accepted`, `deprecated`, `superseded`, `rejected`.

## Decision: The standard is a specification plus a bundled validator

- ID: D1
- Status: accepted
- Decided: 2026-10-15
- Sources: https://agentskills.io/specification
- Recheck: if the agentskills specification changes its own architecture

Rationale: The agentskills project pairs a canonical specification document with
a reference validator rather than distributing prose alone. A standard that
cannot be executed is advice; a bundled validator makes the machine-checkable
part falsifiable. This repository follows that shape: `STANDARD.md` is the norm
and `scripts/standards_check.py` is the reference implementation.

## Decision: Decision records use the immutable ADR model

- ID: D2
- Status: accepted
- Decided: 2026-10-15
- Sources: https://adr.github.io/madr/ , https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html , https://github.com/thomvaill/log4brains
- Recheck: if a superseding decision-log model becomes the documented norm

Rationale: The MADR template, AWS guidance, and the log4brains tooling agree that
a decision record is immutable after acceptance and is superseded rather than
rewritten. Rewriting a record to match present reality destroys the trail that
explains why a choice was made, which is the main failure mode this standard
exists to prevent. Each entry therefore records status, decision date, source
URLs, a recheck trigger, and a short rationale.

## Decision: Adopt the anti-rot core; defer external tooling

- ID: D3
- Status: accepted
- Decided: 2026-10-15
- Sources: https://artel.run/docs/documentation/ , https://datadef.io/guides/en/docs-checks-in-ci , https://docs.thally.io/guides/provenance , https://github.com/AgentMemoryWorld/Awesome-Agent-Memory
- Recheck: when drift on this repository's own records is observed

Rationale: Documentation rots because it hand-duplicates a source of truth;
derive what can be derived and watch what cannot. CI can check links, style, and
dates, but it cannot verify that a sentence is true. Freshness must never fail
open: an unverifiable claim is reported as unverified, not as fresh. Agent-memory
projects are catalogs of patterns, not drop-in tools. The anti-rot core in this
repository is therefore a short decision log, a machine-readable evidence index
with verified dates, a mutable current-state document split from an append-only
record, and a validator that checks them — with richer external tooling deferred
until drift is observed.

## Decision: Record and enforce the change lifecycle

- ID: D4
- Status: accepted
- Decided: 2026-10-15
- Sources: https://continuous-architecture.org/practices/fitness-functions , https://docs.thally.io/guides/provenance
- Recheck: if the research-to-decision edge is enforced by another mechanism

Rationale: The standard described the anti-rot records but not the process that
maintains them, so whether a change followed research → finding → decision →
implementation → check was left to memory. Fitness-function practice and
provenance guidance agree that an unstated process is not followed: a rule earns
its place only when a check fails without it. The lifecycle is therefore written
down in STANDARD.md, and its central edge — every decision is enabled by at least
one research entry — is enforced by scripts/standards_check.py.

## Decision: Adopt normative language and a conformance clause

- ID: D5
- Status: accepted
- Decided: 2026-10-15
- Sources: https://www.w3.org/TR/qaframe-spec/specgl-ics.html , https://opentide.org/docs/specifications/GOVERNANCE
- Recheck: if the requirement vocabulary changes (for example a successor to RFC 2119)

Rationale: A specification whose requirements read the same as its advice cannot
be conformed to or audited. The W3C QA guidance and the opentide governance
document both separate normative requirement keywords from informative prose and
expect the document to say which it is. STANDARD.md therefore defines MUST, MUST
NOT, SHOULD, and MAY, and states that it is the only normative document while the
other files are informative and link to it.

## Decision: Version the standard and change it by change class

- ID: D6
- Status: accepted
- Decided: 2026-10-15
- Sources: https://www.openmanuscript.org/docs/governance/specification-lifecycle , https://github.com/TIDES-transit/TIDES
- Recheck: if a specification-lifecycle standard supersedes this convention

Rationale: A shared quality floor that changes silently is worse than one that
does not change, because consumers cannot tell what they conform to. Established
specification projects classify a change as editorial, compatible, or breaking
and tie each to a version bump. STANDARD.md adopts that model: editorial changes
bump nothing, compatible clarifications and extensions bump the minor version,
and anything that makes a previously conforming repository non-conforming bumps
the major version and requires a migration note.

## Decision: Precedence resolves to STANDARD.md

- ID: D7
- Status: accepted
- Decided: 2026-10-15
- Sources: https://opentide.org/docs/specifications/GOVERNANCE
- Recheck: if the norm is split across more than one document

Rationale: When two documents disagree, a reader needs a rule that resolves the
conflict without a debate. opentide's governance states that its specification
wins on conflict, and the same is needed here. STANDARD.md is the single
normative document; every other file is informative and links to it rather than
restating a rule, so a disagreement is always a bug in the informative file.

## Decision: Accepted findings use a baseline and an exception file

- ID: D8
- Status: accepted
- Decided: 2026-10-15
- Sources: https://continuous-architecture.org/practices/fitness-functions , https://docs.thally.io/guides/provenance
- Recheck: when a validator in this repository reports findings the maintainer chooses not to fix

Rationale: A check that is turned off to silence a known finding stops guarding
anything. Fitness-function practice separates an observed baseline from a
time-bound waiver, and provenance guidance insists that an unverifiable result is
never reported as resolved. STANDARD.md therefore defines a baseline as a dated
snapshot that never waives a finding, an exception as the only waiver and one
that expires, and resolution as requiring the run that would have shown the
finding to complete. Adopting the files is a Grade C control, kept until a
validator actually reports findings the maintainer chooses not to fix.

## Decision: Defer a separate specification licence

- ID: D9
- Status: accepted
- Decided: 2026-10-15
- Sources: https://www.linuxfoundation.org/licensebestpractices
- Recheck: when the standard is published for external adoption

Rationale: The Linux Foundation's licensing guidance distinguishes a source-code
licence from a documentation or specification licence, and a specification
shipped for others to implement often needs its own. This repository is not yet
published for external adoption: it is a local specification with a bundled
validator. Splitting the licence — for example a specification licence for the
prose and a permissive code licence for the validator — is deferred until the
standard is actually published, at which point the single MIT licence becomes a
footgun worth fixing.

## Decision: Do not keep a CHANGELOG

- ID: D10
- Status: accepted
- Decided: 2026-10-15
- Sources: https://github.com/TIDES-transit/TIDES
- Recheck: if a consuming project requires a changelog file

Rationale: Many specification projects keep a CHANGELOG.md, and TIDES requires
one as part of its release checklist. This standard forbids one by design: a
hand-maintained changelog duplicates git history, and the duplicated copy is the
one that rots. The change record here is the git history itself, the immutable
entries in docs/decisions.md, and the dated statements in docs/current-state.md.
The divergence from the specification-project norm is deliberate and recorded, so
a future reader does not treat the absence as an oversight.

## Decision: Review the standard at least twice a year

- ID: D11
- Status: accepted
- Decided: 2026-10-15
- Sources: https://www.openmanuscript.org/docs/governance/specification-lifecycle
- Recheck: if the review cadence is enforced by another mechanism

Rationale: A standard and its evidence are claims about a moving world, and an
unreviewed claim is how rot starts. The Open Manuscript Initiative lifecycle
expects a declared last substantive update and a review trigger. This repository
records the review date in docs/current-state.md, checks it for staleness in the
validator, and commits to reviewing the standard, its deferred controls, and
every registered evidence source at least twice a year.

## Decision: Grade validator findings by severity

- ID: D12
- Status: superseded
- Decided: 2026-10-15
- Sources: https://continuous-architecture.org/practices/fitness-functions , https://docs.thally.io/guides/provenance
- Recheck: if every adopting repository keeps a research ledger, so the two soft rules could become hard

Rationale: A standard that only ever fails cannot be adopted by a repository that
is deliberately different. Dogfooding revealed that the reference implementation
(python-project-workflow) has no research ledger by design, so the research-to-
decision edge and the decision identifier cannot be hard rules for it. A check
with two severities — a hard finding that fails the run, and a soft finding that
is advisory and fails only under `--strict` — lets a repository adopt the
standard, see the gap, and record it rather than be blocked by it. Fitness-
function practice keeps a finding visible without disabling the check, and
provenance guidance keeps an open gap reported rather than hidden. The two rules
downgraded here are the research-to-decision edge and the decision identifier;
every structural, schema, date, and boundary finding stays hard. The recognised-
record evidence and research-to-decision requirements are superseded by D23;
absent or unrecognised research records remain advisory.

## Decision: Accept the common shapes of the decision log and the research register

- ID: D13
- Status: accepted
- Decided: 2026-10-15
- Sources: https://agentskills.io/specification , https://continuous-architecture.org/practices/fitness-functions
- Recheck: if every adopting repository converges on one decision-log and research-register shape

Rationale: A survey of twelve repositories showed that the validator recognised
exactly one shape of each practice and failed correct repositories that used
another. The multi-skill payload is a documented archetype, yet the spine
demanded a single skill directory. A decision log headed `## ADR-0001`, and a
research register that is a dated record rather than an `R-###` table, are the
same practices in a different shape. The fix is to widen what satisfies the
requirement, not to weaken it: the spine accepts one skill directory or a set of
skill directories each named for its skill with its own payload boundary, the
decision-log heading accepts the common ADR forms, and an unrecognised shape is
reported as an advisory note rather than a failure. The substantive checks — a
recognised entry with a status, a date, a registered source, and a rationale —
stay hard. This is the fitness-function rule applied to the standard itself:
keep the check, widen the accepted evidence.

## Decision: Publish the standard as a public repository

- ID: D14
- Status: accepted
- Decided: 2026-10-15
- Sources: https://agentskills.io/specification
- Recheck: if adoption is better served by distributing the standard inside an existing repository

Rationale: A standard that lives only on one machine is a personal synthesis;
its generality can be tested only where another person can adopt it. Publishing
gives the standard the stable URL, the public conformance claim, and the shared
history the anti-rot core assumes, and it matches how the format it builds on is
distributed — a canonical document plus a bundled validator in a public
repository. Detection stays local; publication only widens who can run it.

## Decision: Name the owner of truth for the repository and for the payload

- ID: D15
- Status: accepted
- Decided: 2026-10-15
- Sources: https://artel.run/docs/documentation/ , https://agentskills.io/specification
- Recheck: if the payload boundary is dropped, or the standard gains a runtime document

Rationale: A record rots when it hand-duplicates a source of truth, and a skill is
copied into a host where the authoring repository's documents do not exist. Read
together, those two facts mean truth has two owners that must not cross: the
mutable current-state document owns what is true about the repository, and the
runtime payload owns what an installed skill does, so a payload does not link into
`docs/`. Before this entry the split was implied by the payload-boundary check but
never stated, which left "one owner of truth" open to the reading that a skill
should point at the repository's documents. The rule is now explicit and its owner
is `STANDARD.md` §The anti-rot core.

## Decision: Record the duplicated verification-command list and keep the manifest deferred

- ID: D16
- Status: accepted
- Decided: 2026-10-15
- Sources: https://continuous-architecture.org/practices/fitness-functions
- Recheck: when a verification command is observed to drop from one surface and a gate stops running

Rationale: The verification commands appear in the README, the reference-validator
section of `STANDARD.md`, the git hooks, and the CI workflow. A sibling repository
collapsed the same duplication by sourcing the list from one module and asserting
that CI contains it, but this standard already defers "a shared stage manifest
spanning more than two surfaces", and the proportionality rule forbids adopting a
control before its failure mode is observed. The failure mode — a verification
command silently dropped from one surface — has not been observed. The
proportionate response is therefore to record the duplication in
`docs/current-state.md` §What is next and keep the control deferred, so the gap is
visible rather than rediscovered.

## Decision: Explain the standard and publish a next-steps list

- ID: D17
- Status: accepted
- Decided: 2026-10-15
- Sources: https://agents.md/ , https://llmstxt.org/
- Recheck: if the README framing begins to duplicate `STANDARD.md`

Rationale: A reader who arrives at the repository learns what it is but not why it
exists beside ADR practice, fitness functions, freshness tooling, and the
agent-discovery formats; both the agent-instruction and the discovery conventions
expect a front door that orients a human or an agent. Separately, committed-but-
unbuilt work needs one discoverable place for both audiences, and a second
forward-looking document would be another rot surface. The explanation therefore
lives in the README, and the next steps live as `## What is next` in the mutable
current-state document, which already owns "now".

## Decision: Detect cross-surface drift and stop masking a definite HTTP status

- ID: D18
- Status: accepted
- Decided: 2026-10-15
- Sources: https://continuous-architecture.org/practices/fitness-functions
- Recheck: if the verification-command list is sourced from one place, or a shared manifest stops being deferred

Rationale: A review found the same class of gap the standard exists to prevent. A
script a hook or workflow executes could be absent from the README verification
block with nothing to notice it, so the review added a soft cross-surface check
(`check_consistency`) that reports a command the executed surfaces run but the
README does not document — detection without introducing the deferred shared
manifest. Separately, the URL verifier caught `urllib.error.HTTPError` (a
`URLError` subclass) with its transport-failure handler, so a source returning a
new status such as 404 was reported as an environmental could-not-run (exit 2)
instead of drift (exit 1), and a malformed manifest printed failures yet exited 0.
A check must fail on the condition it names and must not soften a definite finding
into "could not check"; both are now fixed.

## Decision: Adopt a github-actions Dependabot entry and decline uv

- ID: D19
- Status: accepted
- Decided: 2026-10-15
- Sources: https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference , https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/optimizing-pr-creation-version-updates , https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-on-actions , https://github.com/CodeSigils/repo-architecture-skill
- Recheck: if a second ecosystem gains a dependency, or Dependabot stops rewriting SHA pins

Rationale: Actions are pinned to full commit SHAs, and a SHA never rots on its own
— nothing warns that the tag moved — so the repository already has the failure mode
Dependabot closes. The entry is `github-actions` only, weekly, grouped minor and
patch, capped at two open pull requests, with auto-merge of every kind disabled and
a major bump of a pinned action ignored so it is taken deliberately. The shape and
its reasoning are taken from the fleet note
`repo-architecture-skill/docs/research/automation-bots-and-workflows.md`, which is
cited as a source rather than re-derived. `uv` and Python dependencies are
declined, not deferred: this repository has zero third-party dependencies and three
stdlib-only scripts, so a package manager, lockfile, linter, type checker, their
pre-commit wiring, a second SHA-pinned Action in CI, and a weekly stream of
tooling pull requests would all be cost with nothing to act on. `cooldown` is
deliberately not configured — a three-day cooldown already applies by default, so
adding the knob would be a control with no failure mode. One consequence is
recorded rather than hidden: Dependabot commits do not follow this repository's
commit contract, and the local `commit-msg` hook cannot enforce anything on a bot,
so a merged Dependabot commit is an accepted exception.

## Decision: Back a grade claim with a checked-in conformance corpus

- ID: D20
- Status: accepted
- Decided: 2026-10-15
- Sources: https://hushspec.org/docs/conformance-statement , https://axlspec.org/conformance , https://www.w3.org/TR/qaframe-spec/specgl-ics.html
- Recheck: if the validator stops reporting findings as a flat hard/soft set, or the corpus stops matching its expected results on a routine change

Rationale: the standard says a claim is an assertion until a passing check
evidences it, but the only check behind a grade was `--self-test`, which builds
fixtures in a temporary directory and deletes them. Nothing a reader could
reproduce established that the validator behaves correctly on a repository like
theirs. The corpus makes the claim checkable: fixture repositories in known
shapes, an expected-results manifest, and `scripts/check_conformance.py`, which
re-runs the validator against each fixture and compares the exit code and the
hard and soft finding sets. Published conformance practice agrees that a
statement without a report is not evidence, and grades from self-attested
through verified. Two design choices are deliberate: the corpus asserts findings
and the exit code rather than a grade letter, because the validator does not
compute a grade and inventing one here would put a second, weaker truth next to
the validator's; and fixtures carry `{{TODAY}}`/`{{STALE}}` tokens rendered at
run time, so a checked-in fixture cannot rot into failure once it ages past the
freshness window. The corpus makes a grade checkable, not true — it verifies the
validator, not a repository's prose, which stays with human review.

## Decision: Cover every validator check with a corpus fixture

- ID: D21
- Status: accepted
- Decided: 2026-10-15
- Sources: https://hushspec.org/docs/conformance-statement , https://www.w3.org/TR/qaframe-spec/specgl-ics.html
- Recheck: if the validator gains a check no fixture exercises, or a fixture stops
  representing a shape the standard accepts

Rationale: an inspection of the first corpus found it exercised four of the
validator's seven checks. `check_standard`, `check_payload_boundary`, and
`check_consistency` had no fixture, so a regression in any of them would have
passed the corpus in silence while the standard's claim that the fixtures
reproduce the validator's behaviour stayed formally true. Five fixtures now cover
them and two further uncovered branches (a skill whose frontmatter name does not
match its directory; an evidence index that is malformed rather than merely
stale). The standard's own thesis is that a claim without a passing check is an
assertion, and a corpus that checks part of the validator while implying it
checks all of it is the same gap at one remove. Coverage is stated in
`STANDARD.md` rather than left to be inferred from the fixture list, so a future
check that arrives without a fixture is a visible omission. The validators'
per-branch edge cases — a duplicate research id, an `Enables` target that names no
decision, a duplicate decision id — remain asserted by the validator's own
`--self-test`, which is the cheaper place for a single-line mutation.

## Decision: Ship a standalone concern-oriented research consultation guide

- ID: D22
- Status: accepted
- Decided: 2026-10-15
- Sources: https://ebse.webspace.durham.ac.uk/ , https://www.gov.uk/government/publications/evidence-led-assurance-for-the-software-development-lifecycle , https://adr.github.io/madr/ , https://docs.github.com/en/get-started/git-basics/ignoring-files , https://docs.github.com/en/enterprise-cloud%40latest/repositories/creating-and-managing-repositories/best-practices-for-repositories , https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention/push-protection-on-the-command-line , https://github.com/github/gitignore
- Recheck: if a primary source changes, another recurring concern is added, or the consultation guide becomes a competing source registry

Rationale: recurring concerns, such as secrets, `.gitignore`, and repository
security, were being researched repeatedly because existing decision and source
records were correct but not discoverable by concern. Evidence-Based Software
Engineering, GOV.UK assurance guidance, and ADR practice support a sequence in
which authoritative evidence informs a recorded decision. The repository
therefore ships `docs/research/consulting.md`: a small, standalone map from a
concern to the existing decision log, evidence registry, and research record.
The guide contains no duplicate evidence inventory and makes no claim that a
personal lab is required, so the standard remains independently adoptable.

## Decision: Enforce recognised research evidence and decision traceability

- ID: D23
- Status: accepted
- Decided: 2026-10-15
- Sources: https://ebse.webspace.durham.ac.uk/ , https://www.gov.uk/government/publications/evidence-led-assurance-for-the-software-development-lifecycle , https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html , https://ops.fhwa.dot.gov/seits/sections/section3/3_4_5.html
- Recheck: if a recognised ledger shape gains an evidence field that is more reliable than its body, or a repository failure justifies a mechanical appraisal rubric

Rationale: Evidence-first guidance agrees that a decision needs a scoped
question, authoritative evidence, appraisal, and an accountable record. The
existing research record already carries sources and a verification date, while
the decision record carries a status, rationale, and recheck trigger; the gap
was that a parseable record could cite no evidence, duplicate a decision ID, or
leave a decision unenabled without failing validation. Those are objective
traceability failures, so the validator now rejects them when both records use
recognised shapes. This supersedes D12 only for recognised records: a repository
without a ledger, or with a legitimate unrecognised shape, remains adoptable and
receives an advisory finding. For a material multi-option decision, the
consultation guide requires alternatives and consequences in the rationale;
scoring evidence quality or trade-study weights stays human review because the
validator cannot determine their truth and no observed failure justifies a
mechanical rubric.

## Decision: Add an evidence-appraisal profile and scoped trade-study template

- ID: D24
- Status: accepted
- Decided: 2026-10-15
- Sources: https://ebse.webspace.durham.ac.uk/ , https://doi.org/10.1109/TSE.2025.3526730 , https://doi.org/10.1016/j.infsof.2021.106555 , https://www.gov.uk/government/publications/evidence-led-assurance-for-the-software-development-lifecycle , https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html , https://ops.fhwa.dot.gov/seits/sections/section3/3_4_5.html
- Recheck: after one additional Grade B adopter has used the profile, or when a material multi-option decision demonstrates a need for weighted scoring or evidence-strength labels
- Context: whether the next improvement should enforce a universal evidence score, or record a compact human appraisal with provenance
- Evidence appraisal: EBSE and credible-evidence guidance support explicit validity, impact, applicability, and fit-for-purpose reasoning; AWS and FHWA support context, consequences, alternatives, and outcome validation. Automated field checks can establish provenance but cannot establish the truth of that reasoning.
- Outcome check: review a real adopter's profile for completeness and usability before deciding whether its field-presence rule becomes universal; run the profile corpus fixture on every validator change.
- Evidence profile: primary

Rationale: the standard already records sources, rationale, and recheck triggers,
but did not distinguish primary-source sufficiency from a generic URL or make an
outcome check explicit. The new profile adds those fields for a new
behaviour-changing decision and hard-validates its declared shape. `primary`
requires a registered official source, while `constrained` requires a recorded
exception. The existing records remain immutable and are not retrofitted with
invented appraisals. The Grade C trade-study template covers material choices
without requiring weights, scoring, sensitivity analysis, an evidence hierarchy,
or recommendation-strength labels where no observed failure justifies them.

## Decision: Expand consultation coverage and distinguish distributed-skill trust

- ID: D25
- Status: accepted
- Decided: 2026-10-16
- Sources: https://agentskills.io/specification , https://code.claude.com/docs/en/skills
- Recheck: when a runtime-specific safety or compatibility claim is proposed, or the concern map no longer covers every evidence-registry domain
- Context: whether the concern-oriented consultation guide makes the records already held by this repository discoverable, and whether repository security alone covers executable distributed skills
- Evidence appraisal: The existing registry contains sources for more recurring concerns than the four-row guide exposed. The Agent Skills format permits executable support and compatibility declarations, while Claude Code adds runtime-specific invocation, dynamic-context, permission, and workspace-trust behavior. These sources establish a research boundary, not one portable safety policy.
- Outcome check: every registered domain tag has a route in the consultation guide; a future runtime-claim or executable-support decision starts at the new concern rather than inferring safety or compatibility from the common format
- Evidence profile: primary

Rationale: The guide existed to prevent repeated research, but its narrow map
hid recorded evidence for automation, validation, lifecycle, discovery, and
documentation drift. Those routes now point to the existing research and
decisions without copying the source registry. A separate runtime-compatibility
and distributed-skill-trust concern closes a material conceptual gap: secrets
and repository security protect the source repository, whereas executable
support, adapters, installation, and host approvals affect the artifact after
distribution. The standard does not make compatibility testing or an executable
audit universal because neither has a universal failure mode. A repository that
makes such a claim or ships such support can research and justify the narrow
control it needs.

## Decision: Treat coverage reviews as evidence-first triggers

- ID: D26
- Status: accepted
- Decided: 2026-10-16
- Sources: https://ebse.webspace.durham.ac.uk/ , https://www.gov.uk/government/publications/evidence-led-assurance-for-the-software-development-lifecycle
- Recheck: when a coverage review reveals a concern that cannot be reached through the map, current evidence, or recent decisions
- Context: whether a request to review research coverage should begin with broad web research or an audit of the repository's recorded evidence
- Evidence appraisal: EBSE and GOV.UK both support a sequence from an answerable question through relevant evidence to an accountable decision. The repository's concern map, registry, and decision log make that local audit possible; targeted official research is appropriate only when the audit demonstrates a gap.
- Outcome check: a coverage review can identify every registered source domain through the map, and a newly identified recurring concern produces a dated R finding before any control is proposed
- Evidence profile: primary

Rationale: A coverage review previously had no explicit trigger, so an agent
could either repeat web research that the repository had already recorded or
mistake a list of concerns for a mandate to add controls. The consultation guide
now classifies coverage review as a research-sensitive request, audits local
evidence first, and searches official guidance only for a demonstrated gap.
This preserves the evidence-first workflow while keeping the proportionality
rule intact: a concern warrants research when it is recurring and
decision-worthy, but warrants a control only when its failure mode is observed.

## Decision: Enforce consultation-map coverage of the evidence index

- ID: D27
- Status: accepted
- Decided: 2026-10-16
- Sources: https://www.gov.uk/government/publications/evidence-led-assurance-for-the-software-development-lifecycle
- Recheck: when the concern map changes shape, or a repository is found that keeps a guide the check cannot recognise
- Context: The consultation guide's concern map is prose, and nothing detected a map that routes fewer domains than the evidence index declares.
- Evidence appraisal: The demonstrated drift, a registry of fourteen domains reached by four routes, is a named failure mode; the fix is a narrow check over an existing record rather than a new control.
- Outcome check: The validator fails when a registered evidence domain has no route, and the corpus fixture proves the failure.
- Evidence profile: primary

Rationale: A concern map with fewer routes than the evidence index declares is
exactly the drift a coverage review is meant to catch, and prose alone did not
prevent it. The check binds only when the guide exists, so it is a compatible
extension, and a corpus fixture keeps it honest.

## Decision: Name the full artifact set in the change lifecycle

- ID: D28
- Status: accepted
- Decided: 2026-10-16
- Sources: https://www.gov.uk/government/publications/evidence-led-assurance-for-the-software-development-lifecycle
- Recheck: when a standard change is observed to ship without one of the named artifacts
- Context: Step 4 of the change lifecycle named only the validator and its self-test, so the conformance fixture, the version bump, and the paired records were implied rather than stated.
- Evidence appraisal: The lifecycle already requires implementation and check; the gap was that a machine-checkable change could satisfy the letter of step 4 while leaving the corpus unexercised. GOV.UK assurance guidance supports making the accountable artifacts explicit at the point of change rather than trusted to memory.
- Outcome check: A reader of step 4 can enumerate every artifact a machine-checkable change must ship, and the corpus's fixture promise is one of them.
- Evidence profile: primary

Rationale: The change lifecycle is the single owner of how this standard changes,
so its implementation step must name everything a change ships; otherwise a
maintainer who follows step 4 literally can add a check without the fixture that
proves it and the corpus still passes. This closes the gap identified in the
self-review of the consultation-coverage change, which stated the artifact set
only across several documents. Naming the set is a compatible extension of the
existing procedure — it adds no `MUST` on adopting repositories and makes no
conforming repository non-conforming — so it is a minor bump.

## Decision: Adopt a cold-boot directive for maintainer agents

- ID: D29
- Status: accepted
- Decided: 2026-10-16
- Sources: https://agents.md/ , https://llmstxt.org/
- Recheck: when the entry file, the read order, or a supported agent discovery surface changes
- Context: `AGENTS.md` had a read order but no pre-flight. An agent could start on a dirty tree, a diverged branch, or red CI, and could act on an incomplete picture because the read order omitted the consultation guide and the conformance claim.
- Evidence appraisal: The registered `agent-discoverability` sources establish a single discoverable entry file as the agent's starting point (R-004, R-027). The failure mode is starting from an entry that omits state, gates, and the research route; prose in the entry file is the proportionate control, because onboarding completeness is not machine-checkable.
- Outcome check: A maintainer agent following `AGENTS.md` reads the normative rules before the README, checks working-tree and CI state before working, runs the deterministic gates, and names the target file and its owning rule.
- Evidence profile: primary

Rationale: The repository's cold boot is a named concern with a concrete failure
mode — an agent that starts on an unreported dirty tree or acts from a partial
read order. Naming the order and the pre-flight in `AGENTS.md`, the single owner
of agent guidance, prevents it without a control that cannot be checked. This is
instance guidance, not a rule of the standard, so `STANDARD.md` is unchanged and
no version is bumped.

## Decision: Compute the corpus's coverage instead of asserting it

- ID: D30
- Status: accepted
- Decided: 2026-10-16
- Sources: https://www.w3.org/TR/test-methodology/ , https://www.w3.org/QA/WG/2003/10/TestGL-20031020.html , https://hushspec.org/docs/conformance-statement
- Recheck: when a validator check ships without a fixture and the audit stays silent, or when the audit produces a finding that a conforming corpus cannot clear
- Context: `STANDARD.md` and D21 assert that every check the validator performs is exercised by at least one fixture, but only prose asserted it. The same defect class — two machine-readable sides of a completeness claim that nothing reconciles — was demonstrated when the consultation concern map exposed fewer routes than the evidence index declared, and no sentence asserting completeness had prevented it.
- Evidence appraisal: R-018 considered and rejected a mechanism, judging five fixtures plus a sentence proportionate because the sentence would make an omission visible. That judgment rested on visibility being enough; the map-versus-registry drift shows a visible omission is not an enforced one. W3C guidance requires at least one test case per conformance requirement and requires coverage data to be calculated and published, so computing coverage is established practice rather than ceremony, and hushspec's rule that a statement without its report is an assertion still applies to the corpus's own claim.
- Outcome check: Deleting a call from `check_target`, or adding a check that no fixture drives to a finding, fails `python3 scripts/check_conformance.py` with the name of the uncovered check instead of passing silently, and `--self-test` covers the gap arithmetic itself.
- Evidence profile: primary

Rationale: The corpus exists so that the validator's behaviour is reproduced
rather than taken on trust, which makes an unverified coverage claim the same
defect one level up: the evidence for the validator outruns the check on the
evidence. The audit is deliberately a second pass inside `check_conformance.py`
rather than a rule in the adopter-facing validator, because no conformance grade
requires an adopter to ship a corpus. It changes no `MUST`, so `STANDARD.md` is
not required to change for the control itself; the standard's description of the
companion check is corrected so it no longer under-describes what ships.

## Decision: Use one released version per version-changing commit

- ID: D31
- Status: accepted
- Decided: 2026-10-16
- Sources: https://www.gov.uk/government/publications/evidence-led-assurance-for-the-software-development-lifecycle
- Recheck: when a version-changing commit again needs more than one migration heading, or a release workflow replaces commit-based releases
- Context: The 2.4 commit published both 2.3 and 2.4 migration notes, leaving no checkout that represents version 2.3.
- Evidence appraisal: The release remained coherent, but the change lifecycle already names the version bump as an accountable artifact. A one-version-per-commit rule makes the historical state inspectable without requiring a rewrite of shared history.
- Outcome check: Future version-changing commits have exactly one released version and matching migration note; the 2.3 note explicitly states that it shipped with 2.4.
- Evidence profile: primary

Rationale: Version numbers are release identifiers, not a list of independently
reviewable changes hidden inside one commit. The 2.3/2.4 jump was harmless to
runtime behavior but weakened reviewability. The forward rule belongs in the
standard lifecycle, which owns versioning; `AGENTS.md` links to it for maintainer
entry. The historical migration is clarified in place. Rewriting protected shared
history would create more risk than it removes.
