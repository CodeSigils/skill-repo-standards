# Current state

This document is **mutable**: it owns what is true *now*. Every claim carries a
check date. It is the opposite of `docs/research/index.md`, which is append-only
and never retro-edited.

Last reviewed: 2026-10-15.

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
- Grade B "anti-rot core": a mutable current-state document split from an
  append-only research record; an immutable decision log; a machine-readable
  evidence index with verified dates; the research-once protocol; the
  canonical-owner rule. (checked 2026-10-15)
- One owner of truth per audience: `docs/current-state.md` owns what is true
  about this repository, and the runtime payload owns what an installed skill
  does; a payload is kept from linking into `docs/`. (checked 2026-10-15)
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
  compares the exit code and the hard and soft finding sets. Every check the
  validator performs is exercised by at least one fixture, so a regression in any
  of them fails the corpus instead of passing silently. It makes a grade checkable
  rather than asserted, and its fixtures render date tokens at run time so a
  checked-in fixture cannot rot past the freshness window. (checked 2026-10-15)
- Grade C: controls a repository has individually justified against a named
  failure mode. (checked 2026-10-15)
- A standalone research consultation guide maps recurring concerns to the
  evidence registry and the records that support each decision; it can be used
  without a personal lab or any other repository, and is linked from both the
  human README and agent instructions. Behaviour-changing choices record scope,
  applicability, limitations, and a recheck trigger; material multi-option
  choices also record alternatives and consequences. (checked 2026-10-15)

## What is next

Committed-but-unbuilt work, in the order it is worth doing:

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
  enforced; scoring evidence quality or trade-study weights remains human review
  until a repository exhibits a failure that a mechanical rubric can prevent.
  (checked 2026-10-15)

## Known limits

- The validator detects drift in machine-checkable fields; it cannot judge
  whether a sentence in a decision is true. (checked 2026-10-15)
- The live external-reference check requires network access and is therefore
  excluded from the default deterministic suite. (checked 2026-10-15)
