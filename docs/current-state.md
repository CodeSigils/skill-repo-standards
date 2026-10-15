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

- Grade A "spine": one canonical payload; `SKILL.md` frontmatter of exactly
  `name` and `description`; one validation entrypoint with `--self-test`;
  `README.md` and `SECURITY.md`; a `what:`/`why:` commit contract; SHA-pinned
  least-privilege automation. (checked 2026-10-15)
- Grade B "anti-rot core": a mutable current-state document split from an
  append-only research record; an immutable decision log; a machine-readable
  evidence index with verified dates; the research-once protocol; the
  canonical-owner rule. (checked 2026-10-15)
- A change lifecycle (research → finding → decision → implementation → check)
  whose research-to-decision edge is machine-enforced: every decision must be
  enabled by a research entry. (checked 2026-10-15)
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
- Grade C: controls a repository has individually justified against a named
  failure mode. (checked 2026-10-15)

## What is deliberately deferred

- Control-justification ledger, claim-evidence matrix, shared stage manifest,
  git-history freshness (a `verifiedCommit`-style field), scheduled freshness or
  URL monitors, mandatory cross-repository adoption, and any hosted or
  MCP-backed memory service. Each is deferred until drift is observed.
  (checked 2026-10-15)

## Known limits

- The validator detects drift in machine-checkable fields; it cannot judge
  whether a sentence in a decision is true. (checked 2026-10-15)
- The live external-reference check requires network access and is therefore
  excluded from the default deterministic suite. (checked 2026-10-15)
