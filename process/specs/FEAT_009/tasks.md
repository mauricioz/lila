# FEAT_009 - Tasks

Status: in progress · Owner: @mauricioz · Branch:
`devs/mauri/feat/FEAT_009-lila-eyes`

Each task is one reviewable commit or less. Mark `[x]` only when the code, tests
and docs for that task are in the same commit.

## 1. Spec and standards

- [x] Write `FEAT_009.md` against the current display and asset code
- [x] Record the applicable standards (`process/STANDARDS.md`)
- [x] Create the OpenSpec change `FEAT-009-lila-eyes`

## 2. Assets

- [x] Write the 21-animation generator (`generate_eyes.py`)
- [x] Produce the 21 GIFs in `main/assets/emoji/lila-gif/`
- [x] Document the collection and how to regenerate it (`README.md`)
- [x] Verify the loop lengths, palette and total size

## 3. Implementation

- [x] Resolve `main/assets/emoji/<name>` in
      `build_default_assets.get_emoji_collection_path()`
- [x] Select `lila-gif` and `font_noto_sans_basic_16_4` for `wk-esp32s3-dev`
- [x] Add `LcdDisplay::ApplyEmojiLayout()` and call it from `SetEmotion()`
- [x] Keep the status text and the battery popup above the eyes

## 4. Tests

- [x] Unit test: local collection resolution wins over the vendor paths
- [x] Asset build fits `--max_size` for the Lila board
- [x] Regression: a small GIF or a PNG keeps the classic top-middle layout

## 5. Documentation

- [x] `process/ROADMAP.md`
- [x] `CHANGELOG.md`
- [x] `main/boards/wk-esp32s3-dev/README.md`

## 6. Verification

- [x] `python -m compileall -q scripts`
- [x] `python scripts/sync_skills.py --check`
- [x] `python scripts/check_workflow.py`
- [x] `python -m unittest discover -s scripts/tests -v`
- [x] `python scripts/build_lila.py --dry-run`
- [x] `python scripts/check_format.py --base origin/main`
- [x] Firmware build with ESP-IDF 6.1 and assets partition check

## 7. Hardware (pending)

- [ ] The eyes fill the 240x240 panel behind the status text
- [ ] Colours match the palette (no banding beyond the 7-colour design)
- [ ] The 3-4 s loops play without visible stutter
- [ ] The emotion changes driven by the server update the animation
