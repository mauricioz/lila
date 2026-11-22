# Change: FEAT-009-lila-eyes

## Why

The Lila build shows a static 64 px emoji below the status bar, while the
device the family wants to match is recognised by its animated eyes. The body
of the interface is already there: the firmware compiles the GIF decoder and
the emoji collection loader accepts GIF files. What is missing is a collection
of Lila's own, a layout that lets a panel-sized animation fill the screen and a
build selection that points the board at the local collection.

## What Changes

- `scripts/build_default_assets.py` resolves an emoji collection name against
  `main/assets/emoji/<name>` before the noto-fonts and `otto-gif` vendor
  locations. A local collection is a normal directory of PNG or GIF files.
- `main/CMakeLists.txt` selects `lila-gif` and
  `font_noto_sans_basic_16_4` for `CONFIG_BOARD_TYPE_WK_ESP32S3_DEV`.
- `LcdDisplay::ApplyEmojiLayout(bool)` renders a GIF whose decoded width is at
  least the panel width as a full-screen image behind the status text, and
  restores the classic top-middle position for smaller or still images.
- `main/assets/emoji/lila-gif/` ships 21 animations, a generator and a README.

## Impact

- Affected capability: display emotions and the build's emoji collection
  resolution.
- Affected code: `main/display/lcd_display.cc`,
  `main/display/lcd_display.h`, `main/CMakeLists.txt`,
  `scripts/build_default_assets.py`.
- Affected assets: the 21 static PNG emotions leave the `wk-esp32s3-dev`
  assets partition and 21 GIFs plus the 16 px common font replace them.
- Every other board keeps its collection, its font and its layout: the display
  decision is taken from the decoded GIF size and the build selection is
  per-board.
- No protocol, NVS or MCP change. The build CLI surface is unchanged; a
  collection name may now refer to a directory inside `main/assets/emoji/`.
