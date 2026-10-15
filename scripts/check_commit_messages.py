#!/usr/bin/env python3
"""Enforce the commit message contract.

Subject:  type[(scope)]: verb — rationale   (em dash before the rationale)
Body:     a `what:` line followed by a `why:` line
Forbidden: a GitHub closing keyword (fix/close/resolve + #N), which would
           auto-close an issue on merge.

Usage:
    python3 scripts/check_commit_messages.py <rev-or-file>
    python3 scripts/check_commit_messages.py --self-test

Exit codes: 0 clean, 1 findings, 2 could not run.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

SUBJECT_RE = re.compile(
    r"^(feat|fix|docs|chore|ci|refactor|test|build|perf|style|revert)"
    r"(\([a-z0-9._/-]+\))?: .+ — .+$"
)
CLOSING_KEYWORD_RE = re.compile(
    r"(?i)\b(close[sd]?|fix(es|ed)?|resolve[sd]?)\b[:\s]*#\d+"
)


def read_message(target: str) -> tuple[str | None, int]:
    """Return (message, exit-code); the message is None when it cannot be read."""
    path = Path(target)
    if path.is_file():
        try:
            return path.read_text(encoding="utf-8"), 0
        except (OSError, UnicodeDecodeError):
            return None, 2
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%B", target],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None, 2
    if result.returncode != 0:
        return None, 2
    return result.stdout, 0


def check_message(message: str) -> list[str]:
    """Return the contract findings for a commit message body."""
    lines = [line for line in message.splitlines() if not line.startswith("#")]
    subject_index = next((i for i, line in enumerate(lines) if line.strip()), None)
    if subject_index is None:
        return ["commit message is empty"]

    errors: list[str] = []
    subject = lines[subject_index].strip()
    if not SUBJECT_RE.match(subject):
        errors.append(
            "subject must be 'type[(scope)]: verb — rationale' with an em dash, "
            f"got '{subject}'"
        )

    body = lines[subject_index + 1 :]
    what_index = next((i for i, line in enumerate(body) if line.strip().startswith("what:")), None)
    why_index = next((i for i, line in enumerate(body) if line.strip().startswith("why:")), None)
    if what_index is None:
        errors.append("body is missing a 'what:' line")
    if why_index is None:
        errors.append("body is missing a 'why:' line")
    if what_index is not None and why_index is not None and what_index > why_index:
        errors.append("'what:' must appear before 'why:'")

    if CLOSING_KEYWORD_RE.search(message):
        errors.append(
            "message contains a GitHub closing keyword (fix/close/resolve + #N), "
            "which would auto-close an issue; use 'Refs #N' instead"
        )

    return errors


def run_self_test() -> int:
    """Assert a valid message passes and each mutation is rejected."""
    valid = (
        "ci: add — enforce the commit contract\n\n"
        "what: check the subject and body of every commit.\n"
        "why: the contract was documented but never enforced.\n"
    )
    if check_message(valid):
        print("FAIL: self-test rejected a valid message", file=sys.stderr)
        return 1

    invalid = {
        "no em dash": "ci: add enforce the commit contract\n\nwhat: x\nwhy: y\n",
        "missing why": "ci: add — enforce\n\nwhat: x\n",
        "what after why": "ci: add — enforce\n\nwhy: y\nwhat: x\n",
        "closing keyword": "ci: add — enforce\n\nwhat: x\nwhy: this fixes #12\n",
    }
    for label, message in invalid.items():
        if not check_message(message):
            print(f"FAIL: self-test accepted an invalid message ({label})", file=sys.stderr)
            return 1

    print("PASS: check_commit_messages.py self-tests")
    return 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_test()
    if len(argv) != 2:
        print("FAIL: expected one argument (a revision or a message file)", file=sys.stderr)
        return 2
    message, code = read_message(argv[1])
    if message is None:
        print(f"FAIL: could not read commit message from '{argv[1]}'", file=sys.stderr)
        return code
    errors = check_message(message)
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    if errors:
        return 1
    print("OK: commit message follows the contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
