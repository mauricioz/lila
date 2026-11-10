# FEAT_002 — Tasks

Status: done · Owner: @mauricioz · Branch: `devs/mauri/chore/lila-workflow`

## 1. Spec and standards

- [x] Write `FEAT_002.md` against the incident
- [x] Select standards: `ci-release` (CI-1a), `docs`, `python-tooling`
- [x] Skip OpenSpec: tooling and policy only, no firmware contract

## 2. Implementation

- [x] `scripts/pr.py` with `check`, `check --pr <n>` and `open`
- [x] Target derived from the `origin` remote; the upstream is refused explicitly
- [x] Git reads trust the checkout (`safe.directory`), so the tool works in the
      ESP-IDF container where the tree is owned by another user
- [x] Token read from `GITHUB_TOKEN`/`GH_TOKEN`, never printed or stored
- [x] `PR target guard` step in `.github/workflows/ci.yml`
- [x] Rule written in `process/WORKFLOW.md`, `process/standards/ci-release.md`,
      `.github/BRANCH_PROTECTION.md`, `.github/PULL_REQUEST_TEMPLATE.md` and
      `AGENTS.md`
- [x] `scripts/check_workflow.py` fails if the rule or the guard disappears
- [x] Skills mention the tool and the target rule

## 3. Tests

- [x] Remote URL parsing (https, ssh, invalid)
- [x] Target validation: upstream refused, missing remote refused, `main` refused
- [x] Payload construction never names the upstream
- [x] `scripts/tests/test_pr.py` → 14 tests

## 4. Documentation

- [x] `process/WORKFLOW.md` — "Where a pull request goes"
- [x] `.github/BRANCH_PROTECTION.md` — target statement
- [x] PR template — target checklist
- [x] `AGENTS.md`, `process/standards/ci-release.md` (CI-1a)
- [x] `CHANGELOG.md`

## 5. Verification

- [x] `python -m compileall -q scripts`
- [x] `python scripts/sync_skills.py --check`
- [x] `python scripts/check_workflow.py`
- [x] `python -m unittest discover -s scripts/tests -v`
- [x] `python scripts/pr.py check` → target `mauricioz/lila:main`

## 6. Review and merge

- [x] `architecture-compliance-check` passed (tooling only)
- [x] `code-review-checklist` passed
- [x] Security scan passed (no token is read from or written to disk)
- [x] PR opened from the feature branch, targeting `mauricioz/lila:main` (PR #1, merged
      as `dca5e89`)
