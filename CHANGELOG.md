# Changelog - Machine Edition Developer Kit

All notable changes to the Machine Edition Developer Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-29

### Added
- Governed reference specimen derived from authorized SROW Public Companion assets (`specimen/srow/`).
- Authoritative public schemas mirrored from `Machine Edition Specification v0.1` (`c18dea5f378265cad37c0acf0c80f3969617876f`) with schema manifest integrity verification (`schemas/schema-manifest.json`).
- Full reference implementation of the Machine Edition Specification v0.1 Validator covering checks C1 through C7:
  - C1: Manifest presence and schema validation (Draft 2020-12).
  - C2: Required package files presence (`manifest.json`, `meaning-units.jsonl`, `provenance.jsonl`, `full-preview.md`, `LICENSE.txt`).
  - C3: Valid JSON/NDJSON syntax.
  - C4: Meaning units, definitions, boundaries, and relationships record schema validation.
  - C5: Referential integrity and provenance link verification.
  - C6: Human entrypoint linkage.
  - C7: License file alignment.
- Minimal parsers and inspection API with `MachineEdition.load()` entity model and TypeScript consumer example (`examples/typescript/consumer.ts`).
- Executable Sample Query Pack (`queries/sample_queries.json`) containing 20 deterministic queries across 9 core categories (`Identity`, `Capability`, `Retrieval`, `Definitions`, `Boundaries`, `Relationships`, `Provenance`, `Resolution`, `Verification`).
- Executable query runner and CLI entry point (`machine_edition_devkit.queries`).
