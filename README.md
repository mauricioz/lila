# Lila

**English** · [Español](README.es.md)

**Lila** is a personal fork of the [XiaoZhi AI Chatbot](https://github.com/78/xiaozhi-esp32),
the open-source ESP32 voice assistant created by [78](https://github.com/78) and the
XiaoZhi community. My daughter **Sophie** chose the name, so this little assistant is
called Lila from here on.

The credit for everything that makes this firmware work belongs to the upstream
project: the audio pipeline, the ESP-SR wake-word engines, the board ports, the
WebSocket and MQTT/UDP protocols, the MCP server, the documentation and years of
careful engineering. Thank you, 78, and thank you to everyone who contributed there.
Lila only adds a few personal touches on top, and it inherits the upstream MIT license.

This README documents **Lila only**. The upstream documentation, the board matrix,
the upstream translations and the community support live in
[78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) — see
[Upstream project](#upstream-project) at the end of this page.

## What Lila adds over upstream

Every change is additive: without a `.env` file and without API credentials, a Lila
build behaves exactly like upstream.

- **Configured builds from `.env`** — `scripts/build_lila.py` reads board, variant,
  language, wake word, display panel, API credentials, extra sdkconfig and zip options
  from `.env` (see `.env.example`) and forwards them to `scripts/build.py`.
  `--dry-run` prints the exact command.
- **Custom MultiNet wake words from the CLI** — `scripts/build.py --wake-word
  custom:<word>` turns any word into a MultiNet custom command, which
  `scripts/build_default_assets.py` packs into the assets partition. No source or
  sdkconfig edits are needed, and the Lila profile wakes on `custom:lila`.
- **Raw sdkconfig overrides** — a repeatable `--sdkconfig KEY=VALUE` flag applied after
  every derived option, which is how API keys and the LCD panel choice are injected
  without touching the tree.
- **`web.search` MCP tool** — Tavily-backed web search, registered only when
  `XIAOZHI_TAVILY_API_KEY` is non-empty. It returns the search answer plus numbered
  results and permits a single in-flight search.
- **`self.telegram.send` MCP tool** — sends a Telegram message, registered only when
  both `XIAOZHI_TELEGRAM_BOT_TOKEN` and `XIAOZHI_TELEGRAM_CHAT_ID` are set. Delivery
  runs on a one-shot worker task so the main event loop never blocks on the network.
- **Lila hardware profile** — Spanish (`es-ES`) defaults, the `lila` wake word and an
  ST7789 240x240 panel (`LCD_ST7789_240X240_7PIN`, or `LCD_ST7789_240X240` when the
  module has a CS line), all selectable from `.env` and matching the 7-pin ST7789
  wiring this build targets on the `wk-esp32s3-dev` board.
- **Documented board changes** — `main/boards/wk-esp32s3-dev/README.md` documents the
  wrapper, both display variants and the two optional tools.
- **A development workflow** — specs, standards, agent skills, host CI checks and a
  PR-only policy for `main` (see [Development workflow](#development-workflow)).

## Quick start

Source your ESP-IDF `release/v6.1` environment first (see the
[upstream setup guide](https://github.com/78/xiaozhi-esp32#development-environment)),
then:

```bash
cp .env.example .env                      # edit language, wake word, panel and keys
python scripts/build_lila.py --dry-run    # print the command
python scripts/build_lila.py              # build
```

Both tools can also be enabled for any board in `idf.py menuconfig`
(`Xiaozhi Assistant` → `Tavily API key`, `Telegram bot token`, `Telegram chat ID`).

## Build guide and 3D-print case

A step-by-step guide takes a new machine from an empty folder to a working
Lila: the shopping list, installing ESP-IDF on Windows, Linux or macOS,
configuring `.env` with copy-paste recipes, building, flashing, printing the
case, and wiring and assembling it with a checkpoint after every step.

| Guide | English | Spanish |
| --- | --- | --- |
| Build, flash, print and assemble | [`docs/lila-build-guide.md`](docs/lila-build-guide.md) | [`docs/lila-build-guide.es.md`](docs/lila-build-guide.es.md) |
| 3D-print files (`.stl`) | [`STL/README.md`](STL/README.md) | [`STL/README.es.md`](STL/README.es.md) |

The `.stl` files live in [`STL/`](STL/). The case targets the `wk-esp32s3-dev`
board with the ST7789 240x240 panel; the index names every file, the print
settings and what is still pending.

## Development workflow

Lila is developed with the process it ships: a spec, a branch, CI, and a pull
request. **`main` is protected and never receives a direct push** — every change,
including process and documentation edits, arrives through a PR.

| Step | Where |
| --- | --- |
| Process overview and map | [`process/README.md`](process/README.md) |
| Full pipeline and quality gates | [`process/WORKFLOW.md`](process/WORKFLOW.md) |
| Rules per change area | [`process/STANDARDS.md`](process/STANDARDS.md), [`process/standards/`](process/standards/) |
| Feature specs (`FEAT_XXX`) | [`process/specs/`](process/specs/) |
| Shipped and planned features | [`process/ROADMAP.md`](process/ROADMAP.md) |
| OpenSpec, CodeGraph and RTK | [`process/TOOLING.md`](process/TOOLING.md) |
| Branch protection setup | [`.github/BRANCH_PROTECTION.md`](.github/BRANCH_PROTECTION.md) |
| Changelog | [`CHANGELOG.md`](CHANGELOG.md) |

Spec-driven development uses [OpenSpec](https://github.com/Fission-AI/OpenSpec)
for changes that alter a contract, plus a `FEAT_XXX` document per feature.
[CodeGraph](https://github.com/colbymchenry/codegraph) indexes the firmware so an
agent can find symbols and call paths without reading whole files, and
[RTK](https://github.com/rtk-ai/rtk) compresses command output to keep agent
context small. All three are optional for building the firmware.

Skills for OpenCode and Claude Code are vendored in the repository
(`.opencode/skills/` is the source, `.claude/skills/` is generated) so the
pipeline, the standards selection and the review gates behave the same in both
tools.

```bash
# The checks CI runs on every pull request
python -m compileall -q scripts
python scripts/sync_skills.py --check
python scripts/check_workflow.py
python -m unittest discover -s scripts/tests -v

# Preview the configured build without starting ESP-IDF
python scripts/build_lila.py --dry-run

# C/C++ style on the lines the change touches
python scripts/check_format.py --base origin/main
```

CI is split in two: `ci.yml` runs the host checks and `clang-format` on every
pull request, while `firmware-build.yml` is a manual, reproducible Lila build in
the ESP-IDF 6.1 container. A pull request lists which checks ran and what still
needs validation on a physical device.

## Upstream project

Lila is built on [XiaoZhi AI Chatbot](https://github.com/78/xiaozhi-esp32) by
[78](https://github.com/78) and the XiaoZhi community, and it keeps the upstream
MIT license. Everything that is not a Lila addition lives upstream:

| Looking for | Go to |
| --- | --- |
| This page in Spanish | [`README.es.md`](README.es.md) |
| Project overview, features and upstream translations | [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) |
| Supported boards and release matrix | [upstream board list](https://github.com/78/xiaozhi-esp32#supports-138-board-directories-and-171-release-variants-partial-list) |
| Firmware releases | [upstream releases](https://github.com/78/xiaozhi-esp32/releases) |
| ESP-IDF setup and flashing guide | [upstream README](https://github.com/78/xiaozhi-esp32#development-environment) |
| Board and firmware documentation | [`docs/`](docs/) in this repository, upstream docs |
| Lila-specific features | [What Lila adds over upstream](#what-lila-adds-over-upstream) |
| Lila release plans | [`process/ROADMAP.md`](process/ROADMAP.md) |

Upstream changes are not pulled in automatically; Lila tracks them by hand and
keeps its own release line.
