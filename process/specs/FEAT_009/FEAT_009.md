# FEAT_009 - Animated Lila eyes

| Field | Value |
| --- | --- |
| ID | FEAT_009 |
| Title | Animated Lila eyes |
| Owner | @mauricioz |
| Status | in progress |
| Priority | high |
| Branch | `devs/mauri/feat/FEAT_009-lila-eyes` |
| OpenSpec change | `FEAT-009-lila-eyes` |
| Created | 2026-11-21 |
| Updated | 2026-11-21 |

## Summary

Lila shows a static 64 px emoji above the status bar, so the face is small and
does not move. This change gives the `wk-esp32s3-dev` build a set of 21
animated 240x240 eye emotions drawn for Lila, fills the panel with them and
keeps the status text on top. The eyes are the device identity the family
asked for: long curved lashes, eyeliner wings and a violet iris.

## Motivation

The reference build the family likes animates its eyes: it blinks, looks
around, squints, cries, thinks with sparkles or falls asleep with a `Zz`. Lila
inherited the stock still PNG collection at 64 px, positioned below the status
bar, so the screen reads as a small icon instead of a character.

The repository already compiles the GIF decoder
(`main/display/lvgl_display/gif/lvgl_gif.cc` + `gifdec.c`), and
`emoji_collection.cc` already recognises a GIF collection, so the work is in
the assets, the layout and the build selection:

- the assets partition is 4,194,304 B and currently uses 4,134,597 B, so the
  20 px common font (1,287,460 B) plus 21 GIFs do not fit;
- the classic LCD layout shows the emoji inside a centred box that stays small
  next to the status bar, so a panel-sized animation needs an explicit layout;
- no emoji collection ships inside this repository, so the build tooling
  cannot select Lila's own art yet.

## Acceptance criteria

- [x] The `wk-esp32s3-dev` build packs 21 eye animations in the assets
      partition and stays below 4,194,304 B with at least 100 KB to spare
      (3,915,015 B, 279,289 B free).
- [x] The 21 names match the emotion names the server sends: `angry`,
      `confident`, `confused`, `cool`, `crying`, `delicious`, `embarrassed`,
      `funny`, `happy`, `kissy`, `laughing`, `loving`, `neutral`, `relaxed`,
      `sad`, `shocked`, `silly`, `sleepy`, `surprised`, `thinking`, `winking`.
- [x] In the classic LCD layout a GIF as large as the panel is centred,
      fills the screen and is drawn behind the status text and the battery
      popup; smaller GIFs and PNG collections keep their current position.
- [x] The text font still renders Spanish accents and the status text after
      the move to the 16 px common font.
- [x] Every other board keeps its emoji collection and layout.
- [x] The generator script rebuilds the collection byte for byte from source.
- [x] Documentation updated (`process/ROADMAP.md`, `CHANGELOG.md`, board
      README, `process/specs/FEAT_009/`).
- [ ] Hardware validation is pending: full-screen rendering, colour fidelity
      and animation smoothness on the ST7789 panel.

## Technical blueprint

| Area | Change |
| --- | --- |
| Firmware | `main/display/lcd_display.cc`: `ApplyEmojiLayout()` and its calls from `SetEmotion()`; `main/display/lcd_display.h` |
| Assets | `main/assets/emoji/lila-gif/`: 21 GIFs, `generate_eyes.py`, `README.md` |
| Build tooling | `scripts/build_default_assets.py`: resolve `main/assets/emoji/<name>` before the vendor collections |
| Board selection | `main/CMakeLists.txt`: `wk-esp32s3-dev` uses `lila-gif` and `font_noto_sans_basic_16_4` |
| Tests | `scripts/tests/test_build_default_assets.py`: local collection resolution |
| Docs | `process/ROADMAP.md`, `CHANGELOG.md`, `main/boards/wk-esp32s3-dev/README.md` |
| CI | The existing asset-size guard (`--max_size`) is the regression check |

## Design decisions

- **Feminine identity.** Each eye has four long, curved lashes on the outer
  corner, a tapered eyeliner that ends in a small wing and a violet iris with a
  lilac ring. No vendor art is used and the names are Lila's own.
- **Tiny palette.** Seven colours (black, white, lilac, violet, deep violet,
  pink, tear blue), 26 to 40 frames per loop, 100 ms per frame and 3 to 4 s
  loops. The whole set is 264,428 B.
- **16 px text font.** Keeping the 20 px common font (1,287,460 B) while
  removing the static PNGs (82,540 B) and adding the GIFs (264,428 B) needs
  about 264 KB more than the 59,707 B the partition has free. The 16 px common
  font (885,948 B) keeps antialiasing and the full common charset and leaves
  about 279 KB of headroom.
- **Dynamic layout.** The display decides at runtime from the decoded GIF
  width, so boards with 128 px or 64 px collections are untouched and no new
  Kconfig option is needed.
- **No new MCP surface.** Emotions keep arriving through the existing
  `SetEmotion()` path from the server.

## Out of scope

- The idle screensaver and the embedded screensaver animations.
- Local voice prompts, reminders, alarms, tasks, habits and the wake-only mode.
- Emotion names beyond the 21 the server already uses.

## Risks

- The display panel is 240x240 but the GIF decoder allocates an ARGB8888 frame
  in PSRAM; the board has 8 MB, so memory is not a concern, but a wrong GIF
  size would overflow the layout. The runtime check compares the decoded width
  with `LV_HOR_RES`.
- The 16 px font changes the status text metrics. The status bar uses
  `LV_SIZE_CONTENT`, so it adapts, but the hardware check must confirm that the
  text does not collide with the eyes.
