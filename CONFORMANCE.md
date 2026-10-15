# Conformance

- **Grade claimed:** B — spine plus anti-rot core.
- **`STANDARD.md` version:** 1.1 (draft).
- **Checked:** 2026-10-15.
- **Command:** `python3 scripts/standards_check.py`

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
