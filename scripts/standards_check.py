#!/usr/bin/env python3
"""Reference validator for the skill repository standard.

Checks the machine-checkable parts of STANDARD.md. It detects drift in fields,
dates, and boundaries; it never judges whether prose is true.

Usage:
    python3 scripts/standards_check.py [TARGET] [--max-age-days N] [--strict] [--self-test]

Findings carry a severity. A **hard** finding fails the check. A **soft** finding
is advisory: it marks a rule a repository may adopt incrementally, and it does
not change the exit code unless `--strict` is given.

Exit codes follow the local check contract: 0 clean, 1 findings, 2 could not run.
"""

from __future__ import annotations

import argparse
from collections import Counter
import datetime as dt
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

HARD = "hard"
SOFT = "soft"

# A finding is (severity, message). Hard findings fail the check; soft findings
# are advisory and only fail when the check runs in strict mode.
Finding = tuple[str, str]


def hard(message: str) -> Finding:
    """Mark a finding as a hard failure."""
    return (HARD, message)


def soft(message: str) -> Finding:
    """Mark a finding as advisory (does not fail unless strict)."""
    return (SOFT, message)


ALLOWED_STATUSES = ("proposed", "accepted", "deprecated", "superseded", "rejected")
# Accept the common ADR heading shapes, not one exact wording (regex below).
DECISION_HEADING_RE = re.compile(
    r"(?m)^#{2,3}[ \t]+(?P<kind>Decision|ADR[-\s]*\d*|D\d+)\b[:\s\u2014-]*(?P<title>.*?)\s*$"
)
DECISION_ID_RE = re.compile(r"^D\d+$")
RESEARCH_ROW_RE = re.compile(
    r"(?m)^\|\s*(?P<id>R-\d+)\s*\|(?P<concern>[^|]*)\|(?P<status>[^|]*)\|"
    r"(?P<verified>[^|]*)\|(?P<enables>[^|]*)\|"
)
RESEARCH_BODY_RE = re.compile(r"(?m)^##\s+(?P<id>R-\d+)\b")
URL_RE = re.compile(r"https?://[^\s)>\]`'\"]+")
REL_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SPINE_FILES = ("README.md", "SECURITY.md")
# The decision identifier is checked separately because it is a soft rule: a
# repository can record decisions without IDs and still adopt the spine.
DECISION_FIELDS = ("Status", "Decided", "Sources", "Recheck")
APPRAISAL_FIELDS = ("Context", "Evidence appraisal", "Outcome check", "Evidence profile")
EVIDENCE_PROFILES = ("primary", "constrained")
FRONTMATTER_NAME_RE = re.compile(r"(?m)^name:\s*(?P<name>.+?)\s*$")
REVIEWED_RE = re.compile(r"(?m)^Last reviewed:\s*(?P<date>\d{4}-\d{2}-\d{2})")
SCRIPT_REF_RE = re.compile(r"(?:python3|python)\s+(?P<path>[\w./-]+\.py)")


def normalize_url(url: str) -> str:
    """Strip decoration, fragment, and a trailing slash so two spellings match."""
    cleaned = url.strip().strip("<>").rstrip(".,;:'\"")
    cleaned = cleaned.split("#", 1)[0]
    return cleaned.rstrip("/")


def parse_frontmatter_name(text: str) -> str | None:
    """Return the `name` value of a leading YAML frontmatter block, if any."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[4:end]
    match = FRONTMATTER_NAME_RE.search(block)
    if match is None:
        return None
    return match.group("name").strip().strip("'\"")


def _read_path(path: Path) -> str | None:
    """Read UTF-8 text, returning None when the file is missing or unreadable."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def decision_blocks(text: str) -> list[tuple[str, str]]:
    """Split a decision log into (title, block text) pairs."""
    matches = list(DECISION_HEADING_RE.finditer(text))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        stop = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        title = match.group("title").strip() or match.group("kind").strip()
        blocks.append((title, text[start:stop]))
    return blocks


def decision_field(block: str, field: str) -> str | None:
    """Return the value of a `- Field: value` line inside a decision block."""
    match = re.search(
        rf"(?m)^[ \t]*(?:[-*][ \t]*)?(?:\*\*)?{re.escape(field)}(?:\*\*)?:[ \t]*(?P<value>.*)$",
        block,
    )
    if match is None:
        return None
    return match.group("value").strip()


def decision_ids(text: str | None) -> set[str]:
    """Return the decision IDs declared in a decision log."""
    if text is None:
        return set()
    ids: set[str] = set()
    for _title, block in decision_blocks(text):
        value = decision_field(block, "ID")
        if value:
            ids.add(value)
    return ids


def registered_urls(root: Path) -> set[str]:
    """Return the normalized URLs registered in the local evidence index."""
    text = _read_path(root / "docs" / "evidence-urls.json")
    if text is None:
        return set()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return set()
    entries = data.get("urls") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        return set()
    return {
        normalize_url(entry["url"])
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("url"), str)
    }


def registered_source_types(root: Path) -> dict[str, str]:
    """Return the registered source type keyed by normalized URL."""
    text = _read_path(root / "docs" / "evidence-urls.json")
    if text is None:
        return {}
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {}
    entries = data.get("urls") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        return {}
    return {
        normalize_url(entry["url"]): entry["source_type"]
        for entry in entries
        if isinstance(entry, dict)
        and isinstance(entry.get("url"), str)
        and isinstance(entry.get("source_type"), str)
    }


def registered_domain_tags(root: Path) -> set[str]:
    """Return the evidence-registry domain tags declared for source routing."""
    text = _read_path(root / "docs" / "evidence-urls.json")
    if text is None:
        return set()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return set()
    entries = data.get("urls") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        return set()
    return {
        entry["domain_tag"]
        for entry in entries
        if isinstance(entry, dict)
        and isinstance(entry.get("domain_tag"), str)
        and entry["domain_tag"]
    }


def consulting_map_tags(root: Path) -> set[str] | None:
    """Return the domain tags routed by the consultation concern map.

    Returns ``None`` when the repository keeps no consultation guide, so a
    reader can tell "no guide" apart from "a guide with an unrecognised map".
    Only the ``domain_tag`` column of the concern-map table is read, which keeps
    backticked tags in the workflow steps from being mistaken for routes.
    """
    text = _read_path(root / "docs" / "research" / "consulting.md")
    if text is None:
        return None
    column: int | None = None
    in_map = False
    tags: set[str] = set()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            if in_map:
                break
            if "concern map" in stripped.lower():
                in_map = True
                column = None
            continue
        if not in_map or not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if column is None:
            for index, cell in enumerate(cells):
                if "domain_tag" in cell:
                    column = index
                    break
            continue
        if column < len(cells):
            tags.update(re.findall(r"`([a-z][a-z0-9-]*)`", cells[column]))
    return tags


def research_blocks(text: str) -> dict[str, str]:
    """Return each recognised research entry body keyed by its R identifier."""
    matches = list(RESEARCH_BODY_RE.finditer(text))
    return {
        match.group("id"): text[
            match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(text)
        ]
        for index, match in enumerate(matches)
    }


def check_decisions(root: Path) -> list[Finding]:
    """Validate the decision schema, dates, sources, and registration."""
    path = root / "docs" / "decisions.md"
    text = _read_path(path)
    if text is None:
        return []

    findings: list[Finding] = []
    blocks = decision_blocks(text)
    if not blocks:
        findings.append(
            soft(
                "docs/decisions.md has no entries in a recognised shape; the "
                "decision schema and the research-to-decision edge are not "
                "machine-checkable here"
            )
        )

    registered = registered_urls(root)
    source_types = registered_source_types(root)

    for title, block in blocks:
        for field in DECISION_FIELDS:
            value = decision_field(block, field)
            if value is None or not value:
                findings.append(
                    hard(f"decision '{title}' is missing a non-empty {field} field")
                )

        decision_id = decision_field(block, "ID")
        if not decision_id:
            findings.append(
                soft(
                    f"decision '{title}' has no ID "
                    "(an ID is how a research entry enables the decision)"
                )
            )
        elif not DECISION_ID_RE.match(decision_id):
            findings.append(soft(f"decision '{title}' has a malformed ID '{decision_id}'"))

        status = decision_field(block, "Status")
        if status and status not in ALLOWED_STATUSES:
            findings.append(
                hard(
                    f"decision '{title}' has status '{status}' "
                    f"(allowed: {', '.join(ALLOWED_STATUSES)})"
                )
            )

        decided = decision_field(block, "Decided")
        if decided:
            try:
                dt.date.fromisoformat(decided)
            except ValueError:
                findings.append(
                    hard(f"decision '{title}' has a malformed Decided date '{decided}'")
                )

        sources = URL_RE.findall(decision_field(block, "Sources") or "")
        if not sources:
            findings.append(hard(f"decision '{title}' cites no source URL"))
        for url in sources:
            if normalize_url(url) not in registered:
                findings.append(
                    hard(
                        f"decision '{title}' cites an unregistered source '{url}' "
                        "(add it to docs/evidence-urls.json)"
                    )
                )

        profile = decision_field(block, "Evidence profile")
        if profile:
            for field in APPRAISAL_FIELDS:
                if not decision_field(block, field):
                    findings.append(
                        hard(
                            f"decision '{title}' declares an evidence profile but "
                            f"is missing a non-empty {field} field"
                        )
                    )
            if profile not in EVIDENCE_PROFILES:
                findings.append(
                    hard(
                        f"decision '{title}' has evidence profile '{profile}' "
                        f"(allowed: {', '.join(EVIDENCE_PROFILES)})"
                    )
                )
            elif profile == "primary":
                if not any(source_types.get(normalize_url(url)) == "official_docs" for url in sources):
                    findings.append(
                        hard(
                            f"decision '{title}' has evidence profile 'primary' but "
                            "cites no registered official_docs source"
                        )
                    )
            elif not decision_field(block, "Primary-source exception"):
                findings.append(
                    hard(
                        f"decision '{title}' has evidence profile 'constrained' but "
                        "is missing a non-empty Primary-source exception field"
                    )
                )

        if "Rationale:" not in block:
            findings.append(hard(f"decision '{title}' has no Rationale paragraph"))

    declared = [decision_field(block, "ID") for _title, block in blocks]
    present = [value for value in declared if value]
    for decision_id, count in sorted(Counter(present).items()):
        if count > 1:
            findings.append(
                hard(f"docs/decisions.md has duplicate decision ID '{decision_id}'")
            )

    return findings


def check_research(root: Path) -> list[Finding]:
    """Validate the research register and its link to the decision log."""
    path = root / "docs" / "research" / "index.md"
    text = _read_path(path)
    decisions_text = _read_path(root / "docs" / "decisions.md")

    if text is None:
        if decision_blocks(decisions_text or ""):
            return [
                soft(
                    "docs/decisions.md exists but docs/research/index.md is missing "
                    "(the research-to-decision edge is not yet recorded)"
                )
            ]
        return []

    findings: list[Finding] = []
    rows = RESEARCH_ROW_RE.findall(text)
    if not rows:
        if text.strip():
            findings.append(
                soft(
                    "docs/research/index.md has no '| R-### | ... |' rows; the "
                    "research-to-decision edge is not machine-checkable in this shape"
                )
            )
        else:
            findings.append(hard("docs/research/index.md is empty"))
        return findings

    bodies = research_blocks(text)
    known_decisions = decision_ids(decisions_text)
    registered = registered_urls(root)
    seen: set[str] = set()

    for rid, _concern, _status, verified, enables in rows:
        if rid in seen:
            findings.append(hard(f"research id '{rid}' appears more than once"))
        seen.add(rid)
        body = bodies.get(rid)
        if body is None:
            findings.append(hard(f"research '{rid}' has no matching '## {rid}' body section"))
        else:
            sources = URL_RE.findall(body)
            if not sources:
                findings.append(hard(f"research '{rid}' cites no source URL"))
            for url in sources:
                if normalize_url(url) not in registered:
                    findings.append(
                        hard(
                            f"research '{rid}' cites an unregistered source '{url}' "
                            "(add it to docs/evidence-urls.json)"
                        )
                    )
        checked = verified.strip()
        try:
            dt.date.fromisoformat(checked)
        except ValueError:
            findings.append(hard(f"research '{rid}' has a malformed Last Verified '{checked}'"))
        for target in re.findall(r"D\d+", enables):
            if target not in known_decisions:
                findings.append(
                    hard(
                        f"research '{rid}' enables '{target}', which is not a decision id "
                        "declared in docs/decisions.md"
                    )
                )

    enabled = {
        target for _rid, _concern, _status, _verified, enables in rows
        for target in re.findall(r"D\d+", enables)
    }
    for decision_id in sorted(known_decisions):
        if decision_id not in enabled:
            findings.append(
                hard(
                    f"decision '{decision_id}' is not enabled by any research entry "
                    "(append an R-### entry that enables it)"
                )
            )

    return findings


def check_standard(root: Path, today: dt.date, max_age_days: int) -> list[Finding]:
    """Validate the standard document itself and the review cadence."""
    findings: list[Finding] = []

    standard = _read_path(root / "STANDARD.md")
    if standard is not None:
        if "## Normative language" not in standard:
            findings.append(hard("STANDARD.md has no '## Normative language' section"))
        if "## Standard lifecycle" not in standard:
            findings.append(hard("STANDARD.md has no '## Standard lifecycle' section"))
        if not re.search(r"(?m)^\*\*Version ", standard):
            findings.append(hard("STANDARD.md has no '**Version ...**' marker"))

    current = _read_path(root / "docs" / "current-state.md")
    if current is not None:
        match = REVIEWED_RE.search(current)
        if match is None:
            findings.append(hard("docs/current-state.md has no parseable 'Last reviewed:' date"))
        else:
            try:
                reviewed = dt.date.fromisoformat(match.group("date"))
            except ValueError:
                findings.append(hard("docs/current-state.md has a malformed 'Last reviewed:' date"))
            else:
                age = (today - reviewed).days
                if age > max_age_days:
                    findings.append(
                        hard(
                            f"docs/current-state.md was last reviewed {age} days ago "
                            f"(limit {max_age_days}); review the standard"
                        )
                    )

    return findings


def check_evidence_index(root: Path, today: dt.date, max_age_days: int) -> list[Finding]:
    """Validate the evidence index shape and the freshness of each entry."""
    path = root / "docs" / "evidence-urls.json"
    text = _read_path(path)
    if text is None:
        return []

    findings: list[Finding] = []
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return [hard(f"docs/evidence-urls.json is not valid JSON: {exc}")]

    if not isinstance(data, dict):
        return [hard("docs/evidence-urls.json must be a JSON object")]
    if not isinstance(data.get("version"), int):
        findings.append(hard("docs/evidence-urls.json is missing an integer 'version'"))
    if not isinstance(data.get("description"), str) or not data.get("description"):
        findings.append(hard("docs/evidence-urls.json is missing a non-empty 'description'"))

    entries = data.get("urls")
    if not isinstance(entries, list) or not entries:
        findings.append(hard("docs/evidence-urls.json has no 'urls' entries"))
        return findings

    for entry in entries:
        if not isinstance(entry, dict):
            findings.append(hard("docs/evidence-urls.json has a non-object entry"))
            continue
        name = entry.get("name", "<unnamed>")
        if not isinstance(entry.get("url"), str) or not entry.get("url"):
            findings.append(hard(f"evidence '{name}' has no url"))
        statuses = entry.get("expected_statuses")
        if not isinstance(statuses, list) or not statuses or not all(
            isinstance(item, int) for item in statuses
        ):
            findings.append(hard(f"evidence '{name}' has no non-empty integer expected_statuses"))
        verified = entry.get("last_verified")
        if not isinstance(verified, str):
            findings.append(hard(f"evidence '{name}' has no last_verified date"))
            continue
        try:
            asserted = dt.date.fromisoformat(verified)
        except ValueError:
            findings.append(hard(f"evidence '{name}' has a malformed last_verified '{verified}'"))
            continue
        age = (today - asserted).days
        if age > max_age_days:
            findings.append(
                hard(
                    f"evidence '{name}' was last verified {age} days ago "
                    f"(limit {max_age_days}); revalidate or mark it stale"
                )
            )

    return findings


def check_spine(root: Path) -> list[Finding]:
    """Require the spine files and validate the single-skill frontmatter rule."""
    findings: list[Finding] = []
    for name in SPINE_FILES:
        path = root / name
        text = _read_path(path)
        if text is None:
            findings.append(hard(f"missing required spine file '{name}'"))
        elif not text.strip():
            findings.append(hard(f"spine file '{name}' is empty"))

    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return findings

    skill_dirs = sorted(child for child in skills_dir.iterdir() if child.is_dir())
    if not skill_dirs:
        findings.append(hard("skills/ contains no skill directory"))
        return findings

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        text = _read_path(skill_md)
        if text is None:
            findings.append(hard(f"skill '{skill_dir.name}' has no readable SKILL.md"))
            continue

        name = parse_frontmatter_name(text)
        if name is None:
            findings.append(hard(f"skill '{skill_dir.name}' SKILL.md has no frontmatter name"))
        elif name != skill_dir.name:
            findings.append(
                hard(
                    f"skill frontmatter name '{name}' does not match its directory "
                    f"'{skill_dir.name}'"
                )
            )

    return findings


def check_payload_boundary(root: Path) -> list[Finding]:
    """Reject any relative link under skills/ that escapes its own skill directory."""
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return []

    findings: list[Finding] = []
    for skill_dir in sorted(child for child in skills_dir.iterdir() if child.is_dir()):
        for document in sorted(skill_dir.rglob("*.md")):
            text = _read_path(document)
            if text is None:
                continue
            for target in REL_LINK_RE.findall(text):
                candidate = target.strip().split(" ", 1)[0]
                if (
                    candidate.startswith(("http://", "https://", "mailto:", "#", "/"))
                    or not candidate
                ):
                    continue
                resolved = (document.parent / candidate).resolve()
                if not resolved.is_relative_to(skill_dir.resolve()):
                    findings.append(
                        hard(
                            f"{document.relative_to(root)} links outside its skill directory "
                            f"to '{candidate}'"
                        )
                    )
    return findings


def check_consistency(root: Path) -> list[Finding]:
    """Flag a script a hook or workflow runs that the README does not document.

    This detects the drift a shared manifest would also prevent, without
    introducing one: a gate is added to CI or a hook and no reader can see it in
    the documented verification list. Only the executed-but-undocumented
    direction is reported, so a documented command that is deliberately not run
    (for example a network check kept out of the default suite) is not a finding.
    """
    readme = _read_path(root / "README.md")
    if readme is None:
        return []

    executed: list[str] = []
    hooks_dir = root / ".githooks"
    if hooks_dir.is_dir():
        for hook in sorted(child for child in hooks_dir.iterdir() if child.is_file()):
            text = _read_path(hook)
            if text is not None:
                executed.append(text)
    workflows_dir = root / ".github" / "workflows"
    if workflows_dir.is_dir():
        for workflow in sorted(workflows_dir.glob("*.y*ml")):
            text = _read_path(workflow)
            if text is not None:
                executed.append(text)

    if not executed:
        return []

    documented = {match.group("path") for match in SCRIPT_REF_RE.finditer(readme)}
    findings: list[Finding] = []
    seen: set[str] = set()
    for text in executed:
        for path in SCRIPT_REF_RE.findall(text):
            if path in seen or path in documented:
                continue
            seen.add(path)
            findings.append(
                soft(
                    f"a hook or workflow runs '{path}', which no README verification "
                    "block documents"
                )
            )
    return findings


def check_consulting(root: Path) -> list[Finding]:
    """Check that the consultation map routes every declared evidence domain.

    The check is inert for a repository without a consultation guide and for one
    whose evidence index declares no domain tags, so an adopter with neither is
    unaffected. A guide whose map cannot be recognised is advisory for the same
    reason an unrecognised research register is: the shape is missing, not the
    substance.
    """
    tags = consulting_map_tags(root)
    if tags is None:
        return []
    registered = registered_domain_tags(root)
    if not registered:
        return []
    if not tags:
        return [soft("consulting guide has no recognised concern map")]
    findings: list[Finding] = []
    for tag in sorted(registered - tags):
        findings.append(hard(f"consulting map does not route evidence domain {tag!r}"))
    for tag in sorted(tags - registered):
        findings.append(
            soft(
                f"consulting map routes {tag!r}, which the evidence index does not "
                "declare"
            )
        )
    return findings


def check_target(root: Path, today: dt.date, max_age_days: int) -> list[Finding]:
    """Run every check and return the combined findings."""
    findings: list[Finding] = []
    findings += check_spine(root)
    findings += check_standard(root, today, max_age_days)
    findings += check_decisions(root)
    findings += check_research(root)
    findings += check_evidence_index(root, today, max_age_days)
    findings += check_consulting(root)
    findings += check_payload_boundary(root)
    findings += check_consistency(root)
    return findings


def _write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _valid_fixture(root: Path) -> None:
    _write(root, "README.md", "# Fixture\n\nA repository.\n")
    _write(root, "SECURITY.md", "# Security\n\nNothing to report.\n")
    _write(
        root,
        "STANDARD.md",
        "# Fixture standard\n\n"
        "**Version 1 (draft).** A fixture.\n\n"
        "## Normative language\n\nMUST and SHOULD.\n\n"
        "## Standard lifecycle\n\nDraft until two repositories conform.\n",
    )
    _write(
        root,
        "docs/current-state.md",
        "# Current state\n\nLast reviewed: 2026-10-15.\n",
    )
    _write(
        root,
        "docs/evidence-urls.json",
        json.dumps(
            {
                "version": 1,
                "description": "Fixture index.",
                "urls": [
                    {
                        "name": "Example",
                        "url": "https://example.com/docs/",
                        "expected_statuses": [200],
                        "source_type": "official_docs",
                        "last_verified": "2026-10-15",
                    }
                ],
            }
        ),
    )
    _write(
        root,
        "docs/decisions.md",
        "# Decision log\n\n"
        "## Decision: Fixture decision\n\n"
        "- ID: D1\n"
        "- Status: accepted\n"
        "- Decided: 2026-10-15\n"
        "- Sources: https://example.com/docs/\n"
        "- Recheck: never\n\n"
        "Rationale: It is a fixture.\n",
    )
    _write(
        root,
        "docs/research/index.md",
        "# Research record\n\n"
        "| ID | Concern | Status | Last Verified | Enables |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| R-001 | Fixture concern | Complete | 2026-10-15 | D1 |\n\n"
        "## R-001 — Fixture concern\n\nThe fixture. Source: https://example.com/docs/\n",
    )


def run_self_test() -> int:
    """Mutate a valid fixture and assert the checks classify each mutation."""
    today = dt.date(2026, 10, 15)
    base = Path(tempfile.mkdtemp(prefix="standards-check-"))
    cover = base.parent / f"{base.name}-consulting"
    try:
        _valid_fixture(base)
        if check_target(base, today, 180):
            print("FAIL: self-test valid fixture was rejected", file=sys.stderr)
            return 1

        def inspect(relative: str, new_content: str) -> list[Finding]:
            target = base / "mutations"
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(base, target, ignore=shutil.ignore_patterns("mutations"))
            _write(target, relative, new_content)
            return check_target(target, today, 180)

        def assert_hard(label: str, relative: str, new_content: str) -> bool:
            findings = inspect(relative, new_content)
            if not any(severity == HARD for severity, _ in findings):
                print(f"FAIL: self-test did not reject a mutation as hard ({label})", file=sys.stderr)
                return False
            return True

        def assert_soft(label: str, relative: str, new_content: str) -> bool:
            findings = inspect(relative, new_content)
            if not any(severity == SOFT for severity, _ in findings):
                print(f"FAIL: self-test did not flag a soft finding ({label})", file=sys.stderr)
                return False
            return True

        decisions = (base / "docs/decisions.md").read_text(encoding="utf-8")
        if not assert_hard(
            "missing Status field", "docs/decisions.md", decisions.replace("- Status: accepted\n", "")
        ):
            return 1
        if not assert_hard(
            "unknown status",
            "docs/decisions.md",
            decisions.replace("Status: accepted", "Status: maybe"),
        ):
            return 1
        if not assert_hard(
            "unregistered source",
            "docs/decisions.md",
            decisions.replace("https://example.com/docs/", "https://unregistered.example/x"),
        ):
            return 1
        profile_decision = decisions.replace(
            "- Recheck: never\n\n",
            "- Recheck: never\n"
            "- Context: fixture validation\n"
            "- Evidence appraisal: the registered official source is applicable\n"
            "- Outcome check: the fixture stays clean\n"
            "- Evidence profile: primary\n\n",
        )
        if not assert_hard(
            "constrained evidence profile without exception",
            "docs/decisions.md",
            profile_decision.replace("Evidence profile: primary", "Evidence profile: constrained"),
        ):
            return 1
        if not assert_hard(
            "evidence profile missing outcome check",
            "docs/decisions.md",
            profile_decision.replace("- Outcome check: the fixture stays clean\n", ""),
        ):
            return 1

        evidence = (base / "docs/evidence-urls.json").read_text(encoding="utf-8")
        if not assert_hard(
            "stale evidence",
            "docs/evidence-urls.json",
            evidence.replace("2026-10-15", "2000-01-01"),
        ):
            return 1

        # A repository can adopt the spine without decision IDs, but once both
        # records are present in recognised shapes, their relation is an invariant.
        if not assert_soft(
            "decision without an ID",
            "docs/decisions.md",
            decisions.replace("- ID: D1\n", ""),
        ):
            return 1

        research = (base / "docs/research/index.md").read_text(encoding="utf-8")
        if not assert_hard(
            "duplicate research id",
            "docs/research/index.md",
            research.replace(
                "| R-001 | Fixture concern | Complete | 2026-10-15 | D1 |\n",
                "| R-001 | Fixture concern | Complete | 2026-10-15 | D1 |\n"
                "| R-001 | Duplicate | Complete | 2026-10-15 | D1 |\n",
            ),
        ):
            return 1
        if not assert_hard(
            "research enables an unknown decision",
            "docs/research/index.md",
            research.replace("| D1 |", "| D9 |"),
        ):
            return 1
        if not assert_hard(
            "malformed research date",
            "docs/research/index.md",
            research.replace("2026-10-15", "not-a-date"),
        ):
            return 1
        if not assert_hard(
            "decision enabled by no research",
            "docs/research/index.md",
            research.replace("| D1 |", "| |"),
        ):
            return 1
        if not assert_hard(
            "research without a source",
            "docs/research/index.md",
            research.replace("https://example.com/docs/", ""),
        ):
            return 1
        if not assert_hard(
            "research with an unregistered source",
            "docs/research/index.md",
            research.replace("https://example.com/docs/", "https://unregistered.example/x"),
        ):
            return 1
        if not assert_hard(
            "duplicate decision id",
            "docs/decisions.md",
            decisions + "\n## Decision: Duplicate fixture decision\n\n" + decisions.split("## Decision: ", 1)[1],
        ):
            return 1

        standard = (base / "STANDARD.md").read_text(encoding="utf-8")
        if not assert_hard(
            "standard without a lifecycle section",
            "STANDARD.md",
            standard.replace("## Standard lifecycle", "## Lifecycle"),
        ):
            return 1

        current = (base / "docs/current-state.md").read_text(encoding="utf-8")
        if not assert_hard(
            "stale review date",
            "docs/current-state.md",
            current.replace("2026-10-15", "2000-01-01"),
        ):
            return 1

        def assert_no_hard(label: str, relative: str, new_content: str) -> bool:
            findings = inspect(relative, new_content)
            if any(severity == HARD for severity, _ in findings):
                print(
                    f"FAIL: self-test rejected an accepted shape as hard ({label})",
                    file=sys.stderr,
                )
                return False
            return True

        if not assert_no_hard(
            "ADR heading variant",
            "docs/decisions.md",
            decisions.replace("## Decision: Fixture decision", "## ADR-001: Fixture decision"),
        ):
            return 1

        if not assert_soft(
            "research register in another shape",
            "docs/research/index.md",
            "# Research record\n\nA dated field record with no R-### rows.\n",
        ):
            return 1

        # An unrecognised shape is an adoption gap, not a conformance failure.
        if not assert_soft(
            "decisions file in an unrecognised shape",
            "docs/decisions.md",
            "# Decisions\n\n## Methodology over checklist\n\n**Decision:** prose.\n",
        ):
            return 1

        if not assert_soft(
            "gate not documented in the README",
            ".githooks/pre-push",
            "#!/bin/sh\npython3 scripts/undeclared.py\n",
        ):
            return 1

        shutil.copytree(base, cover, ignore=shutil.ignore_patterns("mutations", "multi"))
        _write(
            cover,
            "docs/evidence-urls.json",
            json.dumps(
                {
                    "version": 1,
                    "description": "Fixture index with routed domains.",
                    "urls": [
                        {
                            "name": "Example",
                            "url": "https://example.com/docs/",
                            "expected_statuses": [200],
                            "source_type": "official_docs",
                            "last_verified": "2026-10-15",
                        },
                        {
                            "name": "Alpha",
                            "url": "https://example.com/alpha",
                            "expected_statuses": [200],
                            "domain_tag": "alpha-domain",
                            "source_type": "official_docs",
                            "last_verified": "2026-10-15",
                        },
                        {
                            "name": "Beta",
                            "url": "https://example.com/beta",
                            "expected_statuses": [200],
                            "domain_tag": "beta-domain",
                            "source_type": "official_docs",
                            "last_verified": "2026-10-15",
                        },
                    ],
                }
            ),
        )

        def coverage(map_rows: str) -> list[Finding]:
            _write(
                cover,
                "docs/research/consulting.md",
                "# Research consultation\n\n"
                "## Concern map\n\n"
                "| Concern | `domain_tag` | Read first | Recheck when |\n"
                "| --- | --- | --- | --- |\n"
                + map_rows,
            )
            return check_target(cover, today, 180)

        if any(severity == HARD for severity, _ in coverage(
            "| Alpha | `alpha-domain` | R-001 | never |\n"
            "| Beta | `beta-domain` | R-001 | never |\n"
        )):
            print("FAIL: self-test rejected a fully routed concern map", file=sys.stderr)
            return 1

        missing = coverage("| Alpha | `alpha-domain` | R-001 | never |\n")
        if not any(
            severity == HARD and "beta-domain" in message
            for severity, message in missing
        ):
            print(
                "FAIL: self-test did not reject a concern map that omits a "
                "registered evidence domain",
                file=sys.stderr,
            )
            return 1

        if not any(severity == SOFT for severity, _ in coverage(
            "| Alpha | `alpha-domain` | R-001 | never |\n"
            "| Beta | `beta-domain` | R-001 | never |\n"
            "| Gamma | `gamma-domain` | R-001 | never |\n"
        )):
            print(
                "FAIL: self-test did not flag a concern-map route with no "
                "registered evidence domain",
                file=sys.stderr,
            )
            return 1

        multi = base / "multi"
        if multi.exists():
            shutil.rmtree(multi)
        shutil.copytree(base, multi, ignore=shutil.ignore_patterns("mutations", "multi"))
        _write(multi, "skills/alpha/SKILL.md", "---\nname: alpha\n---\n\nAlpha.\n")
        _write(multi, "skills/beta/SKILL.md", "---\nname: beta\n---\n\nBeta.\n")
        if any(severity == HARD for severity, _ in check_target(multi, today, 180)):
            print("FAIL: self-test rejected a multi-skill payload as hard", file=sys.stderr)
            return 1
    finally:
        shutil.rmtree(base, ignore_errors=True)
        shutil.rmtree(cover, ignore_errors=True)

    print("PASS: standards_check.py self-tests")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check a repository against the standard.")
    parser.add_argument("target", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--max-age-days", type=int, default=180)
    parser.add_argument("--strict", action="store_true", help="treat soft findings as failures")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_test()

    root = Path(args.target).resolve()
    if not root.is_dir():
        print(f"FAIL: target '{root}' is not a directory", file=sys.stderr)
        return 2

    findings = check_target(root, dt.date.today(), args.max_age_days)
    hard_findings = [message for severity, message in findings if severity == HARD]
    soft_findings = [message for severity, message in findings if severity == SOFT]
    for message in hard_findings:
        print(f"FAIL: {message}", file=sys.stderr)
    for message in soft_findings:
        print(f"NOTE: {message}", file=sys.stderr)
    if hard_findings or (args.strict and soft_findings):
        return 1
    if soft_findings:
        print(
            f"OK: repository conforms to the hard rules; "
            f"{len(soft_findings)} advisory finding(s)"
        )
        return 0
    print("OK: repository conforms to the machine-checkable parts of the standard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
