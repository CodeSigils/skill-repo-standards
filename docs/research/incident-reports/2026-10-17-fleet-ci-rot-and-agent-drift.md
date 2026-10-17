# Incident report: fleet CI rot and agent drift

- **Date:** 2026-10-17
- **Status:** closed (remediated)
- **Owner of record:** `docs/research/index.md` (this file is an evidence input to
  `R-031`; it is not a rule owner and not a source registry)
- **Scope:** four sibling repositories under one maintainer — `skill-discovery`,
  `awesome-agent-trust`, `zero-md-formatter`, `zola-skill`

This is a first-party, dated record of what was found and fixed. It states
evidence, not rules; the normative control it supports lives in `STANDARD.md`
and is decided in `docs/decisions.md` (`D33`).

## Summary

A fleet of related repositories had accumulated gate rot and stale branches that
PR-centric views did not surface. Three repositories had a red or absent gate on
`main` or an unrelated stranded pull request; a fourth carried merged-but-
undeleted branches. The common thread: *advisory* checks were treated as
conformance, and "done" was measured by a pull request's state rather than the
default branch's.

## The six defects

1. **Expired evidence plus token-originated merges that never ran CI.**
   `skill-discovery`'s scheduled check had gone red, and merges performed with
   the default `GITHUB_TOKEN` did not trigger a workflow run, so the default
   branch rotted while every visible pull request looked green.

2. **A deleted upstream turning a soft link into a hard failure.**
   `awesome-agent-trust` referenced an upstream repository that had been deleted;
   the link check returned a definite `404` (not an environmental failure) and
   failed the gate as a non-waivable hard error. An unrelated pull request was
   stranded behind it.

3. **An evidence-freshness window shorter than the schedule cadence.**
   `zero-md-formatter` checked evidence within a 30-day window against a weekly
   scheduled job, so the check went red periodically with no code change.

4. **A required status check that matched no job.**
   Branch protection on `zero-md-formatter` required a check named
   `test (25.x)`, but the workflow matrix built `24.x` and `26.x`, so every pull
   request was blocked by a check name that could never report.

5. **A duplicate lineage with identical trees.**
   Local `main` in `zero-md-formatter` diverged from the remote with no common
   origin. The trees were byte-identical, so a reset discarded no work — but a
   naive "diverged, therefore unsafe" reading would have preserved a dead branch
   forever.

6. **A release-surface blind spot.** The npm artifact at `1.5.1` and the source
   claiming `1.5.1` disagreed: `SKILL.md` had gained a `license:` line and
   `package.json` had gained a script without a version bump. Nothing reconciled
   the package version, the git tag, and the published registry artifact.

## Behavioural failures

- **Pushing into a known-red gate.** Work was pushed on top of a failing default
  branch rather than fixing the gate first.
- **Measuring "done" by branch content, not the default branch.** An agent
  treated a merged or in-flight branch as completion while `main` stayed red.
- **No hygiene inspection before a sweep.** Stale branches and stranded pull
  requests were not enumerated before a destructive readme operation, so the
  operation's effect was misattributed.

## Options considered

- **A — Agent awareness only.** Weakest in isolation; a prompt cannot enumerate
  state it is not told to read.
- **B — A gating conformance check in the standard.** The right home for the
  machine-observable subset: a required check name resolves to a job; an evidence
  window exceeds the schedule cadence; a publish workflow's version, tag, and
  registry artifact agree.
- **C — A GitHub template repository.** Would help only new repositories and
  skips the existing fleet; not the right leverage.
- **D — A scheduled full-gate job.** The missing piece for defect 1: a cadence
  that runs the whole gate on the default branch regardless of how a commit
  arrived.

**Recommendation:** B + D, with A as a backstop; not C.

## Remediation performed

- `skill-discovery`: pull request merged; `main` green.
- `awesome-agent-trust`: the dead upstream link fixed in source (a definite
  `404` is drift, never waived); the stranded pull request merged; stale
  worktrees pruned; `main` green.
- `zero-md-formatter`: the duplicate lineage reset to origin (identical trees, no
  work lost); the required check corrected from `test (25.x)` to `test (26.x)`;
  dependabot pull request rebased and merged; `main` green.
- `zola-skill`: the two merged-but-undeleted branches deleted locally and on the
  remote; the intentional `backup/pre-rewrite` safety branch retained (unique
  non-ancestor lineage). The "duplicate commit subjects" on `main` were benign
  non-squash merge commits with trees identical to the branch tips — nothing to
  fix. Root cause of the lingering branches: the repository sets
  `delete_branch_on_merge = false`.
- The standalone evidence check `verify.py --all` passed its full 1820-check run.

## Durable findings

1. Hard, non-waivable gate errors are fixed in source, never waived through an
   exceptions file.
2. A divergence count is not lost work; compare trees before discarding lineage.
3. Never push into a known-red gate.
4. "Done" is measured by the default branch, not by a pull request's state.
5. Token-originated merges do not trigger a workflow run, so a gate can appear to
   pass while the default branch rots.
6. The release surface — package version, git tag, registry artifact — is a
   first-class property that nothing was reconciling.
7. A state-changing git action should first read the target repository's own
   document chain and the read-only git facts (`status`, `branch -a -vv`,
   `fetch --prune`, recent `log`, and an ancestry/tree check).

## Sources

- `https://git-scm.com/docs/git-status`
- `https://git-scm.com/docs/git-branch`
- `https://git-scm.com/docs/git-log`
- `https://git-scm.com/docs/git-fetch`
- `https://git-scm.com/docs/git-merge-base`
- `https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication`
- `https://docs.github.com/en/actions/reference/events-that-trigger-workflows`
- `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches`
