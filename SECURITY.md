# Security

## What this repository is

`skill-repo-standards` is a **standard and maintainer tooling**. It does not ship
an executable payload to agents. Its scripts run on a maintainer's machine or in
CI, use the Python standard library only, and make no changes outside the files
they are asked to inspect.

## Trust model

- The scripts in `scripts/` are read-only inspectors. They read files, report
  findings, and exit with a status code. They do not install software, mutate
  git state, or write outside a temporary directory.
- No secrets, tokens, or credentials belong in this repository. Do not commit an
  API key, a personal access token, or an SSH private key.
- Nothing here should be executed with elevated privileges.

## Reporting a problem

Report a suspected vulnerability privately to the maintainer rather than in a
public issue. Include the affected file, the command that triggers the problem,
and the observed behaviour.

## Scope

Report issues in the scripts or in the standard's machine-checkable rules.
Questions about how a given repository implements the standard belong to that
repository.
