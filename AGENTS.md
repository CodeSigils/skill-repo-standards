# Repository agent guidance

## What this repository is

`skill-repo-standards` is a **specification plus a bundled reference validator**.
It is maintainer infrastructure: it ships no runtime payload to any agent. The
normative document is `STANDARD.md`; the executable part is
`scripts/standards_check.py`.

## Read first

Before changing anything, read, in this order:

1. `AGENTS.md` — this file: the working contract for the repository.
2. `STANDARD.md` — the normative rules. Read them before the README, so a
   README sentence is not mistaken for a rule. Do not restate them elsewhere;
   link.
3. `README.md` — layout, usage, and the verification commands.
4. `docs/current-state.md` — what is true now, including the `## What is next`
   list of committed-but-unbuilt work.
5. `docs/decisions.md` — durable decisions already made, with sources.
6. `docs/research/consulting.md` — the canonical research consultation guide.
7. The specific script or document you intend to change.
8. `CONFORMANCE.md` last — a status snapshot (grade, version, checked date,
   corpus count), not a rule owner.

Pull `docs/research/index.md` and `docs/evidence-urls.json` on demand; the
consultation guide routes to them.

## Cold boot

On a cold first run, before you change anything:

1. **Check state and CI, and report before working.** Run `git status -sb`,
   `git fetch && git status -sb`, `git remote -v`, and `git log --oneline -10`,
   and check CI with `gh run list`. Report a dirty tree, a diverged branch, or
   red or absent CI before you start rather than working on top of it.
2. **Run the deterministic gates** in the README's Verification section and
   confirm they pass, so you start from a known-good checkout.
3. **Confirm the shape.** This repository is maintainer infrastructure with no
   `skills/` payload (see above), so the payload-boundary check is inert and
   Grade A's payload item does not apply.
4. **Name the target and its owner.** Identify the specific file you intend to
   change and the single rule that owns it.

## Before re-researching

Follow the research-once protocol in `STANDARD.md` through the canonical
[`docs/research/consulting.md`](docs/research/consulting.md) guide. Follow its
[evidence-first workflow](docs/research/consulting.md#evidence-first-workflow)
without substituting a local variant. Search `docs/decisions.md`,
`docs/evidence-urls.json`, and `docs/research/index.md` before performing new
research. Reuse a recorded decision when its scope and freshness fit; revalidate
volatile facts at the point of use; record whether the result was reused,
revalidated, superseded, or newly discovered. When the user asks for a coverage
review, audit the concern map against the registry and recent decisions first;
search official web guidance only for a recurring, decision-worthy gap.

For a new behaviour-changing decision, use
[`docs/research/evidence-appraisal.md`](docs/research/evidence-appraisal.md).
If the decision has multiple viable alternatives and material risk, cost, or
irreversibility, consult `docs/research/trade-study.md`; do not invent a scoring
matrix for a routine choice.

## Owner of truth

Truth has one owner per audience. `docs/current-state.md` owns what is true about
this repository; the runtime payload owns what an installed skill does, and a
payload does not link into `docs/`. Every other file links to the owner rather
than restating it. See `STANDARD.md` §The anti-rot core.

## Canonical-owner rule

Every rule has exactly one owning file. If you find the same rule asserted in
two files, one is wrong: keep the owning file and make the other a link.

## When you change the standard

Follow the change lifecycle in `STANDARD.md`. It is the single owner of the
process — research → finding → decision → implementation → check — including
which files to update and which source to register. A change to this standard's
own version or status follows the `## Standard lifecycle` section there. Do not
restate either here.

## Dependabot

Dependabot opens `github-actions` version updates weekly, grouped and capped by
`.github/dependabot.yml`. Merge one only after the canonical gate passes: read
the diff, then confirm the checks are green. Never enable auto-merge. A
Dependabot commit does not satisfy the commit contract below, and the local
`commit-msg` hook cannot enforce anything on a bot; that exception is recorded
in `docs/decisions.md` D19 rather than left implicit.

## Commit contract

Use `type[(scope)]: verb — rationale` for the subject, then a body with a
`what:` line followed by a `why:` line. Do not use GitHub closing keywords
(`fix`, `close`, `resolve` followed by an issue number) — they auto-close issues
on merge. Reference an issue with `Refs` instead.

For standard-release versioning, follow the rule in
[`STANDARD.md`'s change lifecycle](STANDARD.md#change-lifecycle).

## Verification before claiming completion

Run the commands in the README's Verification section. The deterministic checks
must pass; the live URL check is optional locally.
