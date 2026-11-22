# display-emotions

## ADDED Requirements

### Requirement: Local emoji collection resolution

The build tooling SHALL resolve an emoji collection name against
`main/assets/emoji/<name>` before the noto-fonts and `otto-gif` vendor
locations, so that a collection shipped inside this repository can be selected
without touching the build CLI.

#### Scenario: Collection shipped in the repository

- **WHEN** the build selects `lila-gif` and
  `main/assets/emoji/lila-gif` contains GIF files
- **THEN** the asset builder packs those files and does not look for
  `lila-gif` in the noto-fonts bundle

#### Scenario: Vendor collection still selected

- **WHEN** the build selects `noto-color-emoji_64` or `otto-gif`
- **THEN** the asset builder resolves the vendor location exactly as before

### Requirement: Full-screen animated emotions

In the classic LCD layout the display SHALL render a GIF whose decoded width
is at least the panel width as a panel-sized image centred on the screen,
behind the status text and the battery popup, and SHALL restore the classic
top-middle position when the image is smaller or still.

#### Scenario: Panel-sized GIF

- **WHEN** `SetEmotion()` loads a GIF whose decoded width is at least
  `LV_HOR_RES`
- **THEN** the image is resized to the panel, centred, moved behind the other
  layers and the chat container stops painting an opaque background

#### Scenario: Small GIF or PNG

- **WHEN** `SetEmotion()` shows a GIF narrower than the panel or a PNG
- **THEN** the image keeps its content size, is aligned to the top middle
  below the status text and the container keeps its background

### Requirement: Unchanged behaviour for other boards

The display SHALL decide the layout from the decoded image size at runtime, so
that boards with their own collection keep their current presentation.

#### Scenario: Board with a 64 px collection

- **WHEN** a board whose emoji collection is 64 px wide shows an emotion
- **THEN** the image is aligned below the status text as before

### Requirement: Text remains legible over the face

The `wk-esp32s3-dev` build SHALL keep a text font that renders the Spanish
accents and the full common charset while leaving headroom in the 4,194,304 B
assets partition.

#### Scenario: Assets fit after the eyes are added

- **WHEN** the `wk-esp32s3-dev` variant builds its assets
- **THEN** the generated `assets.bin` stays below the partition size and keeps
  at least 100 KB free
