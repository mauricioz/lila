# FEAT_002 — PR target guard

| Field | Value |
| --- | --- |
| ID | FEAT_002 |
| Title | Make it impossible to open a Lila pull request against the upstream project |
| Owner | @mauricioz |
| Status | done |
| Priority | high |
| Branch | `devs/mauri/chore/lila-workflow` |
| OpenSpec change | — (process/tooling only, no firmware contract) |
| Created | 2026-11-10 |
| Updated | 2026-11-10 |

## Summary

While `mauricioz/lila` was a GitHub fork of `78/xiaozhi-esp32`, a pull request
was opened against the upstream project by mistake (`78/xiaozhi-esp32#2404`,
closed and never merged). The maintainer has since detached the repository from
the fork network, so the upstream is no longer offered as a base by GitHub. This
feature still makes the target explicit and checkable, so a stray pull request
cannot be created by accident in the future.

## Motivation

GitHub's compare page for a fork offered the parent repository in the "base
repository" dropdown, and the link printed by `git push` landed on that page. A
single click created a pull request in the upstream project, which proposed the
whole Lila divergence (branding commits included) to a third-party maintainer.
The mistake was invisible until someone opened the wrong link, and the closed
pull request stays in the upstream's history forever.

Nothing was leaked: upstream `main` stayed at `a73e9a7` and Lila `main` at
`29f249c`. The repository is no longer part of a fork network, which removes the
dropdown trap; the fix is to stop relying on a dropdown at all and to state the
target in every layer of the workflow.

## Acceptance criteria

- [ ] `python scripts/pr.py open` creates a pull request against the repository
      in the `origin` remote and refuses any other target, including
      `78/xiaozhi-esp32`.
- [ ] `python scripts/pr.py check` reports the target and fails when the current
      branch is `main` or the remote is not the Lila repository.
- [ ] `python scripts/pr.py check --pr <n>` verifies that an existing pull
      request targets `mauricioz/lila:main`.
- [ ] CI asserts, on every pull request, that the base repository and base
      branch are the Lila repository and `main`.
- [ ] The rule is written down in `process/WORKFLOW.md`,
      `.github/BRANCH_PROTECTION.md`, the PR template, `AGENTS.md` and the
      CI/release standard.
- [ ] `scripts/check_workflow.py` fails if the rule or the guard disappears.
- [ ] Tests cover slug parsing, branch validation and payload construction
      without touching the network.

## Technical blueprint

| Area | Change |
| --- | --- |
| Tooling | `scripts/pr.py` (`check`, `open`), `scripts/tests/test_pr.py` |
| CI | `ci.yml`: `PR target guard` step on `pull_request` |
| Policy checks | `scripts/check_workflow.py`: required file, markers and rule text |
| Docs | `process/WORKFLOW.md`, `.github/BRANCH_PROTECTION.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `AGENTS.md`, `process/standards/ci-release.md`, `CHANGELOG.md` |
| Skills | `feature-pipeline` mentions the tool and the target rule |

### Data and contracts

`scripts/pr.py` uses only the standard library (`urllib`). The token comes from
`GITHUB_TOKEN` or `GH_TOKEN`; no credential is read from disk and none is
logged. The target repository is derived from `git remote get-url origin`, never
from a user-supplied string, so a mistake cannot be typed in.

### Risks

- Risk: the CI guard cannot see pull requests aimed at another repository,
  because GitHub runs the *base* repository's workflows for those. → mitigation:
  the guard covers the base branch inside Lila, while `scripts/pr.py` and the
  documentation cover the cross-repository case; upstream workflows are not ours
  to run. The repository is detached from the fork network, so GitHub no longer
  offers the upstream as a base.
- Risk: a token in the environment leaks into logs. → mitigation: the script
  never prints the token and reports only status codes and API messages.

## Scope

**In scope**

- The pull-request tool, the CI guard, the policy checks and the documentation.

**Out of scope**

- Any action on the upstream repository: the stray pull request is closed and
  stays closed.
- Upstream synchronisation; Lila tracks upstream by hand.

## Dependencies

- GitHub API access with a token that can create pull requests in `mauricioz/lila`.
- Git with an `origin` remote pointing at the Lila repository.

## Hardware validation

Not applicable: no firmware change.
