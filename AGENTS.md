# Repository agent guidance

## What this repository is

`skill-repo-standards` is a **specification plus a bundled reference validator**.
It is maintainer infrastructure: it ships no runtime payload to any agent. The
normative document is `STANDARD.md`; the executable part is
`scripts/standards_check.py`.

## Read first

Before changing anything, read:

1. `STANDARD.md` — the normative rules. Do not restate them elsewhere; link.
2. `README.md` — layout, usage, and the verification commands.
3. `docs/decisions.md` — durable decisions already made, with sources.
4. The specific script or document you intend to change.

## Before re-researching

Follow the research-once protocol in `STANDARD.md`. Search `docs/decisions.md`,
`docs/evidence-urls.json`, and `docs/research/index.md` before performing new
research. Reuse a recorded decision when its scope and freshness fit; revalidate
volatile facts at the point of use; record whether the result was reused,
revalidated, superseded, or newly discovered.

## Canonical-owner rule

Every rule has exactly one owning file. If you find the same rule asserted in
two files, one is wrong: keep the owning file and make the other a link.

## When you change the standard

Follow the change lifecycle in `STANDARD.md`. It is the single owner of the
process — research → finding → decision → implementation → check — including
which files to update and which source to register. A change to this standard's
own version or status follows the `## Standard lifecycle` section there. Do not
restate either here.

## Commit contract

Use `type[(scope)]: verb — rationale` for the subject, then a body with a
`what:` line followed by a `why:` line. Do not use GitHub closing keywords
(`fix`, `close`, `resolve` followed by an issue number) — they auto-close issues
on merge. Reference an issue with `Refs` instead.

## Verification before claiming completion

Run the commands in the README's Verification section. The deterministic checks
must pass; the live URL check is optional locally.
