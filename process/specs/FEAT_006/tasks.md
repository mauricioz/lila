# FEAT_006 — Tasks

Status: done · Owner: @mauricioz · Branch: `devs/mauri/feat/FEAT-006-variation-docs`
skill_loaded: true (feature-pipeline, enrich-us, standards-injector)

## 1. Spec and standards

- [x] Write `FEAT_006.md` against the request (default guide stays
      canonical; `docs/variants/` chooser + template pages; battery excluded
      until its FEAT; bilingual from day one)
- [x] Verify facts before documenting: `DISPLAY_LCD_TYPE` choice includes
      `LCD_GC9A01_240X240` for this board (`Kconfig.projbuild:846-881`),
      GC9A01 geometry (`config.h:297-310`), driver branch
      (`wk-esp32s3-dev.cc:380-386`), `build_lila.py` accepts any `LCD_*`
      symbol, LCD pins from the `NO_MOTOR_CONTROL` defaults, simplex speaker
      pins DOUT 21 / BCLK 47 / LRCK 48, no speaker key in `.env.example` or
      Kconfig
- [x] Standards injected: `docs` (DOC-1, DOC-2, DOC-5, DOC-6, DOC-16, DOC-17
      + new DOC-18), `security` (SEC-1, SEC-2), `ci-release` (CI-1, CI-3),
      `python-tooling` (PY-3, PY-12, PY-13, PY-15, PY-17, PY-18)
- [ ] Skip OpenSpec: documentation plus a host-side workflow check; no
      firmware, Kconfig or build-CLI contract

## 2. Implementation

- [x] `docs/variants/README.md` + `.es.md`: chooser — intro, comparison
      matrix (variation, type, display, what changes, STL set, status),
      type legend (`config` / `parts` / `variant`), link back to the default
      guide, language switcher
- [x] `docs/variants/circular-display.md` + `.es.md`: template page —
      what's different (same wiring, round panel, SPI mode 0, mirror X),
      BOM delta (display row + round-screen STL set), configure
      (`LILA_DISPLAY=LCD_GC9A01_240X240`, verified with `--dry-run`),
      print and assemble (delta only, links the guide's wiring table),
      status (code present, hardware not verified)
- [x] `docs/variants/speaker.md` + `.es.md`: template page — what's
      different (purchasing decision, I2S pins, on-board amp), BOM delta
      (speaker row only), configure (explicitly nothing: no key exists),
      print and assemble (default set unless the driver needs a new bay),
      status (no code to change, hardware not verified)
- [x] `scripts/check_workflow.py`: `VARIANT_TEMPLATE_EN` /
      `VARIANT_TEMPLATE_ES`, `check_variants()`, three new
      `TRANSLATION_PAIRS` entries, registration in `run_checks()`, success
      message mentions variants
- [x] `scripts/tests/test_workflow.py`: `VariantTests` — real-repo pass,
      missing chooser, missing sibling, unregistered pair, wrong template
      order, unlisted page, dead matrix link, missing type line, `variant`
      type without a `FEAT_XXX` reference, cross-language type match,
      orphan Spanish page
- [x] `docs/lila-build-guide.md` + `.es.md`: "choose a variation" pointer
      near the top and a row in *Where to go next*; `README.md` +
      `README.es.md`: chooser row in the documentation table
- [x] `process/standards/docs.md`: DOC-16 examples include the variants
      pairs, DOC-17 naming grows `[-<variation>]`, new DOC-18 (template +
      chooser reciprocity); `STL/README.md` + `.es.md` naming section
      matches DOC-17
- [x] `process/ROADMAP.md` v0.3.0 row, `CHANGELOG.md` 0.3.0 bullets

## 3. Verification

- [x] `python -m compileall -q scripts`
- [x] `python scripts/sync_skills.py --check`
- [x] `python scripts/check_workflow.py`
- [x] `python -m unittest discover -s scripts/tests -v` — 220 tests
      (208 + 12 new `VariantTests`); the 12 errors are the pre-existing
      Windows-only failures, unchanged (test_build, test_ci_selection,
      test_ogg_demuxer, test_startup_wake_word_hint)
- [x] `LILA_DISPLAY=LCD_GC9A01_240X240 python scripts/build_lila.py --dry-run`
      shows `CONFIG_LCD_GC9A01_240X240=y`
- [x] `python scripts/build_lila.py --dry-run` (default, unchanged)
- [x] `python scripts/check_format.py --base origin/main` (clang-format
      23.1.5, no C/C++ change; pinned wheel installed locally)
- [x] Anchor check: every `](#...)` and `file.md#anchor` link in the twelve
      Lila documents resolves; two wrong-depth `../STL/` links found and
      fixed during the check

## 4. Review and merge

- [x] `architecture-compliance-check` PASS — the diff touches no `main/`,
      Kconfig, `.env.example` or build-CLI file; docs live in `docs/`, policy
      in `process/`, host tooling in `scripts/`; `check_variants()` follows
      the established `root -> list[str]` check pattern
- [x] `code-review-checklist` PASS — no secret (only `LILA_DISPLAY` symbol
      values), no upstream copying (DOC-2), fully relative links (zero
      external URLs in the new pages), tests follow fixture → act → assert
      with `encoding="utf-8"`
- [x] Secret scan + forbidden-word scan PASS — `scan_secrets` clean, explicit
      grep of the diff for token shapes: zero, repo-wide grep for forbidden
      reference words: zero matches
- [x] PR opened targeting `mauricioz/lila:main` via `scripts/pr.py` — PR #5
