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
