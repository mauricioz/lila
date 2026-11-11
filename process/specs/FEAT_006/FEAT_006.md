# FEAT_006 — Document build variations behind one chooser

| Field | Value |
| --- | --- |
| ID | FEAT_006 |
| Title | Add `docs/variants/`: a chooser matrix and template-shaped pages for the circular display and speaker variations |
| Owner | @mauricioz |
| Status | review |
| Priority | medium |
| Branch | `devs/mauri/feat/FEAT-006-variation-docs` |
| OpenSpec change | — (documentation plus a host-side workflow check; no firmware, Kconfig or build-CLI contract) |
| Created | 2026-11-11 |
| Updated | 2026-11-11 |

## Summary

Lila is documented as exactly one machine: the default build guide is
canonical for the `wk-esp32s3-dev` + ST7789 240x240 profile, and there is no
place to record that a builder can choose a round screen or a different
speaker. This change adds `docs/variants/` — a chooser page with one
comparison matrix and one page per variation, every page following the same
fixed section template — and teaches `check_workflow.py` a `check_variants()`
that fails a pull request when a page deviates from the template, when the
matrix and the pages disagree, or when a translation is missing. The default
guide stays the single canonical build and gains a pointer to the chooser.
Text-only: no images, no firmware change.

## Motivation

A variation today would either bloat the build guide with branches most
readers do not need, or live nowhere at all. The repository already contains
three genuinely different kinds of variation, and they need different amounts
of work:

| Variation | What the repository says today | Category |
| --- | --- | --- |
| Circular display | `LCD_GC9A01_240X240` is already in the `DISPLAY_LCD_TYPE` choice for this board (`main/Kconfig.projbuild:846-881`), the geometry exists (`main/boards/wk-esp32s3-dev/config.h:297-310`), the driver branch exists (`wk-esp32s3-dev.cc:380-386`), and `build_lila.py` accepts any `LCD_*` symbol | **config**: one `.env` line, zero code |
| Different speaker | No speaker key exists in `.env.example` or Kconfig; impedance and power are a purchasing decision | **parts**: BOM only, same firmware |
| Battery | No ADC or battery pins in `config.h`, no Kconfig for this board | **variant**: needs firmware and its own FEAT |

The documentation structure must let a reader answer, per variation: *what do
I buy differently, what do I configure differently, and does this need code?*
The answer is a delta model: the default guide keeps the 90 % of the build
that is shared truth, and every variation page documents only what differs,
in an identical shape, so pages are comparable side by side and can be
enforced mechanically.

## Acceptance criteria

- [ ] `docs/variants/README.md` and `docs/variants/README.es.md`: a chooser
      with a comparison matrix (variation, type, display, what changes, STL
      set, status), a legend for the three types (`config` / `parts` /
      `variant`), a link back to the default guide, and a language switcher.
- [ ] The chooser lists **only variations that exist in the repository
      today**: circular display and speaker. No battery row until the battery
      FEAT starts (decision recorded in the spec).
- [ ] `docs/variants/circular-display.md` and `.es.md`: full page — what
      differs (same pins and wiring table, round panel, SPI mode 0, mirror
      X), BOM delta, the exact `LILA_DISPLAY=LCD_GC9A01_240X240` configure
      step verified with `build_lila.py --dry-run`, print/assemble delta, and
      an honest status (code present, hardware not verified).
- [ ] `docs/variants/speaker.md` and `.es.md`: full page — a purchasing
      choice with no configuration change (no speaker key exists), the I2S
      speaker pins from `config.h`, BOM delta, default STL set unless the
      driver does not fit, status.
- [ ] Every variation page follows one fixed template — `## What's
      different`, `## BOM delta`, `## Configure`, `## Print and assemble`,
      `## Status and verification` (Spanish siblings carry the translated
      headings in the same order) — and declares its type in a
      `**Type:**` / `**Tipo:**` line; a `variant` page must name the
      `FEAT_XXX` that implements it.
- [ ] `scripts/check_workflow.py` gains `check_variants()`, registered in
      `run_checks()`, enforcing: the chooser exists, every page has its
      `.es.md` sibling registered in `TRANSLATION_PAIRS`, template headings
      match in order, the matrix links every page and every matrix link
      resolves, and each page links back to the chooser.
- [ ] New tests in `scripts/tests/test_workflow.py` cover the pass case and
      the failure modes (missing sibling, wrong template, unlisted page,
      dead matrix link, unregistered pair, missing type, `variant` type
      without a FEAT reference).
- [ ] The default guide (`docs/lila-build-guide.md` + `.es.md`) gains a
      "choose a variation" pointer near the top; `README.md` / `README.es.md`
      link the chooser.
- [ ] Standards updated: DOC-16 names the new translation pairs, DOC-17
      grows the optional variation dimension in the STL naming
      (`lila-<part>-<board>[-<variation>].stl`), new DOC-18 documents the
      variation template and chooser reciprocity.
- [ ] `process/ROADMAP.md` and `CHANGELOG.md` updated; both language READMEs
      stay in sync.
- [ ] No images or binary assets; no firmware, Kconfig, `build_lila.py` or
      build-CLI change; no secret-shaped string anywhere (SEC-1, SEC-2).

## Technical blueprint

| Area | Change |
| --- | --- |
| Docs | `docs/variants/README.md` + `.es.md`: chooser, matrix, type legend |
| Docs | `docs/variants/circular-display.md` + `.es.md`: config variation page |
| Docs | `docs/variants/speaker.md` + `.es.md`: parts variation page |
| Docs | `docs/lila-build-guide.md` + `.es.md`: one pointer paragraph to the chooser |
| Docs | `README.md`, `README.es.md`: chooser row in the documentation table |
| Docs | `STL/README.md`, `STL/README.es.md`: naming convention gains the optional `<variation>` dimension (DOC-17) |
| Tooling | `scripts/check_workflow.py`: `VARIANT_TEMPLATE_EN` / `VARIANT_TEMPLATE_ES`, `check_variants()`, three new `TRANSLATION_PAIRS` entries, registration in `run_checks()`, success message |
| Tests | `scripts/tests/test_workflow.py`: `VariantTests` class |
| Standards | `process/standards/docs.md`: DOC-16 examples, DOC-17 naming, new DOC-18 |
| Process | `process/ROADMAP.md`, `CHANGELOG.md`, `process/specs/FEAT_006/` |

### The template (enforced, both languages)

1. `## What's different` / `## Qué cambia`
2. `## BOM delta` / `## Cambio en la lista de compra`
3. `## Configure` / `## Configurar`
4. `## Print and assemble` / `## Imprimir y montar`
5. `## Status and verification` / `## Estado y verificación`

A page is `docs/variants/<variation>.md` with sibling
`docs/variants/<variation>.es.md`. The type line sits above the first
section: `**Type:** \`config\`` (EN) / `**Tipo:** \`config\`` (ES), value one
of `config`, `parts`, `variant`.

### Data and contracts

`check_variants(root)` returns problem strings, like every other check:

- `docs/variants/README.md` and `README.es.md` must exist.
- Each `docs/variants/*.md` page (excluding `README.md` and `*.es.md`)
  must have its `.es.md` sibling **and** the pair must be listed in
  `TRANSLATION_PAIRS`, so `check_translations()` applies cross-link and
  section-count parity to it.
- The `##` headings of each file, in order, must equal the language's
  template exactly; a page missing or reordering a section fails.
- The type line must be present and one of the three values; `variant`
  pages must contain a `FEAT_XXX` reference.
- Matrix reciprocity: `README.md` links every EN page, `README.es.md`
  links every ES page, every link in both matrices resolves to an existing
  file, and every page links back to its language's chooser.

No firmware, protocol, Kconfig or build-CLI change; `check_workflow.py` is a
host-side gate that CI already runs, so no workflow edit is needed.

### Risks

- Risk: the pages invent hardware facts (module pinouts, amplifier
  ratings). → mitigation: pins and geometry come from `config.h`, the panel
  choice from `Kconfig.projbuild`, the configure step from `build_lila.py`
  (verified with `--dry-run`); anything a specific seller's module may vary
  is marked *not verified*.
- Risk: the template locks in headings that later need to change. →
  mitigation: the template lives in two constants in one file; changing it
  is a one-line standards + check change reviewed in its own PR.
- Risk: the chooser and the pages drift apart. → mitigation: reciprocity is
  checked mechanically in both directions.
- Risk: Spanish pages fall behind. → mitigation: pairs must be registered
  in `TRANSLATION_PAIRS`, which already fails on missing, unlinked or
  section-mismatched translations.
- Risk: a future battery row promises hardware that does not exist. →
  mitigation: only variations present in the repository appear; the
  `variant` type in the legend explains the category without promising a
  page.

## Scope

**In scope**

- The six variant documents, the two guide pointers, the two README links,
  `check_variants()` and its tests, DOC-16/DOC-17/DOC-18, roadmap,
  changelog and this spec.

**Out of scope**

- The battery variation (excluded by decision until its FEAT starts: no ADC
  pins, no Kconfig, needs firmware and a release variant).
- Any firmware, Kconfig, `.env.example` or `build_lila.py` change.
- STL geometry: the naming convention gains the variation dimension, but no
  new `.stl` file is added (all rows stay *pending*, as today).
- Images or any binary asset.
- A full `docs/` restructure: the default guide stays the single canonical
  build document.
- OpenSpec: documentation plus a host-side check only; no contract of the
  kinds listed in `AGENTS.md` changes.

## Dependencies

- FEAT_004 (merged, `c7839e4`): the translation pairs, `check_translations`
  and `check_stl_index` this change extends.
- FEAT_005 (merged, `89cda30`): the default guide the chooser points back
  to, and its per-connector wiring tables the variation pages reference
  instead of duplicating.

## Hardware validation

Not applicable for the documents themselves. The circular-display configure
step is verified host-side with `build_lila.py --dry-run` (the command must
contain `CONFIG_LCD_GC9A01_240X240=y`). Printing a round-screen case and
flashing either variation still needs real hardware; both pages keep the
*not verified* markers the guide already uses.

## Notes

- Grounded facts used by the pages: `DISPLAY_LCD_TYPE` choice includes
  `LCD_GC9A01_240X240` "GC9A01 240*240 Circle" for
  `BOARD_TYPE_WK_ESP32S3_DEV && WK_ESP32S3_DEV_DISPLAY_LCD`
  (`Kconfig.projbuild:846-881`); GC9A01 geometry is 240x240, mirror X true,
  SPI mode 0, BGR (`config.h:297-310`); the driver branch calls
  `esp_lcd_new_panel_gc9a01` (`wk-esp32s3-dev.cc:380-386`); the LCD pins are
  the `CONFIG_BOARD_NO_MOTOR_CONTROL` defaults (MOSI 8, CLK 9, DC 12, RST
  13, CS 11, backlight 10) shared with every LCD panel; the simplex speaker
  pins are DOUT 21, BCLK 47, LRCK 48 (`config.h:17-19`); no speaker key
  exists anywhere in `.env.example` or Kconfig.
- Matrix columns are variation, type, display, what changes, STL set and
  status. A `power` column was considered and dropped while battery is out
  of scope (it would be a constant USB-C column); it returns with the
  battery FEAT. Status values are `buildable` (everything needed is in the
  repository today) with the legend stating that hardware remains
  unverified.
- STL naming after this change: `lila-<part>-<board>.stl` for the default
  set and `lila-<part>-<board>-<variation>.stl` where `<variation>` is the
  `docs/variants/` page name (e.g. `lila-panel-wk-esp32s3-dev-circular-display.stl`).
