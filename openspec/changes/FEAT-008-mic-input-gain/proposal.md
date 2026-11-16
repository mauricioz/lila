# Change: FEAT-008-mic-input-gain

## Why

A Lila built with the documented INMP441 microphone never reaches the voice
loop. The AFE reports no speech, the wake word never fires and the server
never transcribes a sentence, although the microphone, the amplifier and the
network path are all verified on the bench.

The microphone delivers its 24 bit sample left aligned in a 32 bit I2S slot.
`NoAudioCodec::Read()` converts it with `>> 12`, which keeps 20 bits of the
word and throws away the other 4: exactly the 12 dB that the AFE (running with
`agc_init = false`) and the server ASR were missing. The measured level at the
AFE input was -37 dBFS RMS, below what the detector triggers on.

## What Changes

- The non-PDM read path of `NoAudioCodec` applies the input gain that the
  codec already supports, with the same semantics as the PDM codec: a gain of
  0 or less means no change, and the samples saturate at the `int16` limits.
- `main/Kconfig.projbuild` gains `WK_ESP32S3_DEV_MIC_GAIN`, an integer from 1
  to 16 that defaults to 4.
- The `wk-esp32s3-dev` board applies that value when the codec is created, so
  the documented build needs no extra step and the value can still be
  overridden per build.

## Impact

- Affected capability: microphone capture on the `wk-esp32s3-dev` board.
- Affected code: `main/audio/codecs/no_audio_codec.cc`,
  `main/Kconfig.projbuild`,
  `main/boards/wk-esp32s3-dev/wk-esp32s3-dev.cc`.
- Every other board keeps its behaviour: `AudioCodec::input_gain_` defaults to
  0, so the multiply is skipped.
- No protocol, NVS or build CLI change. The new Kconfig option is the only new
  contract surface and it is additive.
