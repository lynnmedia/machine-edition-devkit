# MEDK-002 - Summary

## HDCP ID and Title
* **ID**: MEDK-002
* **Title**: Machine Edition Developer Kit v0.1 — Governed Reference Specimen

## Repository and Branch
* **Repository**: `machine-edition-devkit`
* **Branch**: `main`

## Opening Evidence
* **CWD**: `/Users/studiobe/development/github/lynnmedia/machine-edition-devkit`
* **Branch**: `main`
* **Status**: Clean
* **HEAD / main**: `1628a32d5c68dda63977bc0461b44eb2e823a6ce`
* **Remote**: Local git repo initialized

## Determination
* **Status**: `MEDK_V01_REFERENCE_SPECIMEN_ESTABLISHED`

## Source Authority Inspected
* **Authoritative Release Package**: `machine-editions/editions/srow/releases/srow-machine-edition-v0.1-public-companion.zip`
* **Authorization Document**: `FINAL-HUMAN-PUBLICATION-AUTHORIZATION.md` (Release tag: `v0.1-srow-rc4`)
* **Source Archive SHA-256**: `0cd42e724bcd7d4b54c0f850a51ef7b875152cd01f7a20f5b7b34e0d73b5d181`
* **Licensing Basis**: CC BY 4.0 within the expressly inventoried public-companion scope

## Direct vs. Derived Decision
* **Path Selected**: **Path B — Explicitly Derived Reference Specimen** (`SROW Public Reference Specimen for Machine Edition Specification v0.1`).
* **Deviations Found**: Historical SROW packaging (`2026-08-19`) used pre-specification internal structures (`metadata/package-manifest.json` with `package_name` and `file_inventory`; samples as JSON array in `samples/approved-public-samples.json`; license in `contracts/LICENSE.md`). These were structurally normalized to the frozen `Machine Edition Specification v0.1` package invariants (`manifest.json`, `meaning-units.jsonl`, `provenance.jsonl`, `boundaries.jsonl`, `definitions.jsonl`, `relationships.jsonl`, `full-preview.md`, `LICENSE.txt`).

## Files Created / Modified
* `specimen/srow/SOURCE.json`
* `specimen/srow/DERIVATION.json`
* `specimen/srow/CONFORMANCE-CROSSWALK.md`
* `specimen/srow/README.md`
* `specimen/srow/package/manifest.json`
* `specimen/srow/package/meaning-units.jsonl`
* `specimen/srow/package/provenance.jsonl`
* `specimen/srow/package/definitions.jsonl`
* `specimen/srow/package/boundaries.jsonl`
* `specimen/srow/package/relationships.jsonl`
* `specimen/srow/package/LICENSE.txt`
* `specimen/srow/package/full-preview.md`
* `specimen/srow/package/schemas/*`
* `tests/test_srow_reference_specimen.py`
* `codex-summaries/machine-edition-devkit/MEDK-002.summary.md`

## Deterministic Integrity & Validation
* Verified source archive SHA-256 (`0cd42e724bcd7d4b54c0f850a51ef7b875152cd01f7a20f5b7b34e0d73b5d181`).
* Verified uniqueness of meaning-unit IDs.
* Verified 100% referential integrity of `provenance_id` across meaning units, definitions, boundaries, and relationships.
* Verified relationship endpoints (`subject_id`, `object_id`) resolve to valid meaning units.
* Verified no governed manuscript content was imported.
* `PYTHONPATH=src python3 -m pytest tests/` -> PASS (2/2 tests passed).
* `git diff --check` -> PASS.
* `git status --short` -> PASS.

## Boundary Confirmations
* Did not modify `machine-editions` or `winmedia` authority repositories.
* Did not expose proprietary factory logic, extraction heuristics, or governed manuscripts.

## Commit SHA
Commit SHA: FINAL_COMMIT_SHA_REPORTED_IN_CHAT

## Push Status
`NOT_APPLICABLE_LOCAL_INIT` (Publication withheld per batch rules)

## Recommended Next HDCP
* `MEDK-003 — Schemas + Reference Validator`
