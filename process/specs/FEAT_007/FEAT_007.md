# FEAT_007 — Document the verified hardware build

| Field | Value |
| --- | --- |
| ID | FEAT_007 |
| Title | Document the hardware-validated Lila build |
| Owner | @mauricioz |
| Status | in progress |
| Priority | medium |
| Branch | `devs/mauri/docs/hardware-validation` |
| OpenSpec change | none — documentation only, no firmware, Kconfig or build-CLI contract |
| Created | 2026-11-15 |
| Updated | 2026-11-15 |

## Summary

A Lila was assembled from the documented parts and checked on the bench, so the
guide can now state what is verified instead of guessing. The guide also
described the microphone and the amplifier as if they were always on the board,
which is wrong for a build that uses external modules, and it lacked the
failure modes that actually cost the most time. This change records the
verified result, adds the external-module wiring and the troubleshooting rows,
and keeps every unverified item marked as such.

## Motivation

A builder with an external INMP441 and an external MAX98357A had no wiring
tables for them: the guide only covered the on-board microphone and amplifier.
When the speaker stayed silent, the most likely causes (a muted amplifier, a
crossed clock pair, a missing common ground, loose breadboard contacts) were
not written down anywhere. Every fix cost a full debug cycle, and the wake
word model only speaks English, which is also not written down.

## Acceptance criteria

- [x] The guide states, per subsystem, what was verified on a real board and
      what still needs hardware
- [x] External microphone and amplifier wiring tables exist, with the pins
      read from `main/boards/wk-esp32s3-dev/config.h`
- [x] The troubleshooting table covers the audio failure modes found on the
      bench (muted amplifier, 3.3 V supply, crossed clocks, missing common
      ground, unsoldered pins, English-only wake word)
- [x] The English and Spanish guides keep the same sections and the same
      content
- [x] The wake-word phoneme caveat is documented, including that the model
      ships no Spanish voice
- [x] `process/ROADMAP.md` and `CHANGELOG.md` record the change
- [x] `scripts/check_workflow.py` passes (translation parity included)

## Technical blueprint

| Area | Change |
| --- | --- |
| Firmware | none — no code, no Kconfig, no board pin changed |
| Build tooling | none |
| Tests | none — `scripts/check_workflow.py` covers the translation parity |
| Docs | `docs/lila-build-guide.md`, `docs/lila-build-guide.es.md`, `process/ROADMAP.md`, `CHANGELOG.md` |
| CI | none |

### Data and contracts

Documentation only. No protocol, no NVS key, no network payload and no build
contract changes.

### Risks

- Risk: documenting a verified state that later changes → mitigation: the
  status table names the exact board and modules it was measured on
- Risk: the guide drifts into a second hardware profile → mitigation: the
  external modules are described as an alternative to the on-board parts, with
  the same pins, not as a new board

## Scope

**In scope**

- Wiring tables for the external INMP441 and MAX98357A
- A verification-status table for the guide
- Audio troubleshooting rows
- Roadmap and changelog entries

**Out of scope**

- The case geometry and its `STL/` files
- The wake-word phoneme mismatch itself (a configuration choice, not a doc
  change)
- Changing the default wake word or the board pins

## Dependencies

- ESP-IDF `release/v6.1`, board `wk-esp32s3-dev`, ST7789 240x240, INMP441,
  MAX98357A, 8 Ω 0.5 W speaker

## Hardware validation

Already performed on the bench (ESP32-S3 N16R8, INMP441, MAX98357A, ST7789
240x240, 8 Ω 0.5 W speaker):

- [x] Build and flash the Lila configuration
- [x] Boot, activation and MQTT connection
- [x] Display: the face appears and the backlight comes on
- [x] Speaker: the `success.ogg` "ding" is audible at boot
- [x] Microphone: raw PCM captured over UDP, 6.3 s, -37 dBFS RMS, speech
      modulation
- [ ] Wake word: the MultiNet model is English-only; the wake word `lila` is
      phonemised as /liːlə/ ("LEE-luh") and detection is still unproven
- [ ] Server conversation: STT and TTS round trip still unproven
- [ ] TTS voice: chosen in the server console, not in the firmware
- [ ] Case geometry: still being tuned

## Notes

- The microphone proof used the firmware's own audio debugger
  (`CONFIG_USE_AUDIO_DEBUGGER=y`), which streams raw PCM to a UDP listener; the
  capture is a local diagnostic, not a Lila feature.
- The MultiNet model set ships English and Chinese only, so a Spanish wake
  word is always phonemised with English rules. `iris` became /aɪɹəs/
  ("EYE-russ"), which no Spanish speaker says; `lila` becomes /liːlə/
  ("LEE-luh"), which matches "LI-la" almost exactly, so the wake word moved
  to `lila`.
