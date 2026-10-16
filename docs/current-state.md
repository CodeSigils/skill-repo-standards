# Current state

This document is **mutable**: it owns what is true *now*. Every claim carries a
check date. It is the opposite of `docs/research/index.md`, which is append-only
and never retro-edited.

Last reviewed: 2026-10-16.

## What this repository is

- A specification (`STANDARD.md`) plus a bundled reference validator
  (`scripts/standards_check.py`), published under the MIT license.
  (checked 2026-10-15)
- Not a skill: it ships no runtime payload, declares no `skills/` directory, and
  is not consumed through agent skill discovery. (checked 2026-10-15)

## What the standard currently covers

- Grade A "spine": one payload directory or a set of skill directories; `SKILL.md`
  frontmatter of exactly `name` and `description`; one validation entrypoint with
  `--self-test`; `README.md` and `SECURITY.md`; a `what:`/`why:` commit contract;
  SHA-pinned least-privilege automation. (checked 2026-10-15)
- CI enforces the commit contract across every non-merge commit introduced by a
  pull request targeting `main` or a push to `main`, rather than only testing
  the checker itself. Dependabot's generated commits remain the recorded D19
  exception. (checked 2026-10-16)
- Grade B "anti-rot core": a mutable current-state document split from an
  append-only research record; an immutable decision log; a machine-readable
  evidence index with verified dates; the research-once protocol; the
  canonical-owner rule. (checked 2026-10-15)
- One owner of truth per audience: `docs/current-state.md` owns what is true
  about this repository, and the runtime payload owns what an installed skill
  does; a payload is kept from linking into `docs/`. (checked 2026-10-15)
- [`docs/MAINTENANCE.md`](MAINTENANCE.md) owns the repository-only release
  runbook. Each normative standard version is published as an annotated Git tag
  and GitHub release after the documented checks pass; draft versions are
  prereleases, and ordinary maintenance commits are not tagged. (checked
  2026-10-16)
- A change lifecycle (research → finding → decision → implementation → check)
  whose recognised research-to-decision edge is machine-enforced: every
  recognised research body cites registered evidence, every decision has an
  unambiguous ID, and every decision is enabled by a research entry when both
  records are parseable. (checked 2026-10-15)
- Cross-surface consistency: a script a hook or workflow executes but the README
  verification block does not document is reported as an advisory note, which
  detects the drift a shared manifest would prevent without adopting one.
  (checked 2026-10-15)
- Normative language: `MUST`/`MUST NOT`/`SHOULD`/`MAY` are defined, `STANDARD.md`
  is the only normative document, and a conformance claim is an assertion until a
  passing check evidences it. (checked 2026-10-15)
- A standard lifecycle: status moves draft → stable → deprecated → superseded,
  changes are classified as editorial, compatible, or breaking with matching
  version bumps, and the standard and its evidence are reviewed at least twice a
  year with the review date recorded here. (checked 2026-10-15)
- An accepted-findings pattern for carrying a known validator finding without
  disabling the check: a baseline that never waives and an exception that expires.
  (checked 2026-10-15)
- A deliberately wide reading of the accepted shapes: a multi-skill payload, a
  decision log under any common ADR heading, and a research register or decision
  log in an unrecognised shape are advisory notes, not failures; a substantive
  breach stays hard. A survey of twelve sibling repositories found eleven adopt
  cleanly or with advisory notes, leaving one genuine gap (a minimal repository
  with no `SECURITY.md`). (checked 2026-10-15)
- One control adopted against a named failure mode: a `github-actions` Dependabot
  entry. Actions are pinned to full commit SHAs, and a SHA never rots on its own,
  so nothing would report a stale pin. Weekly, grouped (minor and patch), capped at
  two open pull requests, no auto-merge, and a major bump of a pinned action is
  ignored so it is taken deliberately rather than as routine. `uv` and Python
  dependencies are declined: this repository has none. (checked 2026-10-15)
- A conformance corpus, checked in under `conformance/`: fixture repositories in
  known shapes with an expected-results manifest and a runner
  (`scripts/check_conformance.py`) that re-runs the validator against each and
  compares the exit code and the hard and soft finding sets. The runner also
  computes its own coverage: every check the validator defines must be reached
  by at least one fixture and must return a finding some fixture records, so the
  corpus's coverage promise is a failing command rather than a sentence, and a
  regression in any check fails the corpus instead of passing silently. It makes
  a grade checkable rather than asserted, and its fixtures render date tokens at
  run time so a checked-in fixture cannot rot past the freshness window.
  (checked 2026-10-16)
- Grade C: controls a repository has individually justified against a named
  failure mode. (checked 2026-10-15)
- A standalone research consultation guide maps recurring concerns to the
  evidence registry and the records that support each decision; it can be used
  without a personal lab or any other repository, and is linked from both the
  human README and agent instructions. Behaviour-changing choices record scope,
  applicability, limitations, and a recheck trigger; material multi-option
  choices also record alternatives and consequences. (checked 2026-10-15)
- An opt-in evidence-appraisal profile adds context, human appraisal, outcome
  check, and minimum source sufficiency to a new behaviour-changing decision.
  Its declared shape and official-source requirement are validator-enforced; a
  Grade C trade-study template is available only for material multi-option
  choices. (checked 2026-10-15)
- The standalone consultation guide now routes every registered concern domain,
  including automation, validation, lifecycle, discovery, and documentation
  drift. It separately identifies runtime compatibility and distributed-skill
  trust: executable support and host approvals are not established by a portable
  `SKILL.md` format alone. This is a research boundary, not a new universal
  control. (checked 2026-10-16)
- The consultation guide owns a seven-step evidence-first workflow. A coverage
  review now audits the map, registry, and recent decisions before targeted
  official web research; a concern alone does not justify a control. The README
  and agent instructions link to this owner. (checked 2026-10-16)
- The reference validator enforces consultation coverage: when a repository
  keeps `docs/research/consulting.md`, its concern map must route every
  `domain_tag` declared in the evidence index. A registered domain with no route
  is a failure and an unreachable map tag is advisory, so the demonstrated
  map-versus-registry drift is a checked failure rather than prose alone.
  (checked 2026-10-16)
- The change lifecycle's implementation step names the full artifact set a
  machine-checkable change must ship: the validator update and its `--self-test`,
  the `conformance/` fixture and its `expected.json` entry, the README layout
  entry for any new file, the current-state update, and the version bump.
  (checked 2026-10-16)
- `AGENTS.md` owns a cold-boot directive for maintainer agents: the read order
  (normative rules before the README, the consultation guide, the conformance
  claim last), a working-tree and CI pre-flight, running the deterministic gates
  before starting, naming the target file and its owning rule, and a pre-handoff
  status report that makes staged, modified, and untracked work explicit. It is
  instance guidance, not a rule of the standard, so no version is bumped.
  (checked 2026-10-16)
- The standard lifecycle requires each version-changing commit to represent one
  released version. The historical 2.3 migration remains in place but states
  that it shipped with 2.4, preserving an honest record without rewriting shared
  history. (checked 2026-10-16)

## What is next

Committed-but-unbuilt work, in the order it is worth doing:
- Trial the evidence-appraisal profile in one additional Grade B repository and
  record whether it improves review. Only then decide whether its field
  presence should become universal rather than opt-in. (checked 2026-10-15)
- Use the Grade C trade-study template on the first material multi-option
  repository decision; add weights, a matrix, sensitivity analysis, evidence
  hierarchy, or recommendation-strength labels only if that trial exposes a
  failure the current template cannot prevent. (checked 2026-10-15)
- Decide whether the verification-command list should be sourced from one place
  across the README, the hooks, and CI. Cross-surface drift is now **detected**
  (the validator reports a command the executed surfaces run but the README does
  not document; see `docs/decisions.md` D18), but the list is still duplicated. A
  shared stage manifest stays deferred per `STANDARD.md` §Deferred controls until
  a verification command is actually observed to drop from one surface. See
  `docs/decisions.md` D16. (checked 2026-10-15)

## What is deliberately deferred

- Control-justification ledger, a scored claim-evidence matrix, shared stage
  manifest, git-history freshness (a `verifiedCommit`-style field), scheduled
  freshness or URL monitors, mandatory cross-repository adoption, and any hosted
  or MCP-backed memory service. Source provenance and research linkage are
  enforced; universal scoring evidence quality, trade-study weights, an evidence
  hierarchy, and recommendation-strength labels remain human review until a
  repository exhibits a failure that a mechanical rubric can prevent.
  (checked 2026-10-15)

## Known limits

- The validator detects drift in machine-checkable fields; it cannot judge
  whether a sentence in a decision is true. (checked 2026-10-15)
- The live external-reference check requires network access and is therefore
  excluded from the default deterministic suite. (checked 2026-10-15)
