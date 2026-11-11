# FEAT_004 — Tasks

Status: done · Owner: @mauricioz · Branch: `devs/mauri/feat/FEAT-004-lila-docs-and-stl`

## 1. Spec and standards

- [x] Write `FEAT_004.md` against the request
- [x] Enrich the blueprint against the real tree (`check_workflow.py`, standards)
- [x] Select standards: `docs` (DOC-1, DOC-2, DOC-16, DOC-17), `python-tooling`
      (PY-12, PY-13, PY-18), `security` (SEC-1, SEC-2), `ci-release` (CI-3)
- [x] Skip OpenSpec: documentation and assets only, no firmware contract

## 2. Implementation

- [x] `README.es.md`: full Spanish translation of `README.md`
- [x] `README.md`: language switcher, build guide and 3D-print section, upstream
      table row for the Spanish page
- [x] `STL/README.md`: index (target hardware, naming convention, print
      settings, expected files)
- [x] `STL/README.es.md`: the Spanish index
- [x] `docs/lila-build-guide.md`: install ESP-IDF (Windows/Linux/macOS), `.env`,
      build, flash, first boot
- [x] `docs/lila-build-guide.es.md`: the Spanish guide
- [x] Print and assembly sections in both guides (STL, settings, wiring order)
- [x] `scripts/check_workflow.py`: `TRANSLATION_PAIRS`, `check_translations()`,
      `STL_MARKERS`, new documents in `check_links()`, `.stl` in `SKIP_SUFFIXES`
- [x] `process/standards/docs.md`: DOC-2 reworded, DOC-16, DOC-17
- [x] `process/README.md` map, `process/ROADMAP.md`, `CHANGELOG.md`
- [x] `main/boards/wk-esp32s3-dev/README.md`: links to the guide and the STL index

## 3. Tests

- [x] Translation pairs exist and cross-link
- [x] A missing Spanish file is reported
- [x] A broken language switcher is reported
- [x] A section mismatch between the languages is reported
- [x] The STL index mentions the board, the panel and the `.stl` extension
- [x] The link check covers the new documents

## 4. Documentation

- [x] `CHANGELOG.md` 0.3.0
- [x] `process/ROADMAP.md` shipped section
- [x] `process/README.md` map

## 5. Verification

- [x] `python -m compileall -q scripts`
- [x] `python scripts/sync_skills.py --check`
- [x] `python scripts/check_workflow.py`
- [x] `python -m unittest discover -s scripts/tests -v` (208 tests; the 12 errors
      are the pre-existing Windows-only failures, unchanged by this branch)
- [x] `python scripts/build_lila.py --dry-run`
- [x] `python scripts/check_format.py --base origin/main` (no C/C++ line changed)

## 6. Review and merge

- [x] `architecture-compliance-check` passed (no firmware touched)
- [x] `code-review-checklist` passed
- [x] Security scan passed (no token, no private URL; `.env` values stay empty)
- [x] PR opened from the feature branch, targeting `mauricioz/lila:main`
- [ ] Geometry committed in `STL/` by the maintainer (the index and the print
      settings are ready; the files themselves are not part of this change)
