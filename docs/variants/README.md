# Build variations

**English** · [Español](README.es.md)

The [build guide](../lila-build-guide.md) is the default Lila: the
`wk-esp32s3-dev` board with the ST7789 240x240 screen. This folder documents
the ways to build something else. Every variation page states only what
differs from that guide — what to buy differently, what to configure, and
whether code is needed — in the same five sections, so you can compare the
options here and then follow the guide plus the delta.

## Choose a variation

| Variation | Type | Display | What changes | STL set | Status |
| --- | --- | --- | --- | --- | --- |
| [Circular display](circular-display.md) | `config` | GC9A01 240x240, round | one `.env` line; the bezel geometry | round-screen set (pending) | buildable |
| [Different speaker](speaker.md) | `parts` | unchanged | the speaker you buy | default set | buildable |

**buildable** means everything needed is in this repository today. It does
not mean the variation was built on a device: each page states what still
needs hardware validation, and neither variation has been flashed or printed.

## What the types mean

| Type | The variation needs | Process |
| --- | --- | --- |
| `config` | a `.env` value and its STL set | a documentation pull request; no code |
| `parts` | a different purchase, same firmware | a documentation pull request; no code |
| `variant` | firmware and a release variant of its own | its own `FEAT_XXX` and branch first; the page names it |

No variation of type `variant` exists in the repository today.

## How a variation page is shaped

Every page in this folder follows the same sections, in the same order —
`What's different`, `BOM delta`, `Configure`, `Print and assemble`,
`Status and verification` — declares its type near the top, and links back
to this chooser. `scripts/check_workflow.py` fails a pull request when a
page deviates from that template, when this matrix and the pages disagree,
or when a translation is missing.

When the table above does not apply to you, start from the [default
build](../lila-build-guide.md): the guide is the canonical document and the
pages here only add to it.
