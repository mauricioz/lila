# Lila 3D-print files

**English** · [Español](README.es.md)

This folder holds the `.stl` files of the Lila case: the printable parts that
turn the `wk-esp32s3-dev` board and its ST7789 240x240 screen into a small
desk assistant. The build guide explains the whole path, from flashing the
firmware to assembling the case:

- [Build, flash, print and assemble](../docs/lila-build-guide.md)
- [Construir, flashear, imprimir y montar](../docs/lila-build-guide.es.md)

## Target hardware

| Item | Value |
| --- | --- |
| Board | `wk-esp32s3-dev` (ESP32-S3N16R8) |
| Display | ST7789 240x240, 7-pin module (`LCD_ST7789_240X240_7PIN`) |
| Audio | on-board microphone and amplifier |
| Power | USB-C |

The case is designed for that board only. A different board needs its own files
and its own variant, never an adapted copy of these.

## Naming convention

```
lila-<part>-<board>.stl
```

| Part | Meaning |
| --- | --- |
| `case` | the enclosure body |
| `lid` | the front or top cover |
| `panel` | the bezel around the screen |
| `button` | a button cap |
| `mount` | a stand, wall bracket or spacer |

Example: `lila-case-wk-esp32s3-dev.stl`. Lower case, hyphens, the `.stl`
extension, no spaces and no version numbers in the name.

## Files

| File | Part | Status |
| --- | --- | --- |
| `lila-case-wk-esp32s3-dev.stl` | enclosure body | pending |
| `lila-lid-wk-esp32s3-dev.stl` | front cover | pending |
| `lila-panel-wk-esp32s3-dev.stl` | screen bezel | pending |

The rows marked *pending* are the slots the geometry has to fill. The index is
committed before the geometry on purpose: the guide and the print settings are
stable while the first print is still being tuned.

## Print settings

Starting point for a 200x200x200 mm FDM printer with a 0.4 mm nozzle:

| Setting | Value |
| --- | --- |
| Material | PLA or PETG (PLA is easier to tune, PETG survives heat better) |
| Layer height | 0.2 mm |
| Walls | 3 |
| Infill | 20 % (30 % for the lid) |
| Supports | only where the file asks for them; check the model in the slicer |
| Nozzle | 0.4 mm |
| Tolerance | 0.2–0.3 mm clearance for snap fits |

Print the enclosure body and the panel separately so the screen can be fitted
before the lid is closed. Keep the first print as a test: a fit that is too
tight can be corrected in the slicer, a design that is too tight needs a new
file.

## Adding a file

1. Name the file with the convention above and commit it in this folder.
2. Add a row to the table in this file **and** in [`README.es.md`](README.es.md).
3. Record the print settings that worked for it, and any support the part
   needs.

The folder is tracked by git, so the files travel with the repository. Keep each
file small: an ASCII STL of a simple part is well under a megabyte, and a
binary STL is smaller still.

## Status

The geometry is not committed yet: the case is being printed and tuned, and the
files land here as they are finished. Everything in this repository that
describes the case — the guide, the wiring order and the print settings — is
written against the `wk-esp32s3-dev` board and the ST7789 240x240 panel.
