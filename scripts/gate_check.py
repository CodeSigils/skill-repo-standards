#!/usr/bin/env python3
"""Gating and release-surface drift check for a target repository.

Four assertions, each backed by an observed fleet failure recorded in
`docs/research/incident-reports/2026-10-17-fleet-ci-rot-and-agent-drift.md`
and decided in `docs/decisions.md` D33:

1. **Required checks resolve to a job.** Every branch-protection required status
   check name must resolve to a job or a matrix-expanded job name in
   `.github/workflows`. An unmatched name is inconclusive because an external
   provider may supply the check.
2. **Evidence window versus schedule.** The checker cannot infer which schedule
   refreshes evidence or which freshness window a repository actually enforces.
3. **A scheduled workflow must run a full gate.** If a workflow has a
   `schedule:` trigger, at least one of its jobs must be able to run on a
   scheduled event — a workflow whose every job is gated by an event-name
   condition excluding `schedule` never exercises the gate on a cadence. A
   runnable job alone does not establish that the full gate runs.
4. **The release surface agrees.** A repository with a publish workflow must not
   disagree between its package version, its `v*` tags, and its published
   registry artifact: a tag whose package version differs from the tag name, or
   a published registry version with no matching tag, is a release-surface
   defect.

Contract (see STANDARD.md §Local check contract): exit 0 clean, 1 findings,
2 could not run. An assertion whose input does not exist in the target (no
branch protection, no schedule, no publish workflow) is *not applicable* and
notes rather than failing; an assertion whose input exists but cannot be read
(git absent, network refused, unparseable matrix) is *unavailable*. Only a
definite disagreement is a hard finding — an unparsable input never fails.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

Finding = tuple[str, str]

NOMINAL_MAX_AGE_DAYS = 180
DEFAULT_MAX_AGE_DAYS = 180


def hard(message: str) -> Finding:
    return ("hard", message)


def soft(message: str) -> Finding:
    return ("soft", message)


# --------------------------------------------------------------------------
# workflow parsing (stdlib only; conservative: unreadable means "unavailable")
# --------------------------------------------------------------------------

_JOB_RE = re.compile(r"^  ([A-Za-z0-9_.-]+):\s*$")
_JOB_NAME_RE = re.compile(r"^    name:\s*(.+?)\s*$")
_IF_RE = re.compile(r"^    if:\s*(.+?)\s*$")
_MATRIX_INLINE_RE = re.compile(r"^        ([A-Za-z0-9_.-]+):\s*\[([^\]]*)\]\s*$")
_MATRIX_KEY_RE = re.compile(r"^        ([A-Za-z0-9_.-]+):\s*$")
_MATRIX_ITEM_RE = re.compile(r"^          -\s*(.+?)\s*$")
_SCHEDULE_KEY_RE = re.compile(r"^\s+schedule:\s*$")
_CRON_EXPR_RE = re.compile(r"^\s*(?:-\s*)?cron:\s*['\"]?([^'\"\n]+?)['\"]?\s*$")
_USES_JOB_GATE_RE = re.compile(r"event_name")


def _unquote(value: str) -> str:
    """Strip quotes only when they wrap the whole scalar.

    A condition such as `github.event_name == 'push'` must not lose its closing
    quote, or the comparison logic downstream would never see the event name.
    """
    stripped = value.strip()
    if len(stripped) >= 2 and stripped[0] in "'\"" and stripped[-1] == stripped[0]:
        return stripped[1:-1]
    return stripped


def parse_workflow(path: Path) -> dict:
    """Line-oriented, deliberately conservative parse of one workflow file.

    Returns a dict with `has_schedule`, `cron`, and `jobs`. A job whose matrix
    cannot be reduced to scalar literal values is marked `matrix_unknown`, so a
    later comparison refuses to call a mismatch instead of inventing one.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    has_schedule = False
    cron: str | None = None
    for index, line in enumerate(lines):
        if _SCHEDULE_KEY_RE.match(line):
            has_schedule = True
            if cron is None:
                for look_ahead in lines[index + 1 : index + 4]:
                    match = _CRON_EXPR_RE.match(look_ahead)
                    if match:
                        cron = match.group(1).strip()
                        break

    jobs: list[dict] = []
    current: dict | None = None
    in_jobs = False
    in_matrix = False
    matrix_values: list[str] = []
    matrix_key = False
    matrix_parsed = False
    matrix_axes = 0
    matrix_complex = False

    for line in lines:
        if line.startswith("jobs:"):
            in_jobs = True
            continue
        if not in_jobs:
            continue
        job_match = _JOB_RE.match(line)
        if job_match:
            if current is not None:
                current["matrix_values"] = matrix_values if matrix_parsed else None
                current["matrix_unknown"] = bool(
                    current.pop("_saw_matrix", False)
                ) and (not matrix_parsed or matrix_complex or matrix_axes != 1)
                jobs.append(current)
            current = {
                "id": job_match.group(1),
                "name": None,
                "if": None,
                "_saw_matrix": False,
            }
            in_matrix = False
            matrix_values = []
            matrix_key = False
            matrix_parsed = False
            matrix_axes = 0
            matrix_complex = False
            continue
        if current is None:
            continue

        name_match = _JOB_NAME_RE.match(line)
        if name_match and current["name"] is None:
            current["name"] = _unquote(name_match.group(1))
            continue

        if_match = _IF_RE.match(line)
        if if_match and current["if"] is None:
            current["if"] = _unquote(if_match.group(1))
            continue

        if line.strip().startswith("matrix:"):
            current["_saw_matrix"] = True
            in_matrix = True
            matrix_key = False
            continue

        if in_matrix:
            if line.startswith("    ") and not line.startswith("      "):
                in_matrix = False
            else:
                inline = _MATRIX_INLINE_RE.match(line)
                if inline:
                    matrix_axes += 1
                    values = [v.strip() for v in inline.group(2).split(",")]
                    if any("${{" in v or "{" in v or ":" in v for v in values):
                        matrix_complex = True
                    if values:
                        matrix_values.extend(_unquote(v) for v in values)
                        matrix_parsed = True
                    continue
                key = _MATRIX_KEY_RE.match(line)
                if key:
                    matrix_axes += 1
                    if key.group(1) in {"include", "exclude"}:
                        matrix_complex = True
                    matrix_key = True
                    matrix_values = []
                    continue
                item = _MATRIX_ITEM_RE.match(line)
                if item and matrix_key:
                    if "${{" in item.group(1) or ":" in item.group(1):
                        matrix_complex = True
                    matrix_values.append(_unquote(item.group(1)))
                    matrix_parsed = True
                    continue
                if line.strip() and not line.startswith(" " * 8):
                    matrix_key = False

    if current is not None:
        current["matrix_values"] = matrix_values if matrix_parsed else None
        current["matrix_unknown"] = bool(current.pop("_saw_matrix", False)) and (not matrix_parsed or matrix_complex or matrix_axes != 1)
        jobs.append(current)

    return {
        "path": path,
        "has_schedule": has_schedule,
        "cron": cron,
        "jobs": jobs,
    }


def parse_workflows(workdir: Path) -> list[dict]:
    workflow_dir = workdir / ".github" / "workflows"
    if not workflow_dir.is_dir():
        return []
    paths = sorted(
        p
        for p in workflow_dir.iterdir()
        if p.is_file() and p.suffix in {".yml", ".yaml"}
    )
    return [parse_workflow(p) for p in paths]


def check_name_set(workflows: list[dict]) -> tuple[set[str], bool]:
    """Expand every job into the check names GitHub would report.

    Returns the set of names and whether some job has a matrix we could not
    expand, in which case a caller must not conclude that a name is missing.
    """
    names: set[str] = set()
    unknown_matrix = False
    for workflow in workflows:
        for job in workflow["jobs"]:
            label = job["name"] or job["id"]
            if "${{" in label:
                unknown_matrix = True
            if not job.get("matrix_values") and not job.get("matrix_unknown"):
                names.add(label)
            if job.get("_saw_matrix") or "matrix_unknown" in job:
                if job.get("matrix_unknown"):
                    unknown_matrix = True
            if job.get("matrix_values"):
                for value in job["matrix_values"]:
                    names.add(f"{label} ({value})")
    return names, unknown_matrix


# --------------------------------------------------------------------------
# assertion 1 — required check names resolve to a job
# --------------------------------------------------------------------------

def assert_required_checks_resolve(
    required: list[str], available: set[str], unknown_matrix: bool
) -> list[Finding]:
    if not required:
        return []
    if unknown_matrix:
        return []
    findings: list[Finding] = []
    for context in required:
        if context in available:
            continue
        findings.append(soft(f"required check '{context}' resolves to no local workflow job; it may be supplied by an external provider"))
    return findings


def load_required_checks(workdir: Path, branch: str) -> tuple[list[str] | None, str, str]:
    """Returns (contexts, kind, detail); kind is 'ok' | 'inapplicable' | 'unavailable'."""
    if shutil.which("gh") is None:
        return None, "unavailable", "gh CLI not available"
    remote = ""
    try:
        remote = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=workdir,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
    except OSError:
        remote = ""
    match = re.search(r"[:/]([^/]+/[^/]+?)(?:\.git)?$", remote)
    if not match:
        return None, "unavailable", "cannot derive owner/repository from origin"
    slug = match.group(1)
    result = subprocess.run(
        ["gh", "api", f"repos/{slug}/branches/{branch}/protection/required_status_checks"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            return None, "unavailable", "branch-protection response was not JSON"
        contexts = payload.get("contexts") or []
        return list(contexts), "ok", f"{len(contexts)} required check(s)"
    if "Branch not protected" in result.stderr:
        return [], "inapplicable", "branch is not protected"
    return None, "unavailable", result.stderr.strip().splitlines()[-1] if result.stderr else "gh api failed"


def check_required_checks(workdir: Path, branch: str) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    notes: list[str] = []
    workflows = parse_workflows(workdir)
    if not workflows:
        notes.append("required-check assertion could not run: no workflow files found")
        return findings, notes
    required, kind, detail = load_required_checks(workdir, branch)
    if kind == "inapplicable":
        notes.append(f"required-check assertion not applicable: {detail}")
        return findings, notes
    if kind == "unavailable" or required is None:
        notes.append(f"required-check assertion could not run: {detail}")
        return findings, notes
    if not required:
        notes.append("required-check assertion not applicable: no required checks")
        return findings, notes
    available, unknown_matrix = check_name_set(workflows)
    if unknown_matrix:
        notes.append("required-check assertion could not run: matrix cannot be expanded")
        return findings, notes
    unmatched = assert_required_checks_resolve(required, available, unknown_matrix)
    for _, message in unmatched:
        notes.append(f"required-check assertion could not run: {message}")
    if not unmatched:
        notes.append(f"all {len(required)} required check(s) resolve to a workflow job")
    return findings, notes


# --------------------------------------------------------------------------
# assertion 2 — evidence window exceeds schedule cadence
# --------------------------------------------------------------------------

def cron_cadence_days(cron: str | None) -> int | None:
    """Days between scheduled runs, or None when the cadence is not decidable."""
    if not cron:
        return None
    parts = cron.split()
    if len(parts) != 5:
        return None
    day_of_month, month, day_of_week = parts[2], parts[3], parts[4]
    if month != "*":
        return None
    if day_of_week == "*":
        return 1 if day_of_month == "*" else None
    if day_of_week.startswith("*/"):
        try:
            return 7 * int(day_of_week[2:])
        except ValueError:
            return None
    return 7


def assert_window_exceeds_cadence(window_days: int, cadence_days: int) -> list[Finding]:
    if window_days > cadence_days:
        return []
    return [
        hard(
            f"evidence freshness window ({window_days} days) does not exceed the "
            f"schedule cadence ({cadence_days} days); the gate will go red on "
            f"schedule without any code change"
        )
    ]


def check_window_vs_cadence(workdir: Path, max_age_days: int) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    notes: list[str] = []
    workflows = [w for w in parse_workflows(workdir) if w["has_schedule"]]
    if not workflows:
        notes.append("evidence-window assertion not applicable: no schedule trigger")
        return findings, notes
    notes.append("evidence-window assertion could not run: evidence refresh schedule and enforced window cannot be inferred")
    return findings, notes


# --------------------------------------------------------------------------
# assertion 3 — a scheduled workflow must run at least one gating job
# --------------------------------------------------------------------------

def _excludes_schedule(condition: str | None) -> bool:
    """True only for a condition that clearly forbids the scheduled event.

    `github.event_name == 'push'` excludes a schedule run without ever naming
    it, so the test is an equality against a different event (or an explicit
    `!= 'schedule'`). An equality against `'schedule'`, or a condition that also
    admits it, does not exclude.
    """
    if not condition:
        return False
    expression = condition.strip()
    if expression.startswith("${{") and expression.endswith("}}"):
        expression = expression[3:-2].strip()
    match = re.fullmatch(r"github\.event_name\s*(==|!=)\s*(['\"])([a-z_]+)\2", expression)
    if match is None:
        return False
    operator, _, event = match.groups()
    return (operator == "==" and event != "schedule") or (operator == "!=" and event == "schedule")


def assert_scheduled_workflow_runs_full_gate(jobs: list[dict]) -> list[Finding]:
    if not jobs:
        return []
    runnable = [j for j in jobs if not _excludes_schedule(j.get("if"))]
    if runnable:
        return []
    return [
        hard(
            "workflow has a schedule trigger but every job is gated by an "
            "event-name condition that excludes the scheduled event, so the "
            "gate never runs on its cadence"
        )
    ]


def check_scheduled_gate(workdir: Path) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    notes: list[str] = []
    workflows = [w for w in parse_workflows(workdir) if w["has_schedule"]]
    if not workflows:
        notes.append("scheduled-gate assertion not applicable: no schedule trigger")
        return findings, notes
    for workflow in workflows:
        local = assert_scheduled_workflow_runs_full_gate(workflow["jobs"])
        if local:
            findings.extend(
                hard(f"{workflow['path'].name}: {message}") for _, message in local
            )
        else:
            notes.append(f"{workflow['path'].name}: scheduled-gate assertion could not run: runnable jobs do not establish full gate coverage")
    return findings, notes


# --------------------------------------------------------------------------
# assertion 4 — release surface: version, tag, registry agree
# --------------------------------------------------------------------------

def _parse_semver(text: str) -> tuple[int, ...] | None:
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", text.strip())
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def assert_release_surface(
    package_version: str | None,
    tagged_versions: dict[str, str],
    registry_version: str | None,
    registry_reachable: bool,
    published_versions: list[str] | None = None,
) -> tuple[list[Finding], list[str]]:
    """`tagged_versions` maps a `v*` tag to the package version found at it."""
    findings: list[Finding] = []
    notes: list[str] = []

    if package_version is None:
        notes.append("release-surface assertion could not run: no package.json version")
        return findings, notes

    for tag, version_at_tag in sorted(tagged_versions.items()):
        if version_at_tag != package_version and version_at_tag != tag.lstrip("v"):
            pass  # checked below against the tag's own name
        expected = tag[1:] if tag.startswith("v") else tag
        if version_at_tag != expected:
            findings.append(
                hard(
                    f"tag {tag} points at a package version {version_at_tag}, "
                    f"so the tag name and the version it releases disagree"
                )
            )

    if registry_reachable:
        if not registry_version:
            notes.append("release-surface assertion could not run: registry returned no latest version")
        else:
            if published_versions is None:
                notes.append("release-surface assertion could not run: registry version list unavailable")
            else:
                for tag, version in sorted(tagged_versions.items()):
                    if version not in published_versions:
                        findings.append(hard(f"tag {tag} exists but version {version} is absent from the registry"))
            if f"v{registry_version}" not in tagged_versions and not any(
                tag.lstrip("v") == registry_version for tag in tagged_versions
            ):
                findings.append(
                    hard(
                        f"registry publishes {registry_version} but no matching "
                        f"git tag exists, so the release surface is untagged"
                    )
                )
            registry_semver = _parse_semver(registry_version or "")
            package_semver = _parse_semver(package_version or "")
            if (
                registry_semver is not None
                and package_semver is not None
                and registry_semver != package_semver
                and registry_semver > package_semver
            ):
                findings.append(
                    hard(
                        f"registry is ahead of the source: registry "
                        f"{registry_version} but package.json declares "
                        f"{package_version}"
                    )
                )
    else:
        notes.append("release-surface registry leg could not run: network unavailable")

    return findings, notes


def _read_package_version(workdir: Path, spec: str | None = None) -> str | None:
    target = "package.json"
    if spec:
        result = subprocess.run(
            ["git", "show", f"{spec}:{target}"],
            cwd=workdir,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return None
        raw = result.stdout
    else:
        path = workdir / target
        if not path.is_file():
            return None
        raw = path.read_text(encoding="utf-8")
    try:
        return str(json.loads(raw).get("version"))
    except (json.JSONDecodeError, AttributeError, TypeError):
        return None


def _registry_version(workdir: Path) -> tuple[bool, str | None]:
    package_path = workdir / "package.json"
    if not package_path.is_file():
        return False, None
    try:
        name = str(json.loads(package_path.read_text(encoding="utf-8")).get("name"))
    except (json.JSONDecodeError, AttributeError, TypeError):
        return False, None
    if shutil.which("npm") is None:
        return False, None
    result = subprocess.run(
        ["npm", "view", name, "version"],
        cwd=workdir,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return False, None
    value = result.stdout.strip().splitlines()
    return True, value[-1] if value else None


def _registry_versions(workdir: Path) -> list[str] | None:
    try:
        package = json.loads((workdir / "package.json").read_text(encoding="utf-8"))
        name = package.get("name")
    except (OSError, json.JSONDecodeError, AttributeError):
        return None
    if not isinstance(name, str) or not name or shutil.which("npm") is None:
        return None
    result = subprocess.run(
        ["npm", "view", name, "versions", "--json"], cwd=workdir,
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        return None
    try:
        versions = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    if isinstance(versions, str):
        return [versions]
    if isinstance(versions, list) and all(isinstance(v, str) for v in versions):
        return versions
    return None


def _publish_workflows(workflows: list[dict]) -> list[dict]:
    published = []
    for workflow in workflows:
        try:
            text = workflow["path"].read_text(encoding="utf-8")
        except OSError:
            continue
        if re.search(r"npm publish|pypi|twine upload|cargo publish", text):
            published.append(workflow)
    return published


def check_release_surface(workdir: Path) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    notes: list[str] = []
    workflows = parse_workflows(workdir)
    if not _publish_workflows(workflows):
        notes.append("release-surface assertion not applicable: no publish workflow")
        return findings, notes

    package_version = _read_package_version(workdir)
    tagged: dict[str, str] = {}
    tags = subprocess.run(
        ["git", "tag", "--list", "v*"],
        cwd=workdir,
        capture_output=True,
        text=True,
        check=False,
    )
    if tags.returncode != 0:
        notes.append("release-surface assertion could not run: git tag listing failed")
        return findings, notes
    for tag in tags.stdout.split():
        version_at_tag = _read_package_version(workdir, spec=tag)
        if version_at_tag is not None:
            tagged[tag] = version_at_tag

    reachable, registry = _registry_version(workdir)
    versions = _registry_versions(workdir) if reachable else None
    local, extra = assert_release_surface(
        package_version, tagged, registry, reachable, versions
    )
    findings.extend(local)
    notes.extend(extra)
    if not findings and not any("could not run" in n for n in extra):
        notes.append("release surface agrees on version, tag, and registry")
    return findings, notes


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------

def run(target: Path, branch: str, max_age_days: int) -> tuple[list[Finding], list[str], bool]:
    """Returns (findings, notes, any_source_unavailable)."""
    findings: list[Finding] = []
    notes: list[str] = []
    unavailable = False

    def collect(result: tuple[list[Finding], list[str]]) -> None:
        nonlocal unavailable
        local, local_notes = result
        findings.extend(local)
        notes.extend(local_notes)
        for note in local_notes:
            if "could not run" in note:
                unavailable = True

    collect(check_required_checks(target, branch))
    collect(check_window_vs_cadence(target, max_age_days))
    collect(check_scheduled_gate(target))
    collect(check_release_surface(target))

    return findings, notes, unavailable


def run_self_test() -> int:
    """Build fixtures and assert each assertion fires or stays silent."""
    failures: list[str] = []

    def expect(label: str, produced: list[Finding], should_fire: bool) -> None:
        fired = bool(produced)
        if fired != should_fire:
            failures.append(
                f"{label}: expected {'a finding' if should_fire else 'no finding'}, "
                f"got {produced}"
            )

    # 1 — required check that resolves to nothing
    expect(
        "unmatched required check",
        assert_required_checks_resolve(
            ["test (25.x)"], {"test (24.x)", "test (26.x)"}, unknown_matrix=False
        ),
        should_fire=True,
    )
    expect(
        "matched required check",
        assert_required_checks_resolve(
            ["test (24.x)"], {"test (24.x)"}, unknown_matrix=False
        ),
        should_fire=False,
    )
    expect(
        "unknown matrix suppresses a verdict",
        assert_required_checks_resolve(
            ["test (25.x)"], {"test"}, unknown_matrix=True
        ),
        should_fire=False,
    )

    expect(
        "stale matrix value with base job present",
        assert_required_checks_resolve(
            ["test (25.x)"], {"test", "test (24.x)", "test (26.x)"}, False
        ),
        should_fire=True,
    )

    # 2 — freshness window shorter than the cadence
    expect(
        "window equals cadence",
        assert_window_exceeds_cadence(7, 7),
        should_fire=True,
    )
    expect(
        "window exceeds cadence",
        assert_window_exceeds_cadence(180, 7),
        should_fire=False,
    )
    if cron_cadence_days("17 4 * * 1") != 7:
        failures.append("weekly cron cadence: expected 7")
    if cron_cadence_days("0 0 * * *") != 1:
        failures.append("daily cron cadence: expected 1")

    # 3 — every job gated away from the scheduled event
    expect(
        "all jobs exclude schedule",
        assert_scheduled_workflow_runs_full_gate(
            [
                {"id": "a", "if": "github.event_name == 'push'"},
                {"id": "b", "if": "github.event_name == 'push'"},
            ]
        ),
        should_fire=True,
    )
    expect(
        "one job runs on schedule",
        assert_scheduled_workflow_runs_full_gate(
            [
                {"id": "a", "if": "github.event_name == 'push'"},
                {"id": "b", "if": None},
            ]
        ),
        should_fire=False,
    )

    # 4 — tag that lies about the version it releases
    lying, _ = assert_release_surface(
        package_version="1.5.2",
        tagged_versions={"v1.5.2": "1.5.1"},
        registry_version=None,
        registry_reachable=False,
    )
    expect("tag disagrees with its package version", lying, should_fire=True)

    untagged, _ = assert_release_surface(
        package_version="1.5.2",
        tagged_versions={},
        registry_version="1.5.1",
        registry_reachable=True,
    )
    expect("registry publishes with no matching tag", untagged, should_fire=True)

    agree, _ = assert_release_surface(
        package_version="1.5.2",
        tagged_versions={"v1.5.2": "1.5.2"},
        registry_version="1.5.2",
        registry_reachable=True,
    )
    expect("release surface agrees", agree, should_fire=False)

    _, unpublished_notes = assert_release_surface(
        "1.5.2", {"v1.5.1": "1.5.1", "v1.5.2": "1.5.2"}, "1.5.1", True
    )
    if not any("could not run" in note for note in unpublished_notes):
        failures.append("tag newer than registry latest must not be reported as verified")
    missing, _ = assert_release_surface(
        "1.5.2", {"v1.5.1": "1.5.1", "v1.5.2": "1.5.2"}, "1.5.1", True, ["1.5.1"]
    )
    expect("tagged version absent from registry", missing, should_fire=True)
    published, published_notes = assert_release_surface(
        "1.5.2", {"v1.5.1": "1.5.1", "v1.5.2": "1.5.2"}, "1.5.1", True, ["1.5.1", "1.5.2"]
    )
    if published or published_notes:
        failures.append("published version need not be registry latest")

    # workflow parser: a fixture file must survive parsing
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / "ci.yml"
        fixture.write_text(
            "name: CI\n"
            "on:\n"
            "  schedule:\n"
            "    - cron: '17 4 * * 1'\n"
            "jobs:\n"
            "  lint:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - run: echo lint\n"
            "  test:\n"
            "    name: test\n"
            "    if: github.event_name == 'push'\n"
            "    strategy:\n"
            "      matrix:\n"
            "        node: ['24.x', '26.x']\n"
            "    steps:\n"
            "      - run: echo hi\n",
            encoding="utf-8",
        )
        parsed = parse_workflow(fixture)
        if not parsed["has_schedule"] or parsed["cron"] != "17 4 * * 1":
            failures.append(f"schedule parse failed: {parsed}")
        names, unknown = check_name_set([parsed])
        if names != {"lint", "test (24.x)", "test (26.x)"}:
            failures.append(f"check-name expansion wrong: {names} unknown={unknown}")
        expected_gate = assert_scheduled_workflow_runs_full_gate(parsed["jobs"])
        if expected_gate:
            failures.append(f"gate assertion misfired on fixture: {expected_gate}")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        repo = root / "repo"
        repo.mkdir()
        bindir = root / "bin"
        bindir.mkdir()
        workflow_dir = repo / ".github" / "workflows"
        workflow_dir.mkdir(parents=True)
        (workflow_dir / "ci.yml").write_text(
            "jobs:\n  test:\n    name: test\n    strategy:\n      matrix:\n"
            "        node: ['24.x', '26.x']\n    steps:\n      - run: npm publish\n",
            encoding="utf-8",
        )
        package = repo / "package.json"
        package.write_text('{"name":"fixture-package","version":"1.5.1"}', encoding="utf-8")
        env = os.environ.copy()
        env.update({"PATH": str(bindir) + os.pathsep + env.get("PATH", ""),
                    "GIT_AUTHOR_NAME": "Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                    "GIT_COMMITTER_NAME": "Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid"})
        def git(*args: str) -> None:
            subprocess.run(["git", "-c", "commit.gpgsign=false", "-c", "tag.gpgSign=false", "-c", "core.hooksPath=/dev/null", *args], cwd=repo, env=env, check=True, capture_output=True)
        git("init", "-q")
        git("remote", "add", "origin", "https://github.com/example/fixture.git")
        git("add", ".")
        git("commit", "-qm", "fixture")
        git("tag", "v1.5.1")
        package.write_text('{"name":"fixture-package","version":"1.5.2"}', encoding="utf-8")
        git("add", "package.json")
        git("commit", "-qm", "new version")
        git("tag", "v1.5.2")
        gh = bindir / "gh"
        gh.write_text('#!/bin/sh\nif [ "$GH_FAIL" = 1 ]; then echo "HTTP 403" >&2; exit 1; fi\nprintf \'%s\\n\' "$GH_RESULT"\n', encoding="utf-8")
        npm = bindir / "npm"
        npm.write_text('#!/bin/sh\nif [ "$3" = versions ]; then if [ "$NPM_FAIL" = 1 ]; then exit 1; fi; printf \'%s\\n\' "$NPM_RESULT"; else printf \'%s\\n\' "$NPM_LATEST"; fi\n', encoding="utf-8")
        gh.chmod(0o755)
        npm.chmod(0o755)
        cases = [
            ("stale matrix or external check", '{"contexts":["test (25.x)"]}', '["1.5.1","1.5.2"]', "0", "0", 2, "may be supplied by an external provider"),
            ("unpublished tag", '{"contexts":["test (24.x)"]}', '["1.5.1"]', "0", "0", 1, "absent from the registry"),
            ("published non-latest", '{"contexts":["test (24.x)"]}', '["1.5.1","1.5.2"]', "0", "0", 0, "release surface agrees"),
            ("registry unavailable", '{"contexts":["test (24.x)"]}', "[]", "0", "1", 2, "could not run"),
            ("protection unavailable", "", '["1.5.1","1.5.2"]', "1", "0", 2, "HTTP 403"),
        ]
        for label, gh_data, npm_data, gh_fail, npm_fail, expected, message in cases:
            case_env = env | {"GH_RESULT": gh_data, "NPM_RESULT": npm_data,
                              "GH_FAIL": gh_fail, "NPM_FAIL": npm_fail, "NPM_LATEST": "1.5.1"}
            result = subprocess.run([sys.executable, str(Path(__file__).resolve()), str(repo)],
                                    env=case_env, capture_output=True, text=True)
            if result.returncode != expected or message not in result.stdout:
                failures.append(f"{label}: exit {result.returncode}, output {result.stdout!r}")
        for label, latest, versions, expected, message in [
            ("older unpublished tag", "1.5.2", '["1.5.2"]', 1, "tag v1.5.1 exists but version 1.5.1 is absent"),
            ("empty latest response", "", '["1.5.1","1.5.2"]', 2, "registry returned no latest version"),
        ]:
            result = subprocess.run(
                [sys.executable, str(Path(__file__).resolve()), str(repo)],
                env=env | {"GH_RESULT": '{"contexts":["test (24.x)"]}',
                           "NPM_RESULT": versions, "GH_FAIL": "0", "NPM_FAIL": "0", "NPM_LATEST": latest},
                capture_output=True, text=True,
            )
            if result.returncode != expected or message not in result.stdout:
                failures.append(f"{label}: exit {result.returncode}, output {result.stdout!r}")
        (workflow_dir / "ci.yml").write_text(
            "jobs:\n  test:\n    strategy:\n      matrix:\n"
            "        node: ['24.x', '26.x']\n        os: [ubuntu, windows]\n"
            "    steps:\n      - run: npm publish\n", encoding="utf-8"
        )
        result = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), str(repo)],
            env=env | {"GH_RESULT": '{"contexts":["test (24.x, ubuntu)"]}',
                       "NPM_RESULT": '["1.5.1","1.5.2"]', "GH_FAIL": "0", "NPM_FAIL": "0", "NPM_LATEST": "1.5.1"},
            capture_output=True, text=True,
        )
        if result.returncode != 2 or "matrix cannot be expanded" not in result.stdout:
            failures.append(f"unsupported matrix: exit {result.returncode}, output {result.stdout!r}")
        (workflow_dir / "ci.yml").write_text(
            "on:\n  schedule:\n    - cron: '0 0 * * 1'\n"
            "jobs:\n  test:\n    if: ${{ !(github.event_name == 'push') }}\n"
            "    steps:\n      - run: echo test\n", encoding="utf-8"
        )
        result = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), str(repo)],
            env=env | {"GH_RESULT": '{"contexts":["test"]}', "GH_FAIL": "0"},
            capture_output=True, text=True,
        )
        if result.returncode != 2 or "scheduled-gate assertion could not run" not in result.stdout:
            failures.append(f"negated schedule condition: exit {result.returncode}, output {result.stdout!r}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("OK: gate_check self-test passed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default=".", help="repository to check")
    parser.add_argument("--branch", default="main", help="branch for protection checks")
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=DEFAULT_MAX_AGE_DAYS,
        help="evidence freshness window the validator enforces",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_test()

    target = Path(args.target)
    if not target.is_dir():
        print(f"FAIL: {target} is not a directory", file=sys.stderr)
        return 2

    findings, notes, unavailable = run(target, args.branch, args.max_age_days)
    for note in notes:
        print(f"NOTE: {note}")
    hard_count = 0
    for kind, message in findings:
        print(f"FAIL: {message}")
        if kind == "hard":
            hard_count += 1
    if hard_count:
        return 1
    if not unavailable:
        print("OK: no gating or release-surface drift detected")
        return 0
    print("NOTE: one or more assertions were unavailable; the check is incomplete")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
