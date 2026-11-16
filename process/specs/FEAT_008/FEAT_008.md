# FEAT_008 - Compensate the INMP441 input level

| Field | Value |
| --- | --- |
| ID | FEAT_008 |
| Title | Compensate the INMP441 input level |
| Owner | @mauricioz |
| Status | in progress |
| Priority | high |
| Branch | `devs/mauri/fix/FEAT_008-mic-gain` |
| OpenSpec change | `FEAT-008-mic-input-gain` |
| Created | 2026-11-16 |
| Updated | 2026-11-16 |

## Summary

A Lila built with the documented INMP441 microphone never reaches the voice
loop: the AFE reports no speech, the wake word never fires and the server
never transcribes a sentence. The microphone hardware is fine, but the firmware
converts the I2S samples with `>> 12` and therefore hands the voice to the AFE
about 12 dB below the level the detector and the server ASR expect. This
change applies the input gain that the codec already supports to the non-PDM
read path and gives the `wk-esp32s3-dev` board a configurable microphone gain,
4 by default, which restores the missing 12 dB.

## Motivation

The bench evidence, step by step:

- The raw PCM captured over the audio debugger was clean and modulated by
  speech, but at only 466 RMS (about -37 dBFS) with a peak of 2617.
- The AFE runs with `agc_init = false`, so it does not compensate a quiet
  input on its own.
- With the BOOT button the device opened the MQTT audio channel and stayed in
  `listening` for 19.6 s without a single VAD event and without a single
  transcription.
- A vendor firmware for the same board, the same pins, the same codec code and
  the same AFE configuration was flashed on the same device: it reached the
  server too, but the server only answered with its "you went quiet" canned
  lines, because the transcription came back empty. The hardware was therefore
  cleared and the fault was located in the sample conversion.

The INMP441 is a quiet microphone: -26 dBFS sensitivity, so a normal voice at
20-30 cm lands near -20 dBFS in the 32-bit I2S word. The upstream conversion
`bit32_buffer[i] >> 12` keeps 20 bits of that word and discards the other 4,
which is exactly the 12 dB that the AFE and the server were missing.

## Acceptance criteria

- [x] `NoAudioCodec::Read()` applies `input_gain_` to the samples it converts,
      with the same semantics as the PDM codec (`input_gain_ <= 0` means no
      change)
- [x] `CONFIG_WK_ESP32S3_DEV_MIC_GAIN` exists in `main/Kconfig.projbuild`,
      accepts 1 to 16 and defaults to 4
- [x] The `wk-esp32s3-dev` board applies that gain when the codec is created
- [x] Boards that do not set a gain keep their current behaviour
      (`input_gain_` defaults to 0, so the factor is 1)
- [ ] On the real device the voice reaches the AFE at about -25 dBFS RMS
- [ ] On the real device the VAD fires while the user speaks
- [ ] On the real device the wake word `lila` opens a session
- [ ] On the real device the server transcribes a spoken sentence and the
      device answers with the TTS voice
- [x] The English and Spanish guides document the gain and keep the same
      sections
- [x] `process/ROADMAP.md` and `CHANGELOG.md` record the change
- [x] `scripts/check_workflow.py` passes (translation parity included)

## Technical blueprint

| Area | Change |
| --- | --- |
| Firmware | `main/audio/codecs/no_audio_codec.cc`: `NoAudioCodec::Read()` multiplies the converted samples by `input_gain_` (factor 1 when the gain is 0) and saturates at the `int16` limits |
| Kconfig | `main/Kconfig.projbuild`: `WK_ESP32S3_DEV_MIC_GAIN`, `int`, `range 1 16`, `default 4`, `depends on BOARD_TYPE_WK_ESP32S3_DEV` |
| Board | `main/boards/wk-esp32s3-dev/wk-esp32s3-dev.cc`: `InitializeAudioCodec()` calls `GetAudioCodec()->SetInputGain(CONFIG_WK_ESP32S3_DEV_MIC_GAIN)` |
| Build tooling | none - the gain is a Kconfig value, so `LILA_SDKCONFIG` is only needed to override it |
| Tests | none - the change is a scalar multiply in the codec; the host suite covers the repository policy |
| Docs | `docs/lila-build-guide.md`, `docs/lila-build-guide.es.md`, `process/ROADMAP.md`, `CHANGELOG.md` |
| CI | none |

### Data and contracts

- **Kconfig surface**: a new integer option under `BOARD_TYPE_WK_ESP32S3_DEV`.
  The default keeps the documented Lila build working with no extra step, and
  the value can be overridden with `--sdkconfig CONFIG_WK_ESP32S3_DEV_MIC_GAIN=1`
  or the `LILA_SDKCONFIG` escape hatch.
- **No persisted state**: the gain is compiled in, nothing is written to NVS.
- **No protocol change**: the samples keep their format, only their level
  changes.
- **Backward compatibility**: `AudioCodec::input_gain_` defaults to 0, so every
  board that does not call `SetInputGain()` reads the same values as before.

### Risks

- Risk: the gain clips a loud voice → mitigation: at the default of 4 the
  measured peak of 2617 becomes 10468, well inside the `int16` range, and the
  codec saturates instead of wrapping.
- Risk: the change touches a codec shared by many boards → mitigation: the
  multiply is skipped entirely when the gain is 0, which is the default for
  every other board.
- Risk: the wake word still does not fire because the model, not the level, is
  wrong → mitigation: the build is flashed and tested on the device, and the
  guide keeps the wake word marked as not verified until it is proven.

## Scope

**In scope**

- The input gain in the non-PDM read path of `NoAudioCodec`.
- The `WK_ESP32S3_DEV_MIC_GAIN` option and its application by the board.
- The guide and the process documents.

**Out of scope**

- Changing the `>> 12` conversion itself, which would move the level of every
  board that uses `NoAudioCodec`.
- Enabling the AGC in the AFE configuration.
- The wake word model, the server voice and the TTS personality.
- The secret-masking fix in `scripts/build.py` and `scripts/build_lila.py`,
  which is tracked as its own change.

## Dependencies

- ESP-IDF `release/v6.1` (minimum v6.0.1).
- The `wk-esp32s3-dev` board with an external INMP441 on the documented pins.
- A Xiaozhi server account, for the transcription and the TTS check.
- `FEAT_007` documents the bench state this change starts from.

## Hardware validation

What cannot be verified on the host and must be checked on the device:

- [ ] Build and flash the affected variant
- [ ] The samples reach the AFE at about -25 dBFS RMS instead of -37 dBFS
- [ ] The VAD fires while the user speaks
- [ ] The wake word `lila` opens a session
- [ ] The server transcribes a spoken sentence and the device answers
- [ ] The speaker plays the answer without distortion

## Notes

- The bisection used the vendor firmware of the same board as the control: it
  shares the codec code and the AFE configuration with Lila, so it reproduces
  the same fault and proves the hardware is not the cause.
- The gain was measured on the device with a temporary RMS log in
  `NoAudioCodec::Read()`, which is not part of this change. With
  `CONFIG_WK_ESP32S3_DEV_MIC_GAIN=4` a quiet room reads about -27 dBFS RMS
  (peak 4000-8000), and the first seconds after the microphone is enabled
  saturate and then decay, which is the expected settling transient. The same
  room with no gain would sit near -39 dBFS, below the level the detector
  triggers on.
- The guide keeps the wake word, the conversation and the TTS voice marked as
  not verified until the device proves them.
- A 7.5 s turn that ends with `MQTT: Closing audio channel, send_goodbye: 1`
  is a second BOOT press while listening
  (`Application::HandleToggleChatEvent()` closes the channel in that state),
  not a server-side silence timeout.
