#!/usr/bin/env python3
"""Verify the external references registered in docs/evidence-urls.json.

Each entry declares the HTTP statuses it expects and, optionally, text anchors
that must appear in the response body. A changed status or a missing anchor is
drift: the record is stale and must be revalidated.

Usage:
    python3 scripts/verify_urls.py [MANIFEST]
    python3 scripts/verify_urls.py --self-test

The self-test is offline and deterministic. A live run makes network requests
and reports an environmental failure (exit 2) separately from drift (exit 1).

Exit codes: 0 clean, 1 findings, 2 could not run.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

USER_AGENT = "skill-repo-standards-url-verify"
DEFAULT_MANIFEST = Path(__file__).resolve().parents[1] / "docs" / "evidence-urls.json"


def load_manifest(path: Path) -> list[dict[str, Any]]:
    """Return the manifest's url entries, or raise ValueError with a reason."""
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ValueError(f"cannot read manifest {path}: {exc}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"manifest is not valid JSON: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("urls"), list):
        raise ValueError("manifest must be an object with a 'urls' list")
    return data["urls"]


def validate_entry(entry: Any) -> list[str]:
    """Return the shape problems of a single manifest entry."""
    errors: list[str] = []
    if not isinstance(entry, dict):
        return ["entry is not an object"]
    if not isinstance(entry.get("name"), str) or not entry.get("name"):
        errors.append("entry has no name")
    if not isinstance(entry.get("url"), str) or not entry.get("url"):
        errors.append("entry has no url")
    statuses = entry.get("expected_statuses")
    if not isinstance(statuses, list) or not statuses or not all(
        isinstance(item, int) for item in statuses
    ):
        errors.append("entry has no non-empty integer expected_statuses")
    required = entry.get("required_text")
    if required is not None and (
        not isinstance(required, list)
        or not required
        or not all(isinstance(item, str) and item for item in required)
    ):
        errors.append("entry required_text must be a non-empty list of strings")
    return errors


def check_required_text(body: str, required: list[str]) -> str:
    """Return 'ANCHORS_OK' when every anchor is present, else 'MISSING_ANCHOR'."""
    for anchor in required:
        if anchor not in body:
            return "MISSING_ANCHOR"
    return "ANCHORS_OK"


def classify_status(status: int, expected: list[int]) -> str:
    """Return 'OK' when the status is expected, else 'DRIFT'."""
    return "OK" if status in expected else "DRIFT"


def fetch(url: str, required_text: list[str] | None) -> tuple[int, int | str, str | None]:
    """Return (status, content-code, note); a network failure raises URLError."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        status = response.status
        if not required_text:
            return status, 0, None
        body = response.read().decode("utf-8", errors="replace")
        return status, check_required_text(body, required_text), None


def run_live(entries: list[dict[str, Any]]) -> int:
    """Fetch every entry and report drift; distinguish drift from a network failure."""
    drift = False
    network_failure = False
    for entry in entries:
        if entry.get("monitor") is False:
            print(f"SKIP  {entry['name']}")
            continue
        try:
            status, content, _ = fetch(entry["url"], entry.get("required_text"))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            print(f"ERROR {entry['name']}: could not fetch ({exc})", file=sys.stderr)
            network_failure = True
            continue

        expected = entry.get("expected_statuses", [])
        verdict = classify_status(status, expected)
        note = "" if content == 0 else f" content={content}"
        print(f"{verdict:<5} {entry['name']} -> {status}{note}")
        if verdict != "OK" or content not in (0, "ANCHORS_OK"):
            drift = True

    if drift:
        print("RESULT: drift detected; revalidate the manifest entries above.", file=sys.stderr)
        return 1
    if network_failure:
        print("RESULT: some URLs could not be checked (environmental).", file=sys.stderr)
        return 2
    print("RESULT: all URLs match their documented expected state.")
    return 0


def run_self_test() -> int:
    """Offline, deterministic assertions over the parsing and comparison helpers."""
    cases = [
        (check_required_text("hello world", ["world"]), "ANCHORS_OK"),
        (check_required_text("hello", ["world"]), "MISSING_ANCHOR"),
        (classify_status(200, [200]), "OK"),
        (classify_status(404, [200]), "DRIFT"),
    ]
    for observed, expected in cases:
        if observed != expected:
            print(f"FAIL: expected {expected}, observed {observed}", file=sys.stderr)
            return 1

    if validate_entry({"name": "x", "url": "https://e.com", "expected_statuses": [200]}):
        print("FAIL: a valid entry was rejected", file=sys.stderr)
        return 1
    if not validate_entry({"name": "x"}):
        print("FAIL: an incomplete entry was accepted", file=sys.stderr)
        return 1

    print("PASS: verify_urls.py self-tests")
    return 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_test()
    manifest = Path(argv[1]) if len(argv) > 1 else DEFAULT_MANIFEST
    try:
        entries = load_manifest(manifest)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2
    for entry in entries:
        for problem in validate_entry(entry):
            print(f"FAIL: {entry.get('name', '<unnamed>')}: {problem}", file=sys.stderr)
    return run_live(entries)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
