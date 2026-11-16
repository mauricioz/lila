# microphone-input-gain

## ADDED Requirements

### Requirement: Configurable microphone input gain

The firmware SHALL expose an integer microphone input gain for the
`wk-esp32s3-dev` board, in the range 1 to 16, and SHALL apply it to the
microphone samples before they reach the audio front end. The default SHALL be
4, which restores the 12 dB that the INMP441 loses in the 32 bit I2S slot.

#### Scenario: Documented Lila build

- **WHEN** a Lila is built for `wk-esp32s3-dev` without any extra option
- **THEN** the firmware applies a gain of 4 to the microphone samples
- **AND** the gain can be read in the boot log

#### Scenario: Gain disabled

- **WHEN** a build sets `CONFIG_WK_ESP32S3_DEV_MIC_GAIN=1`
- **THEN** the firmware applies a gain of 1 and the samples keep the level of
  the unamplified conversion

### Requirement: Unchanged behaviour for every other board

The firmware SHALL leave the microphone samples untouched when no input gain
is configured, so that boards other than `wk-esp32s3-dev` keep their current
behaviour.

#### Scenario: Board without a configured gain

- **WHEN** a board that does not call `SetInputGain()` reads microphone samples
- **THEN** the samples are identical to the samples of the previous firmware

### Requirement: Saturated amplification

The firmware SHALL saturate the amplified samples at the `int16` limits
instead of wrapping around.

#### Scenario: Sample above the limit

- **WHEN** an amplified sample is greater than 32767 or lower than -32767
- **THEN** the sample is clamped to the corresponding limit
