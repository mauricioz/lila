# FEAT-009-lila-eyes - Tasks

## 1. Assets

- [x] Write `main/assets/emoji/lila-gif/generate_eyes.py`
- [x] Generate the 21 emotion animations (240x240, 7 colours, 3-4 s loops)
- [x] Keep the collection under 300 KB so it fits next to a text font
- [x] Document the design and the regeneration command in the collection
      README

## 2. Build tooling

- [x] Resolve `main/assets/emoji/<name>` before the noto-fonts and `otto-gif`
      collections
- [x] Unit test that a local collection wins over the vendor paths
- [x] Select `lila-gif` and `font_noto_sans_basic_16_4` for
      `CONFIG_BOARD_TYPE_WK_ESP32S3_DEV`

## 3. Display

- [x] Add `LcdDisplay::ApplyEmojiLayout(bool)` for the classic LCD layout
- [x] Treat a GIF whose decoded width is at least `LV_HOR_RES` as full screen
- [x] Called from the GIF, PNG and glyph branches of `SetEmotion()`
- [x] Keep the status text and the battery popup above the animation

## 4. Documentation

- [x] `process/specs/FEAT_009/`
- [x] `process/ROADMAP.md`
- [x] `CHANGELOG.md`
- [x] `main/boards/wk-esp32s3-dev/README.md`

## 5. Verification

- [x] Host checks: `compileall`, `sync_skills --check`, `check_workflow.py`,
      unit tests, `build_lila.py --dry-run`, `check_format.py`
- [x] Firmware build with ESP-IDF 6.1 and the assets partition size guard
- [ ] Hardware: the eyes fill the 240x240 panel behind the status text
- [ ] Hardware: the seven colours render without visible banding
- [ ] Hardware: the 3-4 s loops play without stutter
- [ ] Hardware: a server emotion change switches the animation
