# FEAT_003 — Lila-only README

| Field | Value |
| --- | --- |
| ID | FEAT_003 |
| Title | Replace the copied upstream README with a Lila front page and an upstream link |
| Owner | @mauricioz |
| Status | in progress |
| Priority | medium |
| Branch | `devs/mauri/chore/lila-workflow` |
| OpenSpec change | — (documentation only) |
| Created | 2026-11-10 |
| Updated | 2026-11-10 |

## Summary

The root `README.md` pasted the whole upstream XiaoZhi README below the Lila
sections. This change replaces it with a Lila-only front page that credits the
upstream and links to it, and removes the copied upstream translations.

## Motivation

The Lila repository is now a standalone project, not a GitHub fork, so carrying
the upstream README and its translations is both redundant and confusing: it
duplicates content that changes upstream, it mixes two brands on one page, and
the upstream language switcher pointed at files Lila does not maintain. A
Lila-only page with one clear reference is shorter, honest and easier to keep
current.

## Acceptance criteria

- [x] `README.md` documents Lila: identity, what Lila adds, quick start, the
      development workflow.
- [x] The upstream is credited and linked, with a small table pointing to the
      upstream README, board list, releases and setup guide.
- [x] The upstream README body and the language switcher are gone.
- [x] `README_zh.md` and `README_ja.md` (upstream translations) are removed;
      the upstream keeps its own.
- [x] No link in the repository points to the removed files.
- [x] `scripts/check_workflow.py` fails if the upstream body comes back or if the
      upstream link disappears.
- [x] The documentation standard states the new rule.

## Technical blueprint

| Area | Change |
| --- | --- |
| Docs | `README.md` rewritten; `README_zh.md` and `README_ja.md` deleted |
| Policy | `process/standards/docs.md` DOC-1 and DOC-2 rewritten |
| Process | `process/README.md` wording (standalone repository), `process/ROADMAP.md` shipped table |
| Checks | `scripts/check_workflow.py`: README required and forbidden markers, README added to the link check |
| Changelog | `CHANGELOG.md` 0.2.0 |

### Data and contracts

No firmware, build or protocol change. The `docs/` directory keeps the upstream
developer documentation that the repository still needs (board guide, audio
design, code style, protocol notes); only the duplicated README material is
removed.

### Risks

- Risk: upstream readers lose the setup guide on the front page. → mitigation:
  the "Upstream project" table links the upstream setup, flashing and board
  documentation directly.
- Risk: the upstream README contained the release matrix. → mitigation: the
  matrix is linked upstream and the inherited baseline is summarised in
  `process/ROADMAP.md`.

## Scope

**In scope**

- The root README and the two upstream translation files.
- The documentation standard and the mechanical checks that enforce them.

**Out of scope**

- `docs/` and the board READMEs, which are Lila-relevant and still maintained
  here.
- Upstream synchronisation.

## Dependencies

- None.

## Hardware validation

Not applicable: documentation only.
