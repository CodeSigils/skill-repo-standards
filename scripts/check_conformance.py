#!/usr/bin/env python3
"""Run the reference validator across the conformance corpus.

Each directory under ``conformance/fixtures/`` is a miniature repository in a
known shape. ``conformance/expected.json`` records, for every fixture, the exit
code and the exact hard and soft findings the validator must produce. A grade
claim is an assertion until a run evidences it, so this is what makes the claim
checkable rather than merely stated.

Fixture dates are written as ``{{TODAY}}`` and ``{{STALE}}`` and rendered into a
temporary copy at run time, so a checked-in fixture does not rot into failure
once it is older than the freshness window.

Usage: ``python3 scripts/check_conformance.py [--self-test]``
Exit codes follow the local check contract: 0 clean, 1 findings, 2 could not run.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE = ROOT / "conformance"
FIXTURES = CONFORMANCE / "fixtures"
EXPECTED = CONFORMANCE / "expected.json"
VALIDATOR = ROOT / "scripts" / "standards_check.py"
MAX_AGE_DAYS = 180
STALE_DAYS = 400
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt"}


def date_tokens(today: dt.date) -> dict[str, str]:
    """Return the date tokens a fixture may use, rendered for this run."""
    return {
        "{{TODAY}}": today.isoformat(),
        "{{STALE}}": (today - dt.timedelta(days=STALE_DAYS)).isoformat(),
    }


def render(text: str, tokens: dict[str, str]) -> str:
    """Replace every fixture date token in text with its rendered value."""
    for token, value in tokens.items():
        text = text.replace(token, value)
    return text


def materialise(fixture: Path, target: Path, tokens: dict[str, str]) -> None:
    """Copy a fixture to target, rendering date tokens in its text files."""
    shutil.copytree(fixture, target)
    for path in sorted(target.rglob("*")):
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            rendered = render(path.read_text(encoding="utf-8"), tokens)
            path.write_text(rendered, encoding="utf-8")


def parse_findings(stdout: str, stderr: str) -> tuple[list[str], list[str]]:
    """Split validator output into its hard and soft findings."""
    hard: list[str] = []
    soft: list[str] = []
    for line in (stdout + "\n" + stderr).splitlines():
        if line.startswith("FAIL: "):
            hard.append(line[len("FAIL: ") :])
        elif line.startswith("NOTE: "):
            soft.append(line[len("NOTE: ") :])
    return hard, soft


def check_fixture(
    name: str, fixture: Path, expected: dict, tokens: dict[str, str]
) -> list[str]:
    """Run the validator against one fixture; return any mismatches."""
    problems: list[str] = []
    with tempfile.TemporaryDirectory(prefix=f"conformance-{name}-") as tmp:
        target = Path(tmp) / name
        materialise(fixture, target, tokens)
        completed = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                str(target),
                "--max-age-days",
                str(MAX_AGE_DAYS),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    if completed.returncode == 2:
        problems.append(
            f"{name}: the validator could not run (exit 2): {completed.stderr.strip()}"
        )
        return problems

    hard, soft = parse_findings(completed.stdout, completed.stderr)
    if completed.returncode != expected["exit_code"]:
        problems.append(
            f"{name}: exit code {completed.returncode}, expected {expected['exit_code']}"
        )
    for label, actual, wanted in (
        ("hard", hard, expected["hard"]),
        ("soft", soft, expected["soft"]),
    ):
        for message in wanted:
            if message not in actual:
                problems.append(f"{name}: missing {label} finding: {message}")
        for message in actual:
            if message not in wanted:
                problems.append(f"{name}: unexpected {label} finding: {message}")
    return problems


def load_expected(path: Path) -> list[dict]:
    """Return the fixture expectations, or raise when the manifest is unusable."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("conformance/expected.json must be a JSON object")
    fixtures = data.get("fixtures")
    if not isinstance(fixtures, list) or not fixtures:
        raise ValueError("conformance/expected.json has no fixtures")
    return fixtures


def run_self_test() -> int:
    """Check the token rendering and the finding parser offline."""
    tokens = date_tokens(dt.date(2026, 10, 15))
    cases = [
        (render("date: {{TODAY}}", tokens), "date: 2026-10-15"),
        (render("date: {{STALE}}", tokens), "date: 2025-09-10"),
        (parse_findings("", "FAIL: a\nNOTE: b\n"), (["a"], ["b"])),
        (parse_findings("OK: repository conforms\n", ""), ([], [])),
    ]
    for actual, wanted in cases:
        if actual != wanted:
            print(f"FAIL: expected {wanted!r}, got {actual!r}", file=sys.stderr)
            return 1
    print("PASS: check_conformance.py self-tests")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run the conformance corpus.")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv[1:])

    if args.self_test:
        return run_self_test()

    if not VALIDATOR.is_file():
        print(f"FAIL: validator not found at {VALIDATOR}", file=sys.stderr)
        return 2
    if not FIXTURES.is_dir() or not EXPECTED.is_file():
        print("FAIL: the conformance corpus is missing", file=sys.stderr)
        return 2
    try:
        fixtures = load_expected(EXPECTED)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2

    tokens = date_tokens(dt.date.today())
    problems: list[str] = []
    for entry in fixtures:
        name = entry["name"]
        fixture = FIXTURES / name
        if not fixture.is_dir():
            problems.append(f"{name}: fixture directory is missing")
            print(f"FAIL {name}")
            continue
        fixture_problems = check_fixture(name, fixture, entry, tokens)
        if fixture_problems:
            problems.extend(fixture_problems)
            print(f"FAIL {name}")
        else:
            print(f"PASS {name}")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        print("RESULT: the corpus does not match its expected results.", file=sys.stderr)
        return 1

    print(f"RESULT: {len(fixtures)} fixture(s) match their expected results.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
