# Changelog - Machine Edition Developer Kit

All notable changes to the Machine Edition Developer Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-29

### Added
- Governed reference specimen derived from authorized SROW Public Companion assets (`specimen/srow/`).
- Authoritative public schemas mirrored from `Machine Edition Specification v0.1` (`c18dea52074ba278ec6bc4a544c80300df6d8882`) with schema manifest integrity verification (`schemas/schema-manifest.json`).
- Full reference implementation of the Machine Edition Specification v0.1 Validator covering checks C1 through C7:
  - C1: Manifest presence and schema validation (Draft 2020-12).
  - C2: Required package files presence (`manifest.json`, `meaning-units.jsonl`, `provenance.jsonl`, `full-preview.md`, `LICENSE.txt`).
  - C3: Valid JSON/NDJSON syntax.
  - C4: Meaning units, definitions, boundaries, and relationships record schema validation.
  - C5: Referential integrity and provenance link verification.
  - C6: Human entrypoint linkage.
  - C7: License file alignment.
- Structured validation report output with `ME_CONFORMANT` / `ME_NONCONFORMANT` determinations.
- Negative fixture test suite verifying fail-closed behavior across all structural failure modes.
