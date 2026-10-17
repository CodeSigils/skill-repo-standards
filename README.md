# skill-repo-standards

A specification and a bundled validator for the shared quality floor of
agent-skill repositories, plus the anti-rot core that keeps a repository's
written decisions and research trustworthy.

This repository is **maintainer tooling**, not a skill. It ships no runtime
payload to agents. It contains one normative document, one reference validator,
and the seed records that dogfood the standard.

## What problem this solves

Agent-skill repositories independently rediscover the same best practices —
how to lay out a payload, how to keep decisions from silently rotting, how to
make a written record findable before it is re-derived for the hundredth time.
This repository writes the shared floor down once, in one place, and provides a
validator that enforces the machine-checkable parts of it.

## Why this standard, not just the five building blocks

The durable-context field has five well-established families: decision records
(MADR, AWS ADRs, log4brains), executable governance (fitness functions),
freshness and provenance, agent discoverability (AGENTS.md, llms.txt), and agent
memory. They are practice families and tools, not a product for the artifact
class *agent-skill repository*, and none is stdlib-portable to an ecosystem that
is shipped by copying a directory.

This repository is a thin, scoped adapter, not a rival synthesis. It consumes
those families — the sources are registered in `docs/evidence-urls.json` and the
adopt-versus-defer choice for each is recorded in `docs/decisions.md` — and adds
the one thing none of them ships: a validator for skill repositories.
`agentskills`' `skills-ref validate` covers the file format only. The shape here
is deliberately the same as the thing it builds on: a canonical document plus a
bundled validator, in a public repository, adoptable by copy.

It is honest about its own limits. A first sweep across twelve sibling
repositories exposed that the validator had hard-encoded one shape of each good
practice and failed correct repositories that used another; the fix was to widen
what satisfies the requirement, not to weaken it (see `docs/decisions.md` D13).
Detection is automated and correction is routed to review — the validator never
judges whether a sentence is true.

## The two layers

- **The standard** — [`STANDARD.md`](STANDARD.md). A graded specification
  (Grade A spine, Grade B anti-rot core, Grade C justified controls) with a
  normative proportionality rule: adopt a control only when its failure mode
  actually exists.
- **The validator** — [`scripts/standards_check.py`](scripts/standards_check.py).
  It checks every machine-checkable rule listed under
  [`STANDARD.md` §The reference validator](STANDARD.md). It detects drift; it
  never judges prose.

## Maintaining this repository

`STANDARD.md` describes what adopters implement; this repository's maintainer
routing is in [`AGENTS.md`](AGENTS.md). [`docs/MAINTENANCE.md`](docs/MAINTENANCE.md)
owns the repository-only release runbook; it links outward rather than restating
the standard. [`docs/decisions.md`](docs/decisions.md) is the immutable decision
log (ADR model): each entry records why a choice was made and is superseded
rather than rewritten.

Terms used throughout this repository — the normative keywords and the sense of
*finding* — are defined once in
[`STANDARD.md` §Normative language](STANDARD.md#normative-language).

## Use the validator

```bash
python3 scripts/standards_check.py            # check this repository
python3 scripts/standards_check.py TARGET     # check another repository
python3 scripts/standards_check.py --self-test
```

Exit codes follow the local check contract: `0` clean, `1` findings, `2` could
not run.

## Consult research before re-researching

This repository is standalone: research-sensitive work follows the canonical
[evidence-first workflow](docs/research/consulting.md#evidence-first-workflow).
It starts with the concern map, decision log, evidence registry, and append-only
research record before looking outward. When a user requests a coverage review,
first compare the map with the registry and recent decisions; search official
web guidance only for a recurring, decision-worthy gap with no current,
applicable evidence. Agents receive the same route from [`AGENTS.md`](AGENTS.md),
so a human and an agent consult one canonical process rather than separate
instructions.

For a new behaviour-changing decision, use the compact
[evidence-appraisal profile](docs/research/evidence-appraisal.md). For a
material multi-option choice only, use the optional Grade C
[trade-study template](docs/research/trade-study.md).

## Repository layout

```text
.
├── .githooks
│   ├── commit-msg
│   ├── pre-commit
│   └── pre-push
├── .github
│   ├── dependabot.yml
│   └── workflows
│       └── ci.yml
├── .gitignore
├── AGENTS.md
├── CONFORMANCE.md
├── LICENSE
├── README.md
├── SECURITY.md
├── STANDARD.md
├── conformance
│   ├── expected.json
│   └── fixtures
│       ├── advisory-shapes
│       │   ├── README.md
│       │   ├── SECURITY.md
│       │   └── docs
│       │       ├── decisions.md
│       │       └── research
│       │           └── index.md
│       ├── broken
│       │   ├── README.md
│       │   └── docs
│       │       └── decisions.md
│       ├── consulting-map
│       │   ├── README.md
│       │   ├── SECURITY.md
│       │   └── docs
│       │       ├── current-state.md
│       │       ├── decisions.md
│       │       ├── evidence-urls.json
│       │       └── research
│       │           ├── consulting.md
│       │           └── index.md
│       ├── evidence-shape
│       │   ├── README.md
│       │   ├── SECURITY.md
│       │   └── docs
│       │       └── evidence-urls.json
│       ├── evidence-profile
│       │   ├── README.md
│       │   ├── SECURITY.md
│       │   └── docs
│       │       ├── decisions.md
│       │       ├── evidence-urls.json
│       │       └── research
│       │           └── index.md
│       ├── grade-a
│       │   ├── README.md
│       │   ├── SECURITY.md
│       │   └── skills
│       │       └── example
│       │           └── SKILL.md
│       ├── grade-b
│       │   ├── README.md
│       │   ├── SECURITY.md
│       │   └── docs
│       │       ├── current-state.md
│       │       ├── decisions.md
│       │       ├── evidence-urls.json
│       │       └── research
│       │           └── index.md
│       ├── research-integrity
│       │   ├── README.md
│       │   ├── SECURITY.md
│       │   └── docs
│       │       ├── decisions.md
│       │       ├── evidence-urls.json
│       │       └── research
│       │           └── index.md
│       ├── payload-boundary
│       │   ├── README.md
│       │   ├── SECURITY.md
│       │   └── skills
│       │       └── example
│       │           └── SKILL.md
│       ├── skill-name-mismatch
│       │   ├── README.md
│       │   ├── SECURITY.md
│       │   └── skills
│       │       └── example
│       │           └── SKILL.md
│       ├── stale-evidence
│       │   ├── README.md
│       │   ├── SECURITY.md
│       │   └── docs
│       │       └── evidence-urls.json
│       ├── standard-document
│       │   ├── README.md
│       │   ├── SECURITY.md
│       │   ├── STANDARD.md
│       │   └── docs
│       │       └── current-state.md
│       └── undocumented-gate
│           ├── .githooks
│           │   └── pre-push
│           ├── README.md
│           └── SECURITY.md
├── docs
│   ├── current-state.md
│   ├── decisions.md
│   ├── evidence-urls.json
│   ├── MAINTENANCE.md
│   └── research
│       ├── consulting.md
│       ├── evidence-appraisal.md
│       ├── incident-reports
│       │   └── 2026-10-17-fleet-ci-rot-and-agent-drift.md
│       ├── index.md
│       └── trade-study.md
└── scripts
    ├── check_commit_messages.py
    ├── check_conformance.py
    ├── gate_check.py
    ├── standards_check.py
    └── verify_urls.py
```

## Verification

```bash
python3 scripts/standards_check.py
python3 scripts/standards_check.py --self-test
python3 scripts/check_commit_messages.py --self-test
python3 scripts/check_conformance.py
python3 scripts/check_conformance.py --self-test
python3 scripts/gate_check.py
python3 scripts/gate_check.py --self-test
python3 scripts/verify_urls.py --self-test
```

The live external-reference check makes network requests and is intentionally
kept out of the default local suite:

```bash
python3 scripts/verify_urls.py
```

CI also runs the commit-message checker over every non-merge commit introduced
by a pull request targeting `main` or a push to `main`. Dependabot's generated
commits remain the documented exception in `docs/decisions.md` D19.

## Enable the hooks

```bash
git config core.hooksPath .githooks
```

## Conformance

See the checklist at the end of [`STANDARD.md`](STANDARD.md). Grades are
additive and self-asserted; a repository reclaims a lower grade without shame
when a control's failure mode is not present.

A grade claim is an assertion until a passing check evidences it. A repository
that wants the claim to be durable may record it in a short `CONFORMANCE.md`
naming the claimed grade, the `STANDARD.md` version it was checked against, and
the date of the check. This repository's own claim is in
[`CONFORMANCE.md`](CONFORMANCE.md).

## What is next

The current prioritized next steps live in
[`docs/current-state.md`](docs/current-state.md) under "What is next".

## License

MIT. See [`LICENSE`](LICENSE).
