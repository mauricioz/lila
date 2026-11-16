# FEAT-008-mic-input-gain - Tasks

## 1. Firmware

- [x] Apply `input_gain_` in `NoAudioCodec::Read()` with `int16` saturation
- [x] Add `WK_ESP32S3_DEV_MIC_GAIN` to `main/Kconfig.projbuild` (1 to 16,
      default 4)
- [x] Apply the gain from the `wk-esp32s3-dev` board

## 2. Documentation

- [x] Document the gain in the English and Spanish build guides
- [x] Record the change in `process/ROADMAP.md` and `CHANGELOG.md`
- [x] Write the feature spec in `process/specs/FEAT_008/`

## 3. Verification

- [x] Host checks: `compileall`, `sync_skills --check`, `check_workflow.py`,
      unit tests, `build_lila.py --dry-run`, `check_format.py`
- [x] Firmware build with ESP-IDF 6.1
- [ ] Hardware: the voice reaches the AFE at about -25 dBFS RMS
- [ ] Hardware: the VAD fires and the wake word `lila` opens a session
- [ ] Hardware: the server transcribes a spoken sentence and the device
      answers
