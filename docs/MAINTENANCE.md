# Maintenance

This document owns repository-only operational runbooks. It does not define the
standard: `STANDARD.md` owns version meaning and compatibility, and `AGENTS.md`
owns maintainer-agent routing.

## Publish a standard release

Before proposing or performing release work, read this runbook and inspect the
current `STANDARD.md` version and status, existing local and remote tags, and
GitHub releases, including drafts and prereleases. Identify any tag without a
matching published release and report its state before proposing another release.
If the remote tags or GitHub releases cannot be inspected, report that gap and
do not assume the version has not already been published.

Choose a release deliberately when a useful, reviewed set of standard changes is
ready for adopters. There is no release for each commit or calendar interval.
Collect and review related proposals before implementing them together under one
version; do not merge changed normative requirements under an already published
version. Apply the compatibility and version rules in
[`STANDARD.md`](../STANDARD.md#standard-lifecycle) to the complete batch.
Routine commits, pushes, and maintenance changes do not themselves authorize a
version bump, tag, or release.

Publish one release for each normative `STANDARD.md` version or status change.
Target a verified commit that contains that version; do not create a release tag
solely for ordinary CI, agent-guidance, README, current-state, or other
repository-maintenance changes.

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
6. Verify that the remote tag points to the intended commit and the GitHub
   release is published with the correct prerelease status and notes. If tagging
   succeeds but publication or verification fails, report the release as
   incomplete and its exact state; resolve it using the existing tag rather than
   creating another tag for the same version.
7. Do not move, delete, or retroactively create published release tags. A later
   standard version receives its own tag and release.

The release cadence is event-driven: one release for each normative standard
version, never a calendar release without such a version. The twice-yearly
review in `STANDARD.md` remains an evidence-review obligation, not a release
trigger.
