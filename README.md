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

## The two layers

- **The standard** — [`STANDARD.md`](STANDARD.md). A graded specification
  (Grade A spine, Grade B anti-rot core, Grade C justified controls) with a
  normative proportionality rule: adopt a control only when its failure mode
  actually exists.
- **The validator** — [`scripts/standards_check.py`](scripts/standards_check.py).
  Checks spine files, the standard's own document and review date, the decision
  schema, the research register, the research-to-decision edge, evidence
  registration, freshness, the evidence index, and the payload boundary. It
  detects drift; it never judges prose.

## Use the validator

```bash
python3 scripts/standards_check.py            # check this repository
python3 scripts/standards_check.py TARGET     # check another repository
python3 scripts/standards_check.py --self-test
```

Exit codes follow the local check contract: `0` clean, `1` findings, `2` could
not run.

## Repository layout

```text
.
├── .githooks
│   ├── commit-msg
│   ├── pre-commit
│   └── pre-push
├── .github
│   └── workflows
│       └── ci.yml
├── .gitignore
├── AGENTS.md
├── CONFORMANCE.md
├── LICENSE
├── README.md
├── SECURITY.md
├── STANDARD.md
├── docs
│   ├── current-state.md
│   ├── decisions.md
│   ├── evidence-urls.json
│   └── research
│       └── index.md
└── scripts
    ├── check_commit_messages.py
    ├── standards_check.py
    └── verify_urls.py
```

## Verification

```bash
python3 scripts/standards_check.py
python3 scripts/standards_check.py --self-test
python3 scripts/check_commit_messages.py --self-test
python3 scripts/verify_urls.py --self-test
```

The live external-reference check makes network requests and is intentionally
kept out of the default local suite:

```bash
python3 scripts/verify_urls.py
```

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

## License

MIT. See [`LICENSE`](LICENSE).
