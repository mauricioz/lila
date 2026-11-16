# FEAT_008 - Tasks

Status: in progress · Owner: @mauricioz · Branch: `devs/mauri/fix/FEAT_008-mic-gain`

Each task is one reviewable commit or less. Mark `[x]` only when the code, tests
and docs for that task are in the same commit.

## 1. Spec and standards

- [x] Refine `FEAT_008.md` against the code
- [x] Load and record the applicable standards (`process/STANDARDS.md`)
- [x] Create the OpenSpec change (`openspec/changes/FEAT-008-mic-input-gain/`)

## 2. Implementation

- [x] Task 1 - apply `input_gain_` in `NoAudioCodec::Read()` with saturation
- [x] Task 2 - add `WK_ESP32S3_DEV_MIC_GAIN` to `main/Kconfig.projbuild`
- [x] Task 3 - apply the gain from the `wk-esp32s3-dev` board

## 3. Tests

- [x] Regression test for the failure mode: the gain defaults to 0 on every
      other board, so the read path keeps returning the same samples
- [x] Host suite unchanged and green (`python -m unittest discover -s scripts/tests`)
- [ ] Hardware test: the voice reaches the AFE at about -25 dBFS RMS

## 4. Documentation

- [x] `process/ROADMAP.md` shipped table
- [x] `CHANGELOG.md`
- [x] `docs/lila-build-guide.md` and `docs/lila-build-guide.es.md`
- [x] `openspec/changes/FEAT-008-mic-input-gain/`

## 5. Verification

- [x] `python -m compileall -q scripts`
- [x] `python scripts/sync_skills.py --check`
- [x] `python scripts/check_workflow.py`
- [x] `python -m unittest discover -s scripts/tests -v`
- [x] `python scripts/build_lila.py --dry-run`
- [x] `python scripts/check_format.py --base origin/main`
- [x] Firmware build (local ESP-IDF 6.1)

## 6. Review and merge

- [ ] `architecture-compliance-check` passed
- [ ] `code-review-checklist` passed
- [ ] Security scan passed
- [ ] Hardware validation recorded in the PR
- [ ] PR opened from the feature branch (never push to `main`)
