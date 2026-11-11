# FEAT_005 — Upgrade the build, configuration and assembly guide

| Field | Value |
| --- | --- |
| ID | FEAT_005 |
| Title | Rewrite the Lila build guide with a shopping list, configuration recipes and per-connector wiring steps |
| Owner | @mauricioz |
| Status | done |
| Priority | medium |
| Branch | `devs/mauri/feat/FEAT-005-guide-upgrade` |
| OpenSpec change | — (documentation only, no firmware contract) |
| Created | 2026-11-10 |
| Updated | 2026-11-10 |

## Summary

The build guide shipped in FEAT_004 takes a machine from an empty folder to a
working Lila, but it is thin in the three places a builder gets stuck: what
exactly to buy, how to write a `.env` for a common setup without reasoning
about every key, and how to wire and assemble the parts with confidence. This
change rewrites `docs/lila-build-guide.md` and its Spanish sibling in place:
a shopping list (BOM), copy-paste configuration recipes, per-connector wiring
tables, and assembly steps that each end with a verification checkpoint.
Text-only: no images, no new binary assets.

## Motivation

A person building Lila today has to reverse-engineer the parts list from
prose, translate a table of optional keys into their own configuration, and
follow a five-item assembly order with no way to tell whether each step
worked. The guide is the only end-to-end document Lila has, so it is the
right place to fix that. The upgrade is written for the same reader as
before — somebody with no prior ESP-IDF experience — and keeps every existing
section: the ESP-IDF install per OS, the `.env` walkthrough, build, flash,
first boot, print, troubleshooting.

## Acceptance criteria

- [x] A **shopping list** section names every part to buy with its
      specification, quantity and where it goes (board, ST7789 240x240 7-pin
      display, speaker, USB-C data cable, filament), plus the tooling
      (computer, ESP-IDF, printer or print service).
- [x] A **configuration recipes** section provides copy-paste `.env` blocks
      for the common setups: minimal (no credentials), family (Telegram +
      web search), custom wake word, display module with a CS line, and an
      alternate interface language with `python scripts/build.py
      --list-languages` as the authoritative list (verified host-only,
      exit 0).
- [x] The **assembly** section is an ordered set of steps, each with a
      verification checkpoint (what to see in the log, on the screen or at
      the port before moving on), and starts with a bench test before the
      case is closed.
- [x] **Wiring** is split per connector (display, speaker, microphone,
      buttons and LED) with pin, signal and notes, and marks which
      connections the builder makes versus which are already on the board.
- [x] The pin values come from `main/boards/wk-esp32s3-dev/config.h`; no
      hardware fact is invented, and anything not verifiable from the
      repository stays marked as not verified.
- [x] English and Spanish are updated together: same twelve `##` sections,
      cross-linked, commands verbatim — `check_translations()` passes.
- [x] Recipe values are empty or placeholders only; no secret-shaped string
      anywhere (SEC-1, SEC-2).
- [x] No images and no binary assets are added.
- [x] `README.md` and `README.es.md` guide blurbs mention the new content;
      `process/ROADMAP.md` and `CHANGELOG.md` are updated.
- [x] No firmware, Kconfig, build-CLI or `check_workflow.py` change.

## Technical blueprint

| Area | Change |
| --- | --- |
| Docs | `docs/lila-build-guide.md`: `What you need` → `Shopping list`, new `Configuration recipes`, expanded `Assemble and wire` (per-connector tables + checkpointed steps), updated intro TOC |
| Docs | `docs/lila-build-guide.es.md`: the same structure, same twelve `##` sections |
| Docs | `README.md`, `README.es.md`: one-sentence blurb per language |
| Process | `process/ROADMAP.md` (v0.3.0 guide row), `CHANGELOG.md` (0.3.0) |
| Spec | `process/specs/FEAT_005/` (this file + `tasks.md`) |

### Guide section structure (both languages, enforced by `check_translations`)

1. What you need → **Shopping list** (hardware BOM + tools)
2. Install ESP-IDF *(unchanged)*
3. Get the source and configure `.env` *(unchanged)*
4. **Configuration recipes** *(new)*
5. Build the firmware *(unchanged)*
6. Flash the device *(unchanged)*
7. First boot *(unchanged, checkpoint wording tightened)*
8. Print the case *(unchanged)*
9. Assemble and wire *(expanded: bench test first, checkpointed steps,
   per-connector wiring tables)*
10. Check that Lila works *(unchanged)*
11. Troubleshooting *(unchanged)*
12. Where to go next *(unchanged)*

### Data and contracts

No firmware, build, protocol or Kconfig change. `check_workflow.py` already
covers the pair (`TRANSLATION_PAIRS`) and already fails on a section-count
mismatch, so no new check or test is needed; the existing 7 translation/STL
tests enforce this change.

### Risks

- Risk: the upgrade invents hardware facts (voltages, connector types,
  part numbers). → mitigation: every pin comes from `config.h`, every key
  from `.env.example`, every part spec from the existing guide or the board
  README; anything unverifiable stays marked *not verified*.
- Risk: recipes leak a credential. → mitigation: recipe blocks contain only
  empty values and `<token>`-style placeholders, and the secret scan runs
  before the PR.
- Risk: the two languages drift. → mitigation: both files are rewritten in
  the same pass and `check_translations()` fails the PR on a section-count
  mismatch.
- Risk: the section rename breaks inbound anchors. → mitigation: the old
  `#what-you-need` heading is only referenced from the guide's own TOC table,
  which is updated in the same change.

## Scope

**In scope**

- The two guide files, the two README blurbs, roadmap, changelog and spec.

**Out of scope**

- Images, GIFs or any binary asset (explicitly deferred).
- New pages: the overview/status/FAQ content was considered and rejected;
  the guide stays the single end-to-end document.
- `check_workflow.py` or test changes (existing translation parity checks
  already enforce the contract).
- Firmware, `.env.example`, `build_lila.py` or any build-CLI change.

## Dependencies

- FEAT_004 (merged, `c7839e4`): the guide, the translation pair and the
  parity checks this change builds on.

## Hardware validation

Not applicable for the documents. The shopping list, wiring tables and
checkpoints are derived from the repository; the guide keeps stating that
printing and flashing were not executed by the author and still need a real
device.

## Notes

- `python scripts/build.py --list-languages` was run on the host (no
  ESP-IDF): exits 0 and prints 41 locales, so it is safe to document as the
  authoritative locale list.
- The recipes restate the rebuild rule: any `.env` change requires a new
  build for the tools to appear.
