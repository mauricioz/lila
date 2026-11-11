# Build, flash, print and assemble Lila

**English** · [Español](lila-build-guide.es.md)

This guide takes a new machine from an empty folder to a working Lila: the
shopping list, the toolchain, a configured build, the firmware on the board,
the printed case and the wired, assembled assistant. It targets the
`wk-esp32s3-dev` board with the ST7789 240x240 screen — the Lila profile.

The guide was written against the repository, not against a device: the
commands come from the scripts in this repository, but the printing and the
flashing were not executed by the author of these lines. Anything marked
*not verified* needs a real board.

This guide is the default build. A round screen or a different speaker is a
[build variation](variants/README.md): each variation page states only what
differs from this guide, in the same shape, and this guide stays canonical.

| Step | What you get |
| --- | --- |
| [Shopping list](#shopping-list) | every part to buy, with specification and quantity |
| [Install ESP-IDF](#install-esp-idf) | the toolchain that compiles the firmware |
| [Configure the build](#get-the-source-and-configure-env) | a `.env` that describes your Lila |
| [Configuration recipes](#configuration-recipes) | copy-paste `.env` blocks for common setups |
| [Build](#build-the-firmware) | `build/merged-binary.bin` |
| [Flash](#flash-the-device) | Lila running on the board |
| [First boot](#first-boot) | what the log must show |
| [Print](#print-the-case) | the parts of the case |
| [Assemble](#assemble-and-wire) | the wiring tables and the checkpointed assembly steps |
| [Check](#check-that-lila-works) | proof that every subsystem works |
| [Troubleshooting](#troubleshooting) | fixes for the common failures |
| [Where to go next](#where-to-go-next) | the rest of the documentation |

## Shopping list

Everything Lila needs. Sellers and prices vary by region; the specifications
are what matter. The board is the only part the firmware is written for.

### Hardware

| Part | Specification | Qty | Where it goes |
| --- | --- | --- | --- |
| Development board | `wk-esp32s3-dev` (ESP32-S3N16R8: 16 MB flash, 8 MB PSRAM) | 1 | the brain; the board README links the store page |
| Display | ST7789 240x240, 7-pin SPI module: GND, VCC, SCL, SDA, RES, DC, BLK (no CS wire) | 1 | front of the case |
| Speaker | 4 Ω, small enclosure speaker | 1 | inside the case, on the board's speaker output |
| USB-C cable | **data** cable, not charge-only | 1 | power and flashing |
| Filament | PLA or PETG | 1 spool — a case uses a small fraction of it | the case ([print settings](../STL/README.md)) |
| Case files | the `.stl` parts from [`STL/`](../STL/) | 1 set | printed by you or by a print service |

A module with a CS wire also works: it changes one line of configuration
([the recipe](#display-module-with-a-cs-wire)), not the part list.

### Tools

| Item | Detail |
| --- | --- |
| Computer | Windows, Linux or macOS with about 20 GB of free disk |
| Toolchain | ESP-IDF `release/v6.1` (minimum supported: v6.0.1) — installed in the next step |
| Printer | FDM with a 0.4 mm nozzle, 200x200x200 mm or bigger — optional, any print service can print the `.stl` files |
| Hand tools | wire strippers or a soldering iron, depending on how your display module terminates its pins |

The upstream documentation describes the boards and the general setup in
[78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32); this guide only covers
the Lila path.

## Install ESP-IDF

Lila builds with ESP-IDF `release/v6.1`. The official Espressif documentation
has the full instructions — install from it, do not copy it here:

| OS | Official page | Short version |
| --- | --- | --- |
| Windows | [ESP-IDF Tools Installer](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/windows-installer.html) | run the installer, pick ESP32-S3, then open the **ESP-IDF PowerShell** shortcut it creates |
| Linux | [Linux setup](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/linux.html) | install the prerequisites, then run the script below |
| macOS | [macOS setup](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/macos.html) | install the prerequisites, then run the script below |

On Linux and macOS:

```bash
git clone -b release/v6.1 --recursive https://github.com/espressif/esp-idf.git ~/esp-idf
cd ~/esp-idf
./install.sh esp32s3
```

Every new terminal needs the environment loaded:

```bash
. ~/esp-idf/export.sh          # Linux and macOS
```

```powershell
C:\Espressif\frameworks\esp-idf-v6.1\export.ps1   # Windows PowerShell
```

Check it before going further:

```bash
idf.py --version
```

The VS Code extension is optional; every command in this guide works from a
plain terminal. See the
[official page](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/vscode-config.html).

## Get the source and configure `.env`

```bash
git clone https://github.com/mauricioz/lila.git
cd lila
cp .env.example .env
```

```powershell
git clone https://github.com/mauricioz/lila.git
cd lila
Copy-Item .env.example .env
```

Open `.env` in any text editor. Every value is optional; the defaults already
describe a Spanish Lila with the `lila` wake word and a 7-pin ST7789 screen:

| Key | Default | Change it when |
| --- | --- | --- |
| `LILA_BOARD` | `wk-esp32s3-dev` | you build another board |
| `LILA_NAME` | `wk-esp32s3-dev` | you build another variant; it is also the OTA board identity |
| `LILA_LANGUAGE` | `es-ES` | you want another interface language |
| `LILA_WAKE_WORD` | `custom:lila` | you want a different word, a WakeNet model, or `disabled` |
| `LILA_DISPLAY` | `LCD_ST7789_240X240_7PIN` | your module has a CS line: use `LCD_ST7789_240X240` |
| `LILA_TAVILY_API_KEY` | *(empty)* | you want the `web.search` tool; get a key at [tavily.com](https://tavily.com) |
| `LILA_TELEGRAM_BOT_TOKEN` | *(empty)* | you want the `self.telegram.send` tool; create the bot with [@BotFather](https://t.me/BotFather) |
| `LILA_TELEGRAM_CHAT_ID` | *(empty)* | you use the Telegram tool; read the id from `https://api.telegram.org/bot<token>/getUpdates` |
| `LILA_SDKCONFIG` | *(empty)* | you need a raw `CONFIG_KEY=VALUE` override |
| `LILA_ZIP` | `0` | set it to `1` to also package `releases/*.zip` |

`.env` holds your credentials, so it is git-ignored: never copy it into an
issue, a pull request or a screenshot. The keys stay empty in
`.env.example` on purpose.

The wake word `custom:lila` is a MultiNet custom command. It only works on
ESP32-S3, S31 and P4 targets, and it makes the build include the English
MultiNet 7 quantized model in the assets partition.

## Configuration recipes

The table above explains every key on its own. These are complete `.env`
contents for the setups that come up most often: pick the closest one, copy
it over your `.env`, adjust, and rebuild — every change to `.env` needs a new
build before it reaches the device.

### Minimal — no credentials

```bash
# Stock Lila: Spanish interface, wake word "lila", 7-pin ST7789, no optional tools.
LILA_BOARD=wk-esp32s3-dev
LILA_NAME=wk-esp32s3-dev
LILA_LANGUAGE=es-ES
LILA_WAKE_WORD=custom:lila
LILA_DISPLAY=LCD_ST7789_240X240_7PIN
```

### Family — Telegram and web search

```bash
# Everything from Minimal, plus the two optional tools:
LILA_TAVILY_API_KEY=               # key from https://tavily.com
LILA_TELEGRAM_BOT_TOKEN=           # token from @BotFather
LILA_TELEGRAM_CHAT_ID=             # your chat id
```

Leave a key empty and the matching tool simply does not exist in the build —
that is the designed behaviour, not an error. Fill the values in your own
`.env`; never commit them.

### Another wake word

```bash
# a different custom command (MultiNet; ESP32-S3, S31 and P4 only):
LILA_WAKE_WORD=custom:robot

# or a WakeNet model, or turn detection off:
# LILA_WAKE_WORD=hiesp
# LILA_WAKE_WORD=disabled
```

### Display module with a CS wire

```bash
LILA_DISPLAY=LCD_ST7789_240X240    # SPI mode 0 instead of mode 3
```

### Another interface language

```bash
LILA_LANGUAGE=en-US                 # 41 locales ship in the repository
```

The authoritative list needs no ESP-IDF:

```bash
python scripts/build.py --list-languages
```

### Advanced — raw overrides and packaging

```bash
LILA_SDKCONFIG=CONFIG_SOME_VALUE=1  # raw override, applied after every derived option
LILA_ZIP=1                          # also package releases/<version>_<name>.zip
```

## Build the firmware

Preview the command first — it prints exactly what will run, without touching
the tree:

```bash
python scripts/build_lila.py --dry-run
```

Then build:

```bash
python scripts/build_lila.py
```

The wrapper translates `.env` into `scripts/build.py` options, and the build:

1. selects the target (`esp32s3`) and writes `sdkconfig`;
2. builds the assets partition, including the wake-word models;
3. compiles the firmware with `idf.py build`;
4. merges the binaries into `build/merged-binary.bin`.

The first build downloads the dependencies and compiles the whole firmware: it
takes a long time. Later builds reuse the cache and are much faster. If you
switch to another board or variant, the script reconfigures the tree for it.

## Flash the device

Find the serial port and flash:

```bash
idf.py -p COM5 flash monitor
```

```bash
idf.py -p /dev/ttyUSB0 flash monitor      # Linux
idf.py -p /dev/cu.usbmodem101 flash monitor  # macOS
```

`COM5` is an example: use the port the board gets when you plug it in. The
monitor shows the log and stops with `Ctrl + ]`.

If the port does not appear:

- unplug and plug the board again and look for a new `USB JTAG/serial debug
  unit` device;
- some boards only show up after a second reset: hold **BOOT**, press and
  release **RESET**, then release **BOOT**;
- on macOS, use `/dev/cu.usbmodem*` (the `cu.` variant), not `/dev/tty.*`.

To start from a clean flash:

```bash
idf.py -p COM5 erase-flash flash monitor
```

## First boot

Run this right after flashing, with every part still on the desk — it is the
first checkpoint of the whole build. The device connects to the configured
Wi-Fi, shows the face on the screen and listens for the wake word. What to
look for in the log:

- the board name and the Wi-Fi connection;
- the wake word model in use (`Lila`, with the `custom:` prefix);
- the display coming up — the backlight turns on and the face appears;
- no URL in the log: the Lila HTTP helpers print a provider label such as
  `Telegram API` or `Tavily API`, never the request URL, so a bot token never
  reaches the log;
- `Telegram message sent` after you ask Lila to send you a message.

If the tools are not compiled in, that is expected: they are registered only
when their credentials are present in `.env` at build time.

## Print the case

The `.stl` files live in [`STL/`](../STL/) and are indexed in
[`STL/README.md`](../STL/README.md) (Español:
[`STL/README.es.md`](../STL/README.es.md)). The index names each file, the
naming convention and the print settings.

Starting point for the slicer:

| Setting | Value |
| --- | --- |
| Material | PLA or PETG |
| Layer height | 0.2 mm |
| Walls | 3 |
| Infill | 20 % (30 % for the lid) |
| Nozzle | 0.4 mm |
| Tolerance | 0.2–0.3 mm clearance for snap fits |

Print the enclosure body and the screen panel separately, so the screen can be
fitted before the lid is closed. Keep the first print as a test.

*Not verified*: the geometry in `STL/` is still being tuned, so treat the first
print as a prototype and adjust the slicer before asking for a new file.

## Assemble and wire

The `wk-esp32s3-dev` carries the microphone, the amplifier, the buttons and
the LED on the board. You wire exactly two things — the display and the
speaker — and every pin value below is read from
`main/boards/wk-esp32s3-dev/config.h`.

*Not verified*: the tables come from the board configuration; the wiring was
not checked on a physical board with this case.

### Wiring the display

The 7-pin ST7789 module:

| Module pin | Board pin | Signal |
| --- | --- | --- |
| BLK | GPIO10 | backlight |
| SDA (MOSI) | GPIO8 | SPI data |
| SCL (CLK) | GPIO9 | SPI clock |
| DC | GPIO12 | data / command |
| RES | GPIO13 | reset |
| VCC | 3.3 V | power |
| GND | GND | ground |

The module has no CS wire; the firmware still drives a CS line on GPIO11, so
for this module that pin stays unconnected. A module that brings a CS wire
out connects it to GPIO11 and builds with `LILA_DISPLAY=LCD_ST7789_240X240`
— the SPI mode (3 vs 0) is the only difference between the two symbols.

### Wiring the speaker

Two wires from the speaker to the board's speaker output: the amplifier is on
the board. The I2S link between the chip and that amplifier is fixed on the
board and needs no wiring — it is listed for reference only:

| Reference | Pin |
| --- | --- |
| Speaker data (DOUT) | GPIO21 |
| Speaker BCLK | GPIO47 |
| Speaker LRCK | GPIO48 |

### Already on the board

| Function | Pin | Note |
| --- | --- | --- |
| Microphone WS | GPIO40 | on-board microphone |
| Microphone SCK | GPIO42 | on-board microphone |
| Microphone data | GPIO41 | on-board microphone |
| Boot button | GPIO0 | also enters the bootloader |
| Volume up / down | GPIO38 / GPIO39 | |
| Status LED | GPIO14 | |

### Assembly steps

Every step ends with a checkpoint: do not continue until it passes. Debugging
on the desk is much cheaper than debugging through a closed case.

1. **Flash and bench-test first** — [Flash the device](#flash-the-device)
   with every part on the desk.
   - Checkpoint: the boot log runs to the end without a reboot loop, the
     backlight comes on and the face appears on the screen.
2. **Mount the board in the enclosure body.**
   - Checkpoint: the USB-C port lines up with the cutout and the cable goes
     in without force.
3. **Connect the display** using the table above.
   - Checkpoint: power-cycle the board; the backlight turns on as soon as it
     boots.
4. **Connect the speaker** to the board's speaker output.
   - Checkpoint: ask Lila anything; the answer is audible at normal volume,
     with no crackle.
5. **Fit the screen into the panel** and route the wires so nothing is
   pinched.
   - Checkpoint: the face is centered in the opening and no wire is trapped
     between the panel and the body.
6. **Close the lid.**
   - Checkpoint: the seam is even all around, the panel did not move and
     nothing rattles.
7. **Run the full check** — [Check that Lila works](#check-that-lila-works)
   end to end on the finished assistant.

## Check that Lila works

| Check | How |
| --- | --- |
| It boots | the monitor shows the boot log and no reboot loop |
| It sees the screen | the face appears and the backlight is on |
| It hears you | the wake word lights up the screen |
| It talks | the speaker plays the answer |
| It searches | ask for the weather; `web.search` answers when Tavily is configured |
| It writes to you | ask it to send a Telegram message |

`web.search` and `self.telegram.send` only exist when their credentials were
set in `.env` **before** the build. Changing `.env` later requires a new
build.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `idf.py: command not found` | the environment is not loaded | run `. ~/esp-idf/export.sh` (or the PowerShell script) in that terminal |
| `A custom wake word requires ESP32-S3/S31/P4` | the wake word is `custom:<word>` on another chip | use a WakeNet model or `disabled` on other targets |
| The screen stays black | wrong panel symbol or wrong SPI mode | check `LILA_DISPLAY` against your module: 7-pin means `LCD_ST7789_240X240_7PIN` |
| The screen lights up but shows nothing | display wired to the wrong pins | check BLK, SDA, SCL, DC and RES against the display table above |
| The screen shows garbage | SPI mode or wiring mismatch | 7-pin modules use mode 3; modules with CS use mode 0 |
| No sound | speaker not connected, or wrong speaker output | check the speaker wiring above and that both wires reach the board's speaker output |
| The port disappears while flashing | the board reboots into the bootloader | press **BOOT**, tap **RESET**, release **BOOT**, then flash again |
| The build is very slow the first time | dependencies are being downloaded | let it finish; later builds are cached |
| `web.search` does not exist | no Tavily key at build time | set `LILA_TAVILY_API_KEY` in `.env` and rebuild |
| The Telegram tool does not exist | token or chat id missing at build time | set both keys in `.env` and rebuild |
| A URL appears in the log | not a Lila build | Lila logs `Telegram API` / `Tavily API`; update the firmware |

## Where to go next

| Looking for | Go to |
| --- | --- |
| This guide in Spanish | [`lila-build-guide.es.md`](lila-build-guide.es.md) |
| Build variations (round screen, other speaker) | [`variants/README.md`](variants/README.md) |
| The Lila front page | [`README.md`](../README.md) (Español: [`README.es.md`](../README.es.md)) |
| The 3D-print index | [`STL/README.md`](../STL/README.md) |
| Board documentation | [`main/boards/wk-esp32s3-dev/README.md`](../main/boards/wk-esp32s3-dev/README.md) |
| Board list, releases and general setup | [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) |
| ESP-IDF documentation | [Espressif docs](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/index.html) |
