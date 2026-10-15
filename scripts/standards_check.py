#!/usr/bin/env python3
"""Reference validator for the skill repository standard.

Checks the machine-checkable parts of STANDARD.md. It detects drift in fields,
dates, and boundaries; it never judges whether prose is true.

Usage:
    python3 scripts/standards_check.py [TARGET] [--max-age-days N] [--self-test]

Exit codes follow the local check contract: 0 clean, 1 findings, 2 could not run.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ALLOWED_STATUSES = ("proposed", "accepted", "deprecated", "superseded", "rejected")
DECISION_HEADING_RE = re.compile(r"(?m)^## Decision: (?P<title>.+?)\s*$")
DECISION_ID_RE = re.compile(r"^D\d+$")
RESEARCH_ROW_RE = re.compile(
    r"(?m)^\|\s*(?P<id>R-\d+)\s*\|(?P<concern>[^|]*)\|(?P<status>[^|]*)\|"
    r"(?P<verified>[^|]*)\|(?P<enables>[^|]*)\|"
)
RESEARCH_BODY_RE = re.compile(r"(?m)^##\s+(?P<id>R-\d+)\b")
URL_RE = re.compile(r"https?://[^\s)>\]`'\"]+")
REL_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SPINE_FILES = ("README.md", "SECURITY.md")
DECISION_FIELDS = ("ID", "Status", "Decided", "Sources", "Recheck")
FRONTMATTER_NAME_RE = re.compile(r"(?m)^name:\s*(?P<name>.+?)\s*$")
REVIEWED_RE = re.compile(r"(?m)^Last reviewed:\s*(?P<date>\d{4}-\d{2}-\d{2})")


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
        blocks.append((match.group("title"), text[start:stop]))
    return blocks


def decision_field(block: str, field: str) -> str | None:
    """Return the value of a `- Field: value` line inside a decision block."""
    match = re.search(rf"(?m)^-\s*{field}:\s*(?P<value>.*)$", block)
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


def check_decisions(root: Path) -> list[str]:
    """Validate the decision schema, dates, sources, and registration."""
    path = root / "docs" / "decisions.md"
    text = _read_path(path)
    if text is None:
        return []

    errors: list[str] = []
    blocks = decision_blocks(text)
    if not blocks:
        errors.append("docs/decisions.md has no '## Decision:' entries")

    index_path = root / "docs" / "evidence-urls.json"
    registered: set[str] = set()
    index_text = _read_path(index_path)
    if index_text is not None:
        try:
            data = json.loads(index_text)
            entries = data.get("urls") if isinstance(data, dict) else None
            if isinstance(entries, list):
                for entry in entries:
                    if isinstance(entry, dict) and isinstance(entry.get("url"), str):
                        registered.add(normalize_url(entry["url"]))
        except (json.JSONDecodeError, AttributeError):
            pass

    for title, block in blocks:
        for field in DECISION_FIELDS:
            value = decision_field(block, field)
            if value is None or not value:
                errors.append(f"decision '{title}' is missing a non-empty {field} field")

        decision_id = decision_field(block, "ID")
        if decision_id and not DECISION_ID_RE.match(decision_id):
            errors.append(f"decision '{title}' has a malformed ID '{decision_id}'")

        status = decision_field(block, "Status")
        if status and status not in ALLOWED_STATUSES:
            errors.append(
                f"decision '{title}' has status '{status}' "
                f"(allowed: {', '.join(ALLOWED_STATUSES)})"
            )

        decided = decision_field(block, "Decided")
        if decided:
            try:
                dt.date.fromisoformat(decided)
            except ValueError:
                errors.append(f"decision '{title}' has a malformed Decided date '{decided}'")

        sources = URL_RE.findall(decision_field(block, "Sources") or "")
        if not sources:
            errors.append(f"decision '{title}' cites no source URL")
        for url in sources:
            if normalize_url(url) not in registered:
                errors.append(
                    f"decision '{title}' cites an unregistered source '{url}' "
                    "(add it to docs/evidence-urls.json)"
                )

        if "Rationale:" not in block:
            errors.append(f"decision '{title}' has no Rationale paragraph")

    declared = [decision_field(block, "ID") for _title, block in blocks]
    present = [value for value in declared if value]
    if len(present) != len(set(present)):
        errors.append("docs/decisions.md has duplicate decision IDs")

    return errors


def check_research(root: Path) -> list[str]:
    """Validate the research register and its link to the decision log."""
    path = root / "docs" / "research" / "index.md"
    text = _read_path(path)
    decisions_text = _read_path(root / "docs" / "decisions.md")

    if text is None:
        if decision_blocks(decisions_text or ""):
            return [
                "docs/decisions.md exists but docs/research/index.md is missing "
                "(every decision must be enabled by a research entry)"
            ]
        return []

    errors: list[str] = []
    rows = RESEARCH_ROW_RE.findall(text)
    if not rows:
        errors.append("docs/research/index.md has no '| R-### | ... |' rows")
        return errors

    bodies = set(RESEARCH_BODY_RE.findall(text))
    known_decisions = decision_ids(decisions_text)
    seen: set[str] = set()

    for rid, _concern, _status, verified, enables in rows:
        if rid in seen:
            errors.append(f"research id '{rid}' appears more than once")
        seen.add(rid)
        if rid not in bodies:
            errors.append(f"research '{rid}' has no matching '## {rid}' body section")
        checked = verified.strip()
        try:
            dt.date.fromisoformat(checked)
        except ValueError:
            errors.append(f"research '{rid}' has a malformed Last Verified '{checked}'")
        for target in re.findall(r"D\d+", enables):
            if target not in known_decisions:
                errors.append(
                    f"research '{rid}' enables '{target}', which is not a decision id "
                    "declared in docs/decisions.md"
                )

    enabled = {
        target for _rid, _concern, _status, _verified, enables in rows
        for target in re.findall(r"D\d+", enables)
    }
    for decision_id in sorted(known_decisions):
        if decision_id not in enabled:
            errors.append(
                f"decision '{decision_id}' is not enabled by any research entry "
                "(append an R-### entry that enables it)"
            )

    return errors


def check_standard(root: Path, today: dt.date, max_age_days: int) -> list[str]:
    """Validate the standard document itself and the review cadence."""
    errors: list[str] = []

    standard = _read_path(root / "STANDARD.md")
    if standard is not None:
        if "## Normative language" not in standard:
            errors.append("STANDARD.md has no '## Normative language' section")
        if "## Standard lifecycle" not in standard:
            errors.append("STANDARD.md has no '## Standard lifecycle' section")
        if not re.search(r"(?m)^\*\*Version ", standard):
            errors.append("STANDARD.md has no '**Version ...**' marker")

    current = _read_path(root / "docs" / "current-state.md")
    if current is not None:
        match = REVIEWED_RE.search(current)
        if match is None:
            errors.append("docs/current-state.md has no parseable 'Last reviewed:' date")
        else:
            try:
                reviewed = dt.date.fromisoformat(match.group("date"))
            except ValueError:
                errors.append("docs/current-state.md has a malformed 'Last reviewed:' date")
            else:
                age = (today - reviewed).days
                if age > max_age_days:
                    errors.append(
                        f"docs/current-state.md was last reviewed {age} days ago "
                        f"(limit {max_age_days}); review the standard"
                    )

    return errors


def check_evidence_index(root: Path, today: dt.date, max_age_days: int) -> list[str]:
    """Validate the evidence index shape and the freshness of each entry."""
    path = root / "docs" / "evidence-urls.json"
    text = _read_path(path)
    if text is None:
        return []

    errors: list[str] = []
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"docs/evidence-urls.json is not valid JSON: {exc}"]

    if not isinstance(data, dict):
        return ["docs/evidence-urls.json must be a JSON object"]
    if not isinstance(data.get("version"), int):
        errors.append("docs/evidence-urls.json is missing an integer 'version'")
    if not isinstance(data.get("description"), str) or not data.get("description"):
        errors.append("docs/evidence-urls.json is missing a non-empty 'description'")

    entries = data.get("urls")
    if not isinstance(entries, list) or not entries:
        errors.append("docs/evidence-urls.json has no 'urls' entries")
        return errors

    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("docs/evidence-urls.json has a non-object entry")
            continue
        name = entry.get("name", "<unnamed>")
        if not isinstance(entry.get("url"), str) or not entry.get("url"):
            errors.append(f"evidence '{name}' has no url")
        statuses = entry.get("expected_statuses")
        if not isinstance(statuses, list) or not statuses or not all(
            isinstance(item, int) for item in statuses
        ):
            errors.append(f"evidence '{name}' has no non-empty integer expected_statuses")
        verified = entry.get("last_verified")
        if not isinstance(verified, str):
            errors.append(f"evidence '{name}' has no last_verified date")
            continue
        try:
            asserted = dt.date.fromisoformat(verified)
        except ValueError:
            errors.append(f"evidence '{name}' has a malformed last_verified '{verified}'")
            continue
        age = (today - asserted).days
        if age > max_age_days:
            errors.append(
                f"evidence '{name}' was last verified {age} days ago "
                f"(limit {max_age_days}); revalidate or mark it stale"
            )

    return errors


def check_spine(root: Path) -> list[str]:
    """Require the spine files and validate the single-skill frontmatter rule."""
    errors: list[str] = []
    for name in SPINE_FILES:
        path = root / name
        text = _read_path(path)
        if text is None:
            errors.append(f"missing required spine file '{name}'")
        elif not text.strip():
            errors.append(f"spine file '{name}' is empty")

    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return errors

    skill_dirs = sorted(child for child in skills_dir.iterdir() if child.is_dir())
    if len(skill_dirs) != 1:
        errors.append(
            f"skills/ must contain exactly one skill directory, found {len(skill_dirs)}"
        )
        return errors

    skill_dir = skill_dirs[0]
    skill_md = skill_dir / "SKILL.md"
    text = _read_path(skill_md)
    if text is None:
        errors.append(f"skill '{skill_dir.name}' has no readable SKILL.md")
        return errors

    name = parse_frontmatter_name(text)
    if name is None:
        errors.append(f"skill '{skill_dir.name}' SKILL.md has no frontmatter name")
    elif name != skill_dir.name:
        errors.append(
            f"skill frontmatter name '{name}' does not match its directory '{skill_dir.name}'"
        )

    return errors


def check_payload_boundary(root: Path) -> list[str]:
    """Reject any relative link under skills/ that escapes its own skill directory."""
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return []

    errors: list[str] = []
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
                    errors.append(
                        f"{document.relative_to(root)} links outside its skill directory "
                        f"to '{candidate}'"
                    )
    return errors


def check_target(root: Path, today: dt.date, max_age_days: int) -> list[str]:
    """Run every check and return the combined findings."""
    errors: list[str] = []
    errors += check_spine(root)
    errors += check_standard(root, today, max_age_days)
    errors += check_decisions(root)
    errors += check_research(root)
    errors += check_evidence_index(root, today, max_age_days)
    errors += check_payload_boundary(root)
    return errors


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
    """Mutate a valid fixture and assert the checks reject each mutation."""
    today = dt.date(2026, 10, 15)
    base = Path(tempfile.mkdtemp(prefix="standards-check-"))
    try:
        _valid_fixture(base)
        if check_target(base, today, 180):
            print("FAIL: self-test valid fixture was rejected", file=sys.stderr)
            return 1

        mutations: list[tuple[str, str, str | None]] = [
            ("missing Status field", "docs/decisions.md", "Status"),
            ("unknown status", "docs/decisions.md", "Status: accepted"),
            ("unregistered source", "docs/decisions.md", "https://example.com/docs/"),
        ]

        def assert_rejected(label: str, relative: str, new_content: str) -> bool:
            target = base / "mutations"
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(base, target, ignore=shutil.ignore_patterns("mutations"))
            _write(target, relative, new_content)
            findings = check_target(target, today, 180)
            if not findings:
                print(f"FAIL: self-test accepted a mutation ({label})", file=sys.stderr)
                return False
            return True

        decisions = (base / "docs/decisions.md").read_text(encoding="utf-8")
        if not assert_rejected(
            mutations[0][0], "docs/decisions.md", decisions.replace("- Status: accepted\n", "")
        ):
            return 1
        if not assert_rejected(
            mutations[1][0],
            "docs/decisions.md",
            decisions.replace("Status: accepted", "Status: maybe"),
        ):
            return 1
        if not assert_rejected(
            mutations[2][0],
            "docs/decisions.md",
            decisions.replace("https://example.com/docs/", "https://unregistered.example/x"),
        ):
            return 1

        evidence = (base / "docs/evidence-urls.json").read_text(encoding="utf-8")
        if not assert_rejected(
            "stale evidence",
            "docs/evidence-urls.json",
            evidence.replace("2026-10-15", "2000-01-01"),
        ):
            return 1

        if not assert_rejected(
            "decision without an ID",
            "docs/decisions.md",
            decisions.replace("- ID: D1\n", ""),
        ):
            return 1

        research = (base / "docs/research/index.md").read_text(encoding="utf-8")
        if not assert_rejected(
            "duplicate research id",
            "docs/research/index.md",
            research.replace(
                "| R-001 | Fixture concern | Complete | 2026-10-15 | D1 |\n",
                "| R-001 | Fixture concern | Complete | 2026-10-15 | D1 |\n"
                "| R-001 | Duplicate | Complete | 2026-10-15 | D1 |\n",
            ),
        ):
            return 1
        if not assert_rejected(
            "research enables an unknown decision",
            "docs/research/index.md",
            research.replace("| D1 |", "| D9 |"),
        ):
            return 1
        if not assert_rejected(
            "malformed research date",
            "docs/research/index.md",
            research.replace("2026-10-15", "not-a-date"),
        ):
            return 1
        if not assert_rejected(
            "decision enabled by no research",
            "docs/research/index.md",
            research.replace("| D1 |", "| |"),
        ):
            return 1

        standard = (base / "STANDARD.md").read_text(encoding="utf-8")
        if not assert_rejected(
            "standard without a lifecycle section",
            "STANDARD.md",
            standard.replace("## Standard lifecycle", "## Lifecycle"),
        ):
            return 1

        current = (base / "docs/current-state.md").read_text(encoding="utf-8")
        if not assert_rejected(
            "stale review date",
            "docs/current-state.md",
            current.replace("2026-10-15", "2000-01-01"),
        ):
            return 1
    finally:
        shutil.rmtree(base, ignore_errors=True)

    print("PASS: standards_check.py self-tests")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check a repository against the standard.")
    parser.add_argument("target", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--max-age-days", type=int, default=180)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_test()

    root = Path(args.target).resolve()
    if not root.is_dir():
        print(f"FAIL: target '{root}' is not a directory", file=sys.stderr)
        return 2

    errors = check_target(root, dt.date.today(), args.max_age_days)
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    if errors:
        return 1
    print("OK: repository conforms to the machine-checkable parts of the standard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
