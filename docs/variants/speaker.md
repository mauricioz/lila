# Different speaker

**English** · [Español](speaker.es.md)

**Type:** `parts`

Choose a different speaker for Lila: another impedance, more power, or a
driver that fits your case better. This is a purchasing decision — the
firmware, the pins and the configuration stay exactly as the [build
guide](../lila-build-guide.md) describes them.

## What's different

| Area | Default | This variation |
| --- | --- | --- |
| Speaker | 4 Ω, small enclosure speaker | your choice of impedance, power and size |
| Configuration | — | unchanged: no speaker key exists in `.env.example` or Kconfig |
| Firmware | — | unchanged |
| Case | default set sized for the reference speaker | default set, unless the driver does not fit (see below) |
| Display, board, wiring, buttons, LED | — | unchanged |

- The audio path is fixed in hardware: simplex I2S to the on-board
  amplifier, speaker data on GPIO21, bit clock on GPIO47 and word select on
  GPIO48 (`main/boards/wk-esp32s3-dev/config.h`). You choose the driver the
  amplifier drives; nothing in the repository configures it.
- The [shopping list](../lila-build-guide.md#shopping-list) specifies the
  4 Ω reference part. A different driver trades loudness against heat and
  load on the amplifier; the amplifier's rating cannot be verified from this
  repository, so when in doubt keep the reference part (*not verified*: no
  alternative has been measured on a device).

## BOM delta

One row of the [shopping list](../lila-build-guide.md#shopping-list)
changes; every other part is the default one.

| Part | Specification | Qty | Change |
| --- | --- | --- | --- |
| Speaker | your choice of impedance, power and size, within what the on-board amplifier accepts | 1 | replaces the 4 Ω reference speaker |

Physical size matters as much as electrical specs: a driver larger than the
reference part may not fit the case.

## Configure

Nothing. There is no speaker key in `.env.example` and no Kconfig option for
it, so your `.env` stays exactly as the [configuration
recipes](../lila-build-guide.md#configuration-recipes) describe and the same
firmware binary drives the new part. If a firmware option for audio output
ever appears, it will arrive with its own `FEAT_XXX` and this section will
name it.

## Print and assemble

- The default STL set fits the reference speaker, so printing and assembly
  follow the [guide](../lila-build-guide.md#print-the-case) unchanged.
- A physically larger driver needs a bay sized for it. Such geometry follows
  the variation naming — `lila-case-wk-esp32s3-dev-speaker.stl` and its
  siblings — and does not exist yet (*not verified*: nothing has been
  printed).
- Wiring and the assembly checkpoints are the guide's; the speaker connects
  to the board's speaker output exactly as the default part does.

## Status and verification

| Check | State |
| --- | --- |
| Configuration change needed | none — no key exists in `.env.example` or Kconfig |
| Firmware change needed | none |
| Default case fits the reference speaker | the case targets it; the print itself is pending in `STL/README.md` |
| Case fit for other drivers | not verified — no alternative geometry exists |
| Loudness and quality of alternatives | not verified — needs hardware |

Back to the [chooser](README.md).
