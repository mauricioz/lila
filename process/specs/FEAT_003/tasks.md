# FEAT_003 — Tasks

Status: done · Owner: @mauricioz · Branch: `devs/mauri/chore/lila-workflow`

## 1. Spec and standards

- [x] Write `FEAT_003.md`
- [x] Select standards: `docs` (DOC-1, DOC-2)

## 2. Implementation

- [x] Rewrite `README.md` as a Lila-only front page
- [x] Add the "Upstream project" reference section with links
- [x] Delete `README_zh.md` and `README_ja.md`
- [x] Update `process/standards/docs.md` (DOC-1, DOC-2)
- [x] Update `process/README.md` and `process/ROADMAP.md` wording
- [x] `scripts/check_workflow.py`: required upstream link, forbidden upstream
      body markers, README added to the link check

## 3. Tests

- [x] Link check covers the root README
- [x] README markers are part of `check_workflow.py`

## 4. Documentation

- [x] `CHANGELOG.md` 0.2.0
- [x] Root README links the upstream instead of copying it

## 5. Verification

- [x] `python scripts/check_workflow.py`
- [x] `python -m unittest discover -s scripts/tests -v`

## 6. Review and merge

- [x] `architecture-compliance-check` passed (documentation only)
- [x] `code-review-checklist` passed
- [x] PR opened from the feature branch, targeting `mauricioz/lila:main` (PR #1, merged
      as `dca5e89`)
