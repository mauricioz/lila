# FEAT_004 — Spanish documentation, 3D-print files and a build guide

| Field | Value |
| --- | --- |
| ID | FEAT_004 |
| Title | Ship a Spanish README, an STL folder for the Lila case and a step-by-step build guide in English and Spanish |
| Owner | @mauricioz |
| Status | done |
| Priority | medium |
| Branch | `devs/mauri/feat/FEAT-004-lila-docs-and-stl` |
| OpenSpec change | — (documentation and assets only, no firmware contract) |
| Created | 2026-11-10 |
| Updated | 2026-11-10 |

## Summary

Lila is a Spanish-first family assistant, but its documentation is English only,
there is no place for the 3D-print files of the case, and there is no guide that
takes somebody from an empty machine to a working device. This change adds a
Spanish translation of the front page, a `STL/` folder that indexes the files of
the Lila case, and a step-by-step guide (English and Spanish) covering ESP-IDF
setup, the `.env` build, flashing, printing and assembly.

## Motivation

The people who use Lila are Spanish speakers, and the person who prints the
case needs one place to put the `.stl` files and one document that explains how
to print and assemble them. Today the README is English only, the board README
is Chinese (upstream), and the only build instructions are three commands in
the README. Without this change, a new user has to piece the process together
from the README, the upstream docs and tribal knowledge.

## Acceptance criteria

- [x] `README.es.md` is a complete Spanish translation of `README.md`, and both
      files link to each other through a language switcher.
- [x] The upstream is still credited by link and never copied; the Spanish page
      does not paste upstream documentation either.
- [x] `STL/` exists with an index (`STL/README.md` and `STL/README.es.md`) that
      names the target hardware (`wk-esp32s3-dev` + ST7789 240x240), the file
      naming convention, the print settings and the expected files.
- [x] The guide covers the whole path: installing ESP-IDF on Windows, Linux and
      macOS, configuring `.env`, building, flashing, printing the case and
      assembling it.
- [x] The guide exists in English (`docs/lila-build-guide.md`) and Spanish
      (`docs/lila-build-guide.es.md`), and both link to each other, to the STL
      index and to the front page.
- [x] `scripts/check_workflow.py` fails if a translated document is missing, if
      the language switcher disappears or if the English and Spanish documents
      stop having the same section structure.
- [x] The documentation standard states the translation rule and the rule for
      3D-print files.
- [x] `process/ROADMAP.md`, `CHANGELOG.md`, `process/README.md` and the board
      README are updated.
- [x] No firmware, Kconfig, protocol or build-CLI change.

## Technical blueprint

| Area | Change |
| --- | --- |
| Docs | `README.es.md` (new): full translation, same sections as `README.md` |
| Docs | `README.md`: language switcher, "Build guide and 3D-print case" section, upstream table row for the Spanish page |
| Docs | `docs/lila-build-guide.md`, `docs/lila-build-guide.es.md` (new): ESP-IDF install per OS, `.env`, build, flash, print, assemble, troubleshoot |
| Assets | `STL/README.md`, `STL/README.es.md` (new): index, naming convention, print settings, expected files; the `.stl` files are added by the maintainer |
| Policy | `process/standards/docs.md`: DOC-2 reworded, DOC-16 (translations), DOC-17 (3D-print files) |
| Process | `process/README.md` map, `process/ROADMAP.md` (v0.3.0 shipped section) |
| Checks | `scripts/check_workflow.py`: `TRANSLATION_PAIRS`, `check_translations()`, `STL_MARKERS`, new documents in `check_links()` |
| Tests | `scripts/tests/test_workflow.py`: `TranslationTests`, `StlIndexTests` |
| Changelog | `CHANGELOG.md` 0.3.0 |

### The translation check

`check_translations(root)` walks `TRANSLATION_PAIRS`:

| English | Spanish |
| --- | --- |
| `README.md` | `README.es.md` |
| `docs/lila-build-guide.md` | `docs/lila-build-guide.es.md` |
| `STL/README.md` | `STL/README.es.md` |

For each pair it reports a problem when a file is missing, when the English file
does not link to the Spanish one (or the other way round), or when the two files
do not have the same number of `##` sections. The section count is the cheap
mechanical proxy for "the translation still covers the original".

### Data and contracts

No firmware, build, protocol or Kconfig change. The `.stl` files are binary
assets committed under `STL/`; `check_workflow.py` skips binary files in the
secret scan, and `.stl` is added to `SKIP_SUFFIXES` so a future binary cannot
be read as text.

### Risks

- Risk: the Spanish page drifts from the English one. → mitigation: both files
  must have the same section structure and cross-link, and `check_workflow.py`
  fails when they do not.
- Risk: the guide repeats upstream documentation. → mitigation: the guide links
  to the official ESP-IDF installation pages and the upstream setup guide and
  only documents the Lila specific path.
- Risk: the guide promises a printable case before the `.stl` files exist. →
  mitigation: the guide and the index mark the print step as pending until the
  files are committed and say what is still unverified.
- Risk: the roadmap release numbering shifts. → mitigation: the shift is called
  out in the pull request and needs the maintainer's approval on merge
  (DOC-15).

## Scope

**In scope**

- The Spanish front page, the build guide in both languages, the `STL/` index.
- The documentation standard, the roadmap, the changelog and the mechanical
  checks that keep the translations in place.

**Out of scope**

- The `.stl` geometry itself: the maintainer adds the files, the change adds
  the folder, the index and the print instructions.
- Translating the upstream documentation (still linked, never copied).
- Translating the Chinese upstream board README.

## Dependencies

- None. FEAT_002 and FEAT_003 are merged (`c1d4e09`).

## Hardware validation

Not applicable for the documents. The guide states that printing and flashing
were not executed by the agent and still need a real device.

## Notes

- The guide is written from zero on every OS, but it links to the official
  ESP-IDF installation pages instead of copying them, as required by DOC-2.
- The roadmap gains a `v0.3.0 — Spanish documentation and hardware guide`
  section; the planned quality/automation and product milestones move one
  version later.
