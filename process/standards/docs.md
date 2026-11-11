# Documentation standard

## Structure

- **DOC-1** The root `README.md` is Lila's front page: identity, credit to the
  upstream project, what Lila adds, quick start, the development workflow, and a
  short reference to the upstream project.
- **DOC-2** Do not paste upstream documentation into this repository. Link to
  [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) instead, and keep the
  Lila page about Lila. The upstream translations (`README_zh.md`, `README_ja.md`)
  are not mirrored here either. Lila's own translations are a different matter:
  they are Lila content and are maintained here (see DOC-16).
- **DOC-3** Board documentation lives in `main/boards/<board>/README.md` and
  covers: hardware and wiring, build commands, configuration, optional tools, and
  known limitations.
- **DOC-4** Workflow documentation lives in `process/`. `process/README.md` is the
  entry point; every new workflow file must be linked from it.

## Writing

- **DOC-5** Lead with the action: a reader should be able to copy a command from
  the first screen of the section.
- **DOC-6** Every command shows the exact working directory assumptions and uses
  `python scripts/...` (not `./script.py`).
- **DOC-7** Prefer tables for options and checklists for gates; keep line lengths
  under ~100 characters.
- **DOC-8** Use placeholders (`<token>`, `tvly-...`) for credentials, never a
  real-looking example that could be mistaken for a leaked key.
- **DOC-9** State what is not verified yet ("hardware validation still needed")
  instead of implying the feature was tested on a device.

## Links and anchors

- **DOC-10** Use relative links inside the repository and absolute links only for
  external sites.
- **DOC-11** When renaming a file, update every reference in the same PR;
  `scripts/check_workflow.py` verifies the required links.
- **DOC-12** Keep headings stable when people may link to them; add a new heading
  instead of renaming an anchored one.

## Roadmap and changelog

- **DOC-13** Every user-visible change updates the shipped table in
  `process/ROADMAP.md` and adds a `CHANGELOG.md` entry.
- **DOC-14** The roadmap entry names the files involved, so the next contributor
  can find the implementation without a search.
- **DOC-15** Do not move planned items between releases without maintainer
  approval in the PR.

## Translations

- **DOC-16** Every document Lila translates ships in both languages: the English
  file and a Spanish sibling with the `.es.md` suffix in the same folder
  (`README.md` / `README.es.md`, `docs/lila-build-guide.md` /
  `docs/lila-build-guide.es.md`, `STL/README.md` / `STL/README.es.md`).
  - Both files carry a language switcher that links the other one.
  - The Spanish file keeps the same section structure as the English one; a new
    section lands in both. `scripts/check_workflow.py` fails the pull request
    when a translation is missing, unlinked or out of sync.
  - Commands, file names, option names and error messages stay verbatim in the
    Spanish version; only the prose is translated.

## 3D-print files

- **DOC-17** The printable files of the Lila case live in `STL/`.
  - One file per part, named `lila-<part>-<board>.stl`, lower case with
    hyphens and no version number.
  - Every file has a row in `STL/README.md` and in `STL/README.es.md`, with the
    print settings that worked for it.
  - The index names the exact hardware the geometry targets (board, panel,
    connector) so nobody prints a case for the wrong device.
  - The upstream is not mirrored here: a third-party case is linked, not
    copied.
