# Circular display

**English** · [Español](circular-display.es.md)

**Type:** `config`

Swap the square ST7789 240x240 for a round GC9A01 240x240 panel. The firmware
already supports it, so this page is only the delta from the [build
guide](../lila-build-guide.md), which stays the canonical document.

## What's different

| Area | Default | This variation |
| --- | --- | --- |
| Panel | ST7789 240x240, 7-pin module | GC9A01 240x240, round module |
| Configuration | `LILA_DISPLAY=LCD_ST7789_240X240_7PIN` | `LILA_DISPLAY=LCD_GC9A01_240X240` |
| Panel driver | ST7789 branch | the `esp_lcd_new_panel_gc9a01` branch already in the board code |
| Geometry | 240x240, square glass | 240x240, round glass: the corners of the framebuffer sit outside the visible area |
| Case | default bezel | round-screen bezel (geometry pending) |
| Board, wiring, speaker, buttons, LED | — | unchanged |

- The panel choice is already in Kconfig for this board (`LCD_GC9A01_240X240`,
  "GC9A01 240*240 Circle"), the geometry is in `config.h`, and the driver
  branch is in `wk-esp32s3-dev.cc`. No code change and no new branch.
- The wiring does not change: the display connector table in the
  [guide](../lila-build-guide.md#assemble-and-wire) applies as it is. The
  firmware always drives chip-select on GPIO11, so connect a CS wire there if
  your module brings one, and follow the module's own requirement if it does
  not (*not verified* for any specific seller's module).
- The panel is round while the framebuffer stays 240x240: user interface
  drawn in the corners is outside the glass.

## BOM delta

Only two rows of the [shopping list](../lila-build-guide.md#shopping-list)
change; every other part is the default one.

| Part | Specification | Qty | Change |
| --- | --- | --- | --- |
| Display | GC9A01 240x240 round SPI module | 1 | replaces the ST7789 7-pin module |
| Case files | round-screen set: `lila-panel-wk-esp32s3-dev-circular-display.stl` plus the body and lid parts it needs | 1 set | replaces the default bezel geometry — pending, see the [3D-print index](../../STL/README.md) |

Pinouts vary between sellers' modules: the module must expose the SPI
signals of the guide's display wiring table. *not verified*: no specific
round module has been tested.

## Configure

Add one line to `.env` (see [Configure the
build](../lila-build-guide.md#get-the-source-and-configure-env)):

```env
LILA_DISPLAY=LCD_GC9A01_240X240
```

From the repository root, confirm the build picks the panel:

```sh
python scripts/build_lila.py --dry-run
```

The printed command must contain `CONFIG_LCD_GC9A01_240X240=y`. Any `.env`
change requires a new build for it to take effect. Language, wake word,
credentials and the rest of the recipes are unchanged in the [configuration
recipes](../lila-build-guide.md#configuration-recipes).

## Print and assemble

- The round-screen STL set follows the variation naming: its bezel is
  `lila-panel-wk-esp32s3-dev-circular-display.stl`. The geometry is pending,
  so no round-screen case has been printed (*not verified*).
- Assembly follows the guide's checkpointed [assemble and
  wire](../lila-build-guide.md#assemble-and-wire) order: bench test first,
  the wiring tables unchanged, then close the case around the round glass.

## Status and verification

| Check | State |
| --- | --- |
| Panel choice in Kconfig for this board | present (`main/Kconfig.projbuild`) |
| Geometry and driver in the board code | present (`config.h`, `wk-esp32s3-dev.cc`) |
| `.env` selects the panel through `build_lila.py` | verified host-side with `--dry-run` |
| Flash on a real round panel | not verified — needs hardware |
| Round-screen case geometry | pending (the naming slot exists in `STL/README.md`) |

Back to the [chooser](README.md).
