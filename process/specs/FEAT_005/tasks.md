# FEAT_005 — Tasks

Status: done · Owner: @mauricioz · Branch: `devs/mauri/feat/FEAT-005-guide-upgrade`
skill_loaded: true (feature-pipeline, enrich-us, standards-injector)

## 1. Spec and standards

- [x] Write `FEAT_005.md` against the request (one deeper guide, BOM +
      recipes + wiring, checkpointed assembly, text-only)
- [x] Verify facts before documenting: `--list-languages` (41 locales,
      exit 0), `.env.example` keys, `config.h` pin map (incl. the
      `NO_MOTOR_CONTROL` default branch and `DISPLAY_CS_PIN` GPIO11)
- [x] Standards injected: `docs` (DOC-1, DOC-2, DOC-5, DOC-6, DOC-16,
      DOC-17), `security` (SEC-1, SEC-2), `ci-release` (CI-3);
      `python-tooling` N/A (no script change)
- [x] Skip OpenSpec: documentation only, no firmware contract

## 2. Implementation

- [x] `docs/lila-build-guide.md`:
  - [x] `What you need` → `Shopping list` (hardware BOM: spec, qty, where it
        goes; tools table; CS-module note linking the recipe)
  - [x] New `## Configuration recipes`: minimal, family (Telegram + Tavily),
        custom wake word, CS panel, alternate language (+ `--list-languages`),
        advanced (raw overrides + zip)
  - [x] `Assemble and wire`: bench test first, 7 checkpointed steps,
        per-connector tables (display incl. GPIO11 CS note, speaker I2S
        reference, on-board mic/buttons/LED) marked on-board vs user-wired
  - [x] Intro TOC table updated (12 rows, all anchors verified)
  - [x] Troubleshooting: backlight row added, speaker row made precise
- [x] `docs/lila-build-guide.es.md`: same structure, twelve `##` sections,
      commands verbatim, accent-correct anchors
- [x] `README.md` / `README.es.md`: guide blurb mentions shopping list,
      recipes and checkpointed wiring (both languages)
- [x] `process/ROADMAP.md` v0.3.0 guide row, `CHANGELOG.md` 0.3.0 bullet

## 3. Verification

- [x] `python -m compileall -q scripts`
- [x] `python scripts/sync_skills.py --check`
- [x] `python scripts/check_workflow.py` (translation parity, 12/12 sections)
- [x] `python -m unittest discover -s scripts/tests -v` — 208 tests; the 12
      errors are the pre-existing Windows-only failures, unchanged
- [x] `python scripts/build_lila.py --dry-run`
- [x] `python scripts/check_format.py --base origin/main` (no C/C++ change)
- [x] Anchor check: every `](#...)` link in all six linked documents resolves
      to a heading (GitHub slug behaviour confirmed via the contents API:
      non-ASCII letters are kept)

## 4. Review and merge

- [x] `architecture-compliance-check` PASS — no firmware, Kconfig, build CLI
      or script change; docs live in `docs/`, policy in `process/`
- [x] `code-review-checklist` PASS — no secret (recipe values empty or
      placeholders), no upstream copying (DOC-2), relative links inside the
      repo, external links only to official pages
- [x] Secret scan PASS — `check_workflow.py` find_secrets clean; explicit
      grep of the diff for token shapes clean; repo-wide grep for forbidden
      reference words: zero matches
- [ ] PR opened targeting `mauricioz/lila:main` via `scripts/pr.py`
      (last step)
