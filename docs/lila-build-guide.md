# Build, flash, print and assemble Lila

**English** · [Español](lila-build-guide.es.md)

This guide takes a new machine from an empty folder to a working Lila: install
the toolchain, configure the build, compile the firmware, flash it, print the
case and assemble it. It targets the `wk-esp32s3-dev` board with the ST7789
240x240 screen — the Lila profile.

The guide was written against the repository, not against a device: the commands
come from the scripts in this repository, but the printing and the flashing were
not executed by the author of these lines. Anything marked *not verified* needs
a real board.

| Step | What you get |
| --- | --- |
| [Install ESP-IDF](#install-esp-idf) | the toolchain that compiles the firmware |
| [Configure the build](#get-the-source-and-configure-env) | a `.env` that describes your Lila |
| [Build](#build-the-firmware) | `build/merged-binary.bin` |
| [Flash](#flash-the-device) | Lila running on the board |
| [Print](#print-the-case) | the parts of the case |
| [Assemble](#assemble-and-wire) | a finished assistant on the desk |

## What you need

| Item | Detail |
| --- | --- |
| Board | `wk-esp32s3-dev` (ESP32-S3N16R8) |
| Display | ST7789 240x240, 7-pin module (GND, VCC, SCL, SDA, RES, DC, BLK) |
| Speaker | 4 Ω, connected to the board's I2S amplifier output |
| Cable | USB-C, for power and for flashing |
| Computer | Windows, Linux or macOS with about 20 GB of free disk |
| Toolchain | ESP-IDF `release/v6.1` (minimum supported: v6.0.1) |
| Printer | FDM, 0.4 mm nozzle, for the case (optional) |

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

The device connects to the configured Wi-Fi, shows the face on the screen and
listens for the wake word. What to look for in the log:

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

Assembly order:

1. mount the board in the enclosure body;
2. connect the display and the speaker;
3. fit the screen into the panel;
4. close the lid and screw it;
5. plug USB-C and boot the device.

The pin map of the `wk-esp32s3-dev` board, read from
`main/boards/wk-esp32s3-dev/config.h`:

| Function | Pin |
| --- | --- |
| Display backlight | GPIO10 |
| Display MOSI (SDA) | GPIO8 |
| Display CLK (SCL) | GPIO9 |
| Display DC | GPIO12 |
| Display reset | GPIO13 |
| Microphone WS | GPIO40 |
| Microphone SCK | GPIO42 |
| Microphone data | GPIO41 |
| Speaker data (DOUT) | GPIO21 |
| Speaker BCLK | GPIO47 |
| Speaker LRCK | GPIO48 |
| Boot button | GPIO0 |
| Volume up / down | GPIO38 / GPIO39 |
| Status LED | GPIO14 |

The 7-pin ST7789 module has no CS line, which is exactly why the default
`LILA_DISPLAY` is `LCD_ST7789_240X240_7PIN` (SPI mode 3). If your module has a
CS wire, build with `LILA_DISPLAY=LCD_ST7789_240X240` (SPI mode 0).

*Not verified*: the table above comes from the board configuration, but the
wiring was not checked on a physical board with this case.

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
| The screen shows garbage | SPI mode or wiring mismatch | 7-pin modules use mode 3; modules with CS use mode 0 |
| No sound | speaker not connected, or wrong I2S pins | check the speaker pins in the table above and the amplifier |
| The port disappears while flashing | the board reboots into the bootloader | press **BOOT**, tap **RESET**, release **BOOT**, then flash again |
| The build is very slow the first time | dependencies are being downloaded | let it finish; later builds are cached |
| `web.search` does not exist | no Tavily key at build time | set `LILA_TAVILY_API_KEY` in `.env` and rebuild |
| The Telegram tool does not exist | token or chat id missing at build time | set both keys in `.env` and rebuild |
| A URL appears in the log | not a Lila build | Lila logs `Telegram API` / `Tavily API`; update the firmware |

## Where to go next

| Looking for | Go to |
| --- | --- |
| This guide in Spanish | [`lila-build-guide.es.md`](lila-build-guide.es.md) |
| The Lila front page | [`README.md`](../README.md) (Español: [`README.es.md`](../README.es.md)) |
| The 3D-print index | [`STL/README.md`](../STL/README.md) |
| Board documentation | [`main/boards/wk-esp32s3-dev/README.md`](../main/boards/wk-esp32s3-dev/README.md) |
| Board list, releases and general setup | [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) |
| ESP-IDF documentation | [Espressif docs](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/index.html) |
