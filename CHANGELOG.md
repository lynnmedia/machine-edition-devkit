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
- Executable Sample Query Pack (`queries/sample_queries.json`) containing 20 deterministic queries across 9 core categories.
- Executable representation comparison trial (`comparison/`) evaluating PDF, EPUB, Naive RAG, and Machine Edition across 16 tasks in 8 families under guaranteed information parity.
- Comparison execution engine and CLI tool (`machine_edition_devkit.comparison`).
- Comparative methodology documentation (`docs/rag-comparison.md`).
- Frozen Machine Edition Representation Benchmark v0.1 (`benchmark/` and `machine_edition_devkit.benchmark`):
  - 40 frozen benchmark tasks distributed equally across 8 task families (5 items each): factual retrieval, relationship retrieval, hierarchy preservation, provenance tracing, boundary/constraint recognition, ambiguity handling, multi-resolution retrieval, unsupported claim detection.
  - Frozen split into 8 calibration items and 32 evaluation items.
  - 16-fact source corpus derived exclusively from authorized SROW Public Companion v0.1 material with 100% information parity verified across PDF, EPUB, RAG, and Machine Edition.
  - Strict gold firewall separating public task inputs (`tasks.jsonl`) from adjudication ledgers (`gold/`).
  - Offline deterministic scoring engine evaluating 7 dimensions with a 14-token failure taxonomy and 13 synthetic validation fixtures.
  - Cryptographic integrity manifest (`benchmark/integrity-manifest.json`), rights manifest (`benchmark/RIGHTS.md`), threats-to-validity registry (`benchmark/THREATS-TO-VALIDITY.md`), and comprehensive CLI tooling (`verify`, `rebuild`, `test-scorer`, `parity`).
- Benchmark freeze identity reconciliation (`ME-BENCH-001A`) confirming zero benchmark-critical content divergence between lineage commits.
- Structured publication representation trial study (`ME-RES-001`):
  - Pre-registered protocol and directional hypotheses (H1-H5) frozen prior to execution (`research/me-res-001/PROTOCOL.md`, `HYPOTHESES.md`).
  - Executed controlled 384-run evaluation matrix (32 tasks × 4 conditions × 3 replicates) with deterministic pseudo-random scheduling (seed `44527555`).
  - Enforced strict gold firewall isolating generation runtime from adjudication standards.
  - Paired bootstrap statistical analysis over 10,000 resamples confirming significant advantages for Machine Edition in provenance completeness, relationship accuracy, and semantic invariant preservation under factual neutrality.
  - Comprehensive scientific research report (`research/me-res-001/report/ME-RES-001-REPORT.md`) and CLI suite (`machine_edition_devkit.research.me_res_001`).
