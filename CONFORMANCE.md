# Conformance

- **Grade claimed:** B — spine plus anti-rot core.
- **`STANDARD.md` version:** 2.4 (draft).
- **Checked:** 2026-10-16.
- **Command:** `python3 scripts/standards_check.py`
- **Corpus run:** `python3 scripts/check_conformance.py` — 13 of 13 fixtures match
  their expected results.

## Notes

This repository is the standard's home and dogfoods it. It carries the anti-rot
core — an append-only research record, an immutable decision log, a
machine-readable evidence index, a mutable current-state document, and the
change lifecycle — and the reference validator reports no finding when run
against it.

Grade A's payload requirement does not apply: this repository is maintainer
tooling and ships no runtime payload to any agent. The remaining spine items
hold — a single validation entrypoint with a self-test, a `README.md` and a
`SECURITY.md`, the commit contract, and Actions pinned to full commit SHAs.

The repository also ships the conformance corpus, so the grade is checkable
rather than asserted: the corpus proves the validator behaves correctly across
known shapes, and this repository is checked the same way any adopting
repository would be.
