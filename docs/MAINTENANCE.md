# Maintenance

This document owns repository-only operational runbooks. It does not define the
standard: `STANDARD.md` owns version meaning and compatibility, and `AGENTS.md`
owns maintainer-agent routing.

## Publish a standard release

Publish only when a commit changes the normative `STANDARD.md` version or changes
the standard's status. Do not tag ordinary CI, agent-guidance, README, current
state, or other repository-maintenance commits.

1. Start from a clean `main` that is up to date with `origin/main`.
2. Confirm `CONFORMANCE.md` names the same `STANDARD.md` version and records a
   current passing conformance run.
3. Run every deterministic command in the README's Verification section, the
   live `python3 scripts/verify_urls.py` check, and confirm CI is green for the
   intended release commit.
4. Create and push an annotated tag named `v<VERSION>` on that commit. Its
   annotation identifies the standard version and whether it is draft or stable.
5. Publish one GitHub release from that tag. While `STANDARD.md` is `draft`, mark
   the release as a prerelease; do not present it as the latest stable release.
   The release notes link the version's migration section, `CONFORMANCE.md`, and
   the linked decision record.
6. Do not move, delete, or retroactively create published release tags. A later
   standard version receives its own tag and release.

The release cadence is event-driven: one release for each normative standard
version, never a calendar release without such a version. The twice-yearly
review in `STANDARD.md` remains an evidence-review obligation, not a release
trigger.
