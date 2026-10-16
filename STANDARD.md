# Skill Repository Standard

**Version 2.2 (draft).** This document is the single normative source for the
shared quality floor described here. It is not project authority for any other
repository; read that repository directly.

When two documents in a repository disagree, `STANDARD.md` wins. Every other
file is informative and links here rather than restating a rule.

## Purpose and scope

This standard governs **agent-skill repositories**: repositories whose product is
one or more skills consumed by a coding agent through agentskills-style
discovery, maintained by an individual, and shipped by copying a directory.

It does not govern frameworks, applications, or services. It does not force a
single operating model: it defines a shared quality floor and grades of
conformance, and it expects a repository to adopt only the controls its own
failure modes justify.

## Normative language

`MUST`, `MUST NOT`, `SHOULD`, and `MAY` are used in the RFC 2119 sense:

- **MUST** — an absolute requirement of the grade that names it.
- **MUST NOT** — an absolute prohibition.
- **SHOULD** — a strong default; depart only with a recorded reason.
- **MAY** — genuinely optional.

Only this document is normative. `README.md`, `AGENTS.md`, `docs/decisions.md`,
`docs/current-state.md`, and the research record are informative; where one of
them states a rule it links to the owning section here instead of defining it.

## Conformance grades

Conformance is **additive** and **self-asserted**. A repository claims a grade;
lower grades are valid and intentional. A control is required only at the grade
that names it.

| Grade | Name | Requires |
| --- | --- | --- |
| A | Spine | Everything under *The common spine*. |
| B | Spine + anti-rot core | Grade A plus *The anti-rot core*. |
| C | Spine + anti-rot core + justified controls | Grade B plus controls the repository has individually justified. |

A claim is an assertion until it is evidenced. A repository that claims a grade
SHOULD be able to show a passing run of its own validation entrypoint (Grade A)
and, where it adopts them, of the standard's reference validator. For a durable
claim a repository MAY record it in a short `CONFORMANCE.md` naming the claimed
grade, the `STANDARD.md` version it was checked against, and the date of the
check. Where the reference corpus covers the claimed shape, a claim MAY cite the
matching fixture as its evidence, since a checked-in fixture is reproducible by
a reader while a self-check in a temporary directory is not. A claim with no
passing check is an assertion, not evidence.

## The common spine (Grade A)

1. **A canonical runtime payload.** The repository ships either one payload
   directory (for example `skills/<skill-name>/`) or a set of skill directories,
   each named for its skill and each with its own payload boundary. An installed
   copy on a user's machine is a **distribution artifact**, never a second
   source of truth.
2. **`SKILL.md` frontmatter carries exactly `name` and `description`.** `name`
   is kebab-case and equals its directory name. `description` states what the
   skill does and when it applies, in the third person, without XML tags.
   Detail beyond the trigger and the core procedure lives in `references/`
   files loaded on demand (progressive disclosure).
3. **Exactly one validation entrypoint.** It exits `0` on success and `1` on
   findings, and supports a `--self-test` mode that mutates inputs and asserts
   the checks reject bad input.
4. **A `README.md` and a `SECURITY.md`.**
5. **A commit contract.** The subject is `type[(scope)]: verb — rationale` and
   the body contains a `what:` line followed by a `why:` line. There is no
   `CHANGELOG.md`; git history is the change record.
6. **Pinned, least-privilege automation.** GitHub Actions are pinned to full
   40-character commit SHAs, every checkout sets `persist-credentials: false`,
   and each job declares the smallest `permissions` it needs.

   Pinning by SHA makes an Action immutable and also lets it go stale in silence,
   so a repository that pins has an update obligation: something must report that
   the tag moved. This is not a requirement and no grade depends on it — but the
   obligation exists whether or not it is met, and a repository that pins without
   meeting it should know that.

## The anti-rot core (Grade B)

Research and decisions rot. Grade B adds the machinery that keeps a written
record trustworthy and findable.

- **Current state versus append-only record.** A **mutable**
  `docs/current-state.md` owns what is true *now* and stamps every claim with a
  check date. A separate **append-only** `docs/research/index.md` is a dated
  record that is never retro-edited; new evidence is appended, and a superseded
  entry is marked superseded rather than rewritten.
- **A decision log** `docs/decisions.md`. Entries follow the immutable
  architecture-decision-record model: only the status transitions
  (proposed → accepted → deprecated → superseded → rejected); an old decision is
  never rewritten to match present reality, it is superseded by a new entry.
  Each entry records its status, the date it was decided, its external source
  URLs, a recheck trigger, and a short rationale.
- **A machine-readable evidence index** `docs/evidence-urls.json`. Every source
  cited by a decision is registered here with a `last_verified` date, so
  freshness is machine-legible rather than asserted in prose.
- **The research-once protocol.** Before performing new research, search the
  decision log, the evidence index, and the research record. Reuse an existing
  entry whose scope and freshness fit; revalidate volatile, version-sensitive,
  or decision-critical facts at the point of use; and record whether the result
  was reused, revalidated, superseded, or newly discovered. For a
  behaviour-changing choice, record the question and scope, source
  applicability, material limitations, and a recheck trigger in the research
  finding or decision. For a material multi-option choice, record the
  alternatives and consequences. Do not silently repeat a search.
- **Consultation coverage.** When a repository keeps a concern-oriented
  consultation guide at `docs/research/consulting.md`, its concern map MUST
  route every `domain_tag` declared in the evidence index, so each registered
  evidence domain is reachable from the guide. A registered domain with no route
  is a failure; a route with no registered domain is advisory, because it signals
  a dead route. A repository without the guide is unaffected.
- **Traceable research evidence.** A recognised `R-###` entry MUST have a body
  section with at least one source URL, and every source URL in that body MUST be
  registered in `docs/evidence-urls.json`. When both the research register and
  decision log are in recognised shapes, every declared decision ID MUST be
  enabled by at least one research entry. This preserves incremental adoption
  for repositories without a ledger while preventing a parseable ledger from
  silently losing its evidence trail.
- **Evidence-appraisal profile.** A behaviour-changing decision SHOULD use the
  structured profile in `docs/research/evidence-appraisal.md`: context,
  evidence appraisal, outcome check, and evidence profile. When a decision
  declares that profile, all four fields MUST be non-empty. Profile `primary`
  MUST cite at least one registered `official_docs` source; profile
  `constrained` MUST explain why a primary source was unavailable. The profile
  records a maintainer's appraisal; the validator checks its provenance and
  shape, not whether the judgment is true.
- **One owner of truth.** Truth has two owners, and they do not cross.
  `docs/current-state.md` owns what is true about the *repository* now; the
  runtime payload (`SKILL.md` and its `references/`) owns what an *installed*
  skill does. A payload link into `docs/` does not resolve once the skill is
  copied into a host, so a runtime rule belongs in the payload and a repository
  fact belongs in the current-state document. Every other file links to the
  owner rather than restating it.
- **The canonical-owner rule.** Every behavioural rule has exactly one owning
  file. Other files link to it instead of restating it. If two files assert the
  same rule, one of them is wrong.

## Standard lifecycle

This standard is versioned, and it changes under the same change lifecycle as
everything else: a change to it is a decision, not an edit in place.

- **Status.** `draft` until at least two repositories conform at Grade B, then
  `stable`; later `deprecated` (a successor exists) or `superseded`. A change to
  status is recorded in `docs/decisions.md`, not made by editing this line.
- **Version.** Bumped here and the change recorded in `docs/decisions.md`:
  - an editorial change (wording, typos) — no bump;
  - a compatible clarification or extension — a minor bump;
  - a new `MUST`, a removed or weakened `MUST`, or any change that makes a
    previously conforming repository non-conforming — a major bump with a
    migration note.
- **Review cadence.** This document, the deferred list, and every source in
  `docs/evidence-urls.json` are reviewed at least twice a year. The review date
  lives in `docs/current-state.md` and is enforced by the validator.

### 2.0 migration

Version 2.0 makes recognised research records stricter. For each `R-###` body,
add at least one registered source URL. When both records use the recognised
shapes, add an `Enables` link for every decision ID and remove duplicate decision
IDs. A repository without a recognised research register remains adoptable and
receives an advisory finding; it is not required to invent a ledger merely to
pass this standard.

### 2.1 migration

Version 2.1 adds a compatible evidence-appraisal profile for new
behaviour-changing decisions. Existing immutable records do not need to be
rewritten. A new record that opts into the profile must supply all its fields;
use `constrained` only with a primary-source exception. A material multi-option
decision MAY use the Grade C trade-study template before adopting any scoring
control.

### 2.2 migration

Version 2.2 makes the consultation guide's concern map checkable. When a
repository keeps `docs/research/consulting.md`, its concern map must route every
`domain_tag` declared in `docs/evidence-urls.json`. Add a row for any registered
domain the map omits, or drop a tag from the evidence index when the concern is
gone. A repository without the guide is unaffected, so no immutable record needs
to change.

## Change lifecycle

Every change to this standard — a rule, a check, or a record — follows the same
ordered loop. It is the concrete form of the research-once protocol, and it
applies to the standard itself as much as to any repository adopting it.

1. **Research.** Search `docs/decisions.md`, `docs/evidence-urls.json`, and
   `docs/research/index.md` before looking outward. Research only what is not
   already recorded.
2. **Finding.** Append a dated entry to `docs/research/index.md` (an `R-###`
   id) recording the concern, its status, the check date, and the sources.
3. **Decision.** If the finding changes behaviour, record it in
   `docs/decisions.md` (a `D` id) whose `Sources` are registered in
   `docs/evidence-urls.json`.
4. **Implementation.** Update `STANDARD.md` (it owns the rules); if the rule is
   machine-checkable, update `scripts/standards_check.py` and its `--self-test`
   in the same change.
5. **Check.** Run the verification commands in the README. A change is not done
   until the deterministic checks pass *and* the named pair of documents agree:
   `STANDARD.md` (the rules) and `docs/current-state.md` (what is true now) MUST
   describe the same reality, and `docs/decisions.md` MUST hold every choice the
   change made. Disagreement between the pair is documentation drift to resolve
   before the change is closed.

A research entry enables a decision; a decision is enabled by at least one
research entry. The validator enforces that every decision is enabled, that
every `R-###` id is unique, and that every `Enables` target names a decision
that exists — so the research-to-decision edge cannot silently rot.

## Proportionality rule

**Adopt a control only when its failure mode actually exists in this
repository.** A control with no observed, named failure mode is ceremony, and
ceremony is deleted rather than enforced. This rule is normative: it governs the
addition of every control, including those this standard names at Grade C.

## Accepted findings

A validator accumulates findings over time. Two mechanisms keep an accepted
finding visible without disabling the check, and they are not the same thing:

- **A baseline** is a dated snapshot of the findings a maintainer has seen. It
  records "as of this date a human looked"; it never waives a finding, it only
  stops re-reporting an already-seen one as new. A baseline MUST carry its
  review date.
- **An exception** is the only waiver. Each entry names the finding, a reason,
  and an expiry date. It applies to soft findings only, never to a hard one, and
  an expired exception is itself a finding. Exceptions are maintainer state:
  contributors do not edit them.

A finding is reported as **resolved** only when the run that would have shown it
completed successfully. A partial or failed run MUST NOT be read as a
resolution. Adopting a baseline or an exception file is a Grade C control: do it
only when a validator actually reports findings you choose not to fix.

## Local check contract

Every script under `scripts/` returns the same three codes:

- `0` — clean.
- `1` — findings.
- `2` — could not run.

A script must not exit `1` for an environmental problem (a missing tool, no
network, an unreadable temporary directory), because that would be reported as a
repository finding. Failures the tool cannot classify are reported as `2` and
explained.

## Deferred controls

The following are deliberately **not** part of Grade A or Grade B. Do not adopt
them until drift has been observed:

- a control-justification ledger,
- a claim-evidence matrix,
- a shared stage manifest spanning more than two surfaces,
- git-history freshness (for example a `verifiedCommit` field that marks a
  source stale when the file it documents changes since that commit),
- scheduled cron freshness or URL monitors,
- mandatory adoption across all repositories,
- any MCP-backed or hosted memory service.

## Grade C: material-decision trade studies

Use [`docs/research/trade-study.md`](docs/research/trade-study.md) only when a
decision has multiple viable alternatives and material cost, risk, or
irreversibility. The template records objectives, alternatives, criteria,
assessment, stakeholders, the selected option, and an outcome check. It does
not make weighted scoring or sensitivity analysis universal requirements; add
them only when the decision's failure mode warrants them.

## The reference validator

This repository ships `scripts/standards_check.py`. It checks only what is
machine-checkable and never judges prose. Every finding carries a severity: a
**hard** finding fails the run, and a **soft** finding is advisory and fails only
under `--strict`.

```bash
python3 scripts/standards_check.py            # check this repository
python3 scripts/standards_check.py TARGET     # check another repository
python3 scripts/standards_check.py TARGET --strict   # treat soft findings as failures
python3 scripts/standards_check.py --self-test
```

It verifies:

1. spine files (`README.md`, `SECURITY.md`; and if a `skills/` directory exists,
   every skill directory whose `SKILL.md` frontmatter `name` equals its
   directory name);
2. the decision schema — required fields, an allowed status, an ISO date for
   `Decided`, at least one source URL, a non-empty `Recheck`, and a rationale;
3. an opted-in evidence-appraisal profile — complete fields, a registered
   official source for `primary`, or an explicit exception for `constrained`;
4. evidence registration — every decision source URL is present in the evidence
   index;
5. freshness — every `last_verified` date parses and is within the maximum age;
6. evidence index hygiene — a `version` and a `description` are present;
7. the payload boundary — no file under `skills/` links outside its own skill
   directory;
8. the recognised research register — unique `R-###` ids, a parseable check
   date, a matching body section, at least one registered source URL, and
   `Enables` targets that name a declared decision;
9. the recognised research-to-decision edge — every decision is enabled by at
   least one research entry, and every declared decision ID is unique;
10. the standard's own document — a `**Version` marker, a `## Normative language`
   section, and a `## Standard lifecycle` section, when a `STANDARD.md` is
   present;
11. the review cadence — `docs/current-state.md` carries a parseable
    `Last reviewed:` date within the maximum age;
12. the cross-surface consistency of commands — a script a hook or workflow
    executes is documented in the README verification block;
13. consultation coverage — when `docs/research/consulting.md` exists, every
    `domain_tag` declared in the evidence index appears in its concern map (a
    registered domain with no route is hard; a route with no registered domain is
    soft).

The decision identifier is **soft**, so a repository can begin with an
unidentified decision log. An absent or unrecognised research register is also
advisory, preserving incremental adoption. The accepted shapes are deliberately
wide: a multi-skill payload, a decision log under any of the common ADR headings,
and a research register or decision log in a shape the validator does not
recognise are all reported as advisory notes rather than failures. Once both
records are recognised, however, a missing research source, duplicate decision
ID, or unenabled decision is a substantive breach and stays hard.

A companion check, `scripts/check_conformance.py`, runs the validator against
the checked-in fixtures under `conformance/` and compares each fixture's exit
code and finding set with `conformance/expected.json`. It verifies the
validator, not a repository: the fixtures exist so that a stated result can be
reproduced by a reader instead of taken on trust. Every check the validator
performs is exercised by at least one fixture, so a regression in any of them
appears as a corpus failure rather than as silence.

Detection is automated; **correction is not.** A recorded decision is a starting
point for the next reader, not proof.

## Conformance checklist

- [ ] **Grade A** — one payload directory or a set of skill directories;
      `SKILL.md` frontmatter is exactly `name` + `description`; one validation
      entrypoint with `--self-test`; `README.md` and `SECURITY.md`; the commit
      contract; SHA-pinned, least-privilege automation.
- [ ] **Grade B** — `docs/current-state.md` (mutable, dated) split from
      `docs/research/index.md` (append-only); `docs/decisions.md`; a registered
      `docs/evidence-urls.json`; the research-once protocol with a proportionate
      evidence appraisal; traceable recognised research evidence; one owner of
      truth; the canonical-owner rule; consultation coverage when a guide is
      present.
- [ ] **Grade C** — each additional control names the failure mode it prevents;
      a material multi-option decision may use the trade-study template.
