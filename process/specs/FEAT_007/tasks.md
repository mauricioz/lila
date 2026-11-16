# FEAT_007 — Tasks

Status: in progress · Owner: @mauricioz · Branch: `devs/mauri/docs/hardware-validation`
skill_loaded: true (feature-pipeline, enrich-us, standards-injector)

## 1. Spec and standards

- [x] Write `FEAT_007.md`: record the bench result, the guide gaps it
      exposed and what stays unverified
- [x] Verify the facts before documenting: pin map from
      `main/boards/wk-esp32s3-dev/config.h`, I2S channel selection from
      `wk-esp32s3-dev.cc` (speaker `I2S_STD_SLOT_RIGHT`, microphone
      `I2S_STD_SLOT_LEFT`), `no_audio_codec.cc` simplex setup, `Kconfig.projbuild`
      debugger symbols
- [x] Standards injected: `docs` (DOC-3, DOC-5, DOC-7, DOC-9, DOC-12, DOC-16),
      `security` (SEC-1, SEC-2)
- [x] Skip OpenSpec: documentation only; no firmware, Kconfig or build-CLI
      contract

## 2. Implementation

- [x] `docs/lila-build-guide.md`: external microphone and amplifier wiring
      tables, external speaker connection, corrected "already on the board"
      notes, verified-status table, audio troubleshooting rows, first-boot
      sounds
- [x] `docs/lila-build-guide.es.md`: the same content in Spanish, with the
      same sections (DOC-16)
- [x] `process/ROADMAP.md`: the hardware validation entry in the shipped
      table (DOC-13, DOC-14)
- [x] `CHANGELOG.md`: the documentation entry (DOC-13)

## 3. Verification

- [x] `python scripts/check_workflow.py` — translation parity and links
- [x] `python -m unittest discover -s scripts/tests -v`
- [x] `python scripts/build_lila.py --dry-run`
- [x] `python scripts/check_format.py --base origin/main`
- [x] Manual read-through of both languages side by side

## 4. Still open

- [ ] Wake word detection with the English MultiNet model — the wake word moved
      from `iris` (/aɪɹəs/, "EYE-russ") to `lila` (/liːlə/, "LEE-luh"); needs a
      live session on the bench
- [ ] Server conversation (STT + TTS) and the TTS voice choice — the voice is
      selected in the server console
- [ ] Case geometry — still being tuned
