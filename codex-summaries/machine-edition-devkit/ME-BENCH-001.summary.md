# ME-BENCH-001 — Summary

## HDCP ID and Title
* **ID**: `ME-BENCH-001`
* **Title**: `Machine Edition Representation Benchmark v0.1`

## Repository and Branch
* **Repository**: `machine-edition-devkit`
* **Branch**: `main`

## Opening Evidence
* **CWD**: `/Users/studiobe/development/github/lynnmedia/machine-edition-devkit`
* **Precursor**: `MEDK_V01_FUNCTIONAL_SCOPE_COMPLETE`
* **Execution Class**: `BENCHMARK_CORPUS_AND_SCORING_FREEZE`

## Determination & Gates
* **Determination**: `ME_BENCH_V01_FROZEN_AND_LOCALLY_REPRODUCIBLE`
* **Public Reproducibility Gate**: `PENDING_ME_DIST_001`

---

## 1. Benchmark Identity & Lineage
* **Benchmark ID**: `winmedia.machine-edition-representation-benchmark.v0.1`
* **Version**: `0.1.0`
* **Status**: `frozen`
* **Freeze Date**: `2026-08-29`
* **Source Lineage**: `SROW Public Companion v0.1 (archive sha256: 0cd42e724bcd7d4b54c0f850a51ef7b875152cd01f7a20f5b7b34e0d73b5d181) -> SROW Public Reference Specimen -> MEDK-006 -> ME-BENCH-001`
* **Source Document**: `benchmark/source/benchmark-source.md`
* **Source Hash**: `02a76fc32d8471e95669d57a25032aa283737da29b20755ce650ef31ff21544a`
* **Rights**: Creative Commons Attribution 4.0 International (CC BY 4.0) within authorized public companion scope (`benchmark/RIGHTS.md`). Zero governed manuscript, paid-edition text, or internal adjudication ledgers included.

---

## 2. Benchmark Corpus & Task Distribution
* **Total Scored Tasks**: 40 items (`ME-BENCH-001` to `ME-BENCH-040`)
* **Task Split**:
  * Calibration: 8 items (1 item per family)
  * Evaluation: 32 items (4 items per family)
* **Task Families (5 items each)**:
  1. `factual_retrieval`: 5 items (1 calibration, 4 evaluation)
  2. `relationship_retrieval`: 5 items (1 calibration, 4 evaluation)
  3. `hierarchy_preservation`: 5 items (1 calibration, 4 evaluation)
  4. `provenance_tracing`: 5 items (1 calibration, 4 evaluation)
  5. `boundary_constraint_recognition`: 5 items (1 calibration, 4 evaluation)
  6. `ambiguity_handling`: 5 items (1 calibration, 4 evaluation)
  7. `multi_resolution_retrieval`: 5 items (1 calibration, 4 evaluation)
  8. `unsupported_claim_detection`: 5 items (1 calibration, 4 evaluation)

---

## 3. Representation Artifacts & Hashes
1. **PDF**: `benchmark/representations/pdf/benchmark-document.pdf` (Latin-1 fixed-layout document)
   * SHA-256: `632dc518d2d631df6504a7e9dae605d5395696515f20668b556f8f5339f4d7ff`
2. **EPUB**: `benchmark/representations/epub/benchmark-document.epub` (EPUB 3.0 reflowable publication)
   * SHA-256: `18ba036a94f61f71dfbca4eeb9fec0d65b70503f16dbe637db6a40ef77df7ce9`
3. **Naive RAG**: `benchmark/representations/rag/rag-corpus.json` (Sliding-window lexical BM25 chunks)
   * SHA-256: `915fe283995873a466ecf2ee2939316d944e83f36bf7b2fb0a69a923769c0953`
   * Configuration: paragraph-preserving sliding window, target chunk size 250 characters, 40-character overlap.
4. **Machine Edition**: `benchmark/representations/machine-edition/package/` (Conformant Specimen Package)
   * Conformance Status: `ME_CONFORMANT` (C1-C7 verified by validator)
   * Package ID: `winmedia.srow.benchmark-specimen`

---

## 4. Information Parity Gate
* **Result**: `16/16 PASS` (100% information parity verified across all 4 representations for all 16 tracked source facts in `benchmark/source/source-inventory.json`).

---

## 5. Gold Firewall & Adjudication Structure
* **Firewall Result**: `PASS`. `tasks.jsonl` contains zero gold answers, accepted variants, prohibited assertions, or scoring rules.
* **Separated Gold Ledgers**:
  * `benchmark/gold/answers.jsonl`
  * `benchmark/gold/provenance.jsonl`
  * `benchmark/gold/relationships.jsonl`
  * `benchmark/gold/constraints.jsonl`

---

## 6. Scoring Engine & Failure Taxonomy
* **Offline Scoring Dimensions (7)**:
  1. `correctness` (0.0 to 1.0)
  2. `provenance_completeness` (0.0 to 1.0)
  3. `unsupported_assertion_rate` (float)
  4. `semantic_invariant_preservation` (0.0 to 1.0)
  5. `relationship_accuracy` (0.0 to 1.0)
  6. `constraint_violations` (integer count)
  7. `failure_mode` (list of taxonomy tokens)
* **Failure Modes Taxonomy (14)**:
  `NONE`, `INCORRECT_FACT`, `OMISSION`, `UNSUPPORTED_ASSERTION`, `PROVENANCE_MISSING`, `PROVENANCE_FABRICATED`, `RELATIONSHIP_ERROR`, `HIERARCHY_ERROR`, `BOUNDARY_VIOLATION`, `AMBIGUITY_COLLAPSE`, `RESOLUTION_ERROR`, `REFUSAL_WHEN_SUPPORTED`, `ANSWER_WHEN_UNSUPPORTED`, `EXECUTION_ERROR`
* **Scorer Fixture Suite**: `13/13 PASS` (Validates detection of perfect answers, factual errors, partial answers, prohibited claims, fabricated/missing provenance, reversed relationships, boundary breaches, ambiguity handling/collapse, unsupported abstention, and confabulation).

---

## 7. Methodological Governance & Research Separation
* **Research Separation Rule**: Maintained strict firewall between benchmark construction and experimental model runs. No LLMs were queried; no wording or weights were tuned on model performance.
* **Threats to Validity**: Documented in `benchmark/THREATS-TO-VALIDITY.md` across 8 categories (TV-01 through TV-08).

---

## 8. Verification & Clean-Room Reproduction
* **Reproduction Commands**:
  * `python -m machine_edition_devkit.benchmark verify` -> PASS
  * `python -m machine_edition_devkit.benchmark rebuild` -> PASS
  * `python -m machine_edition_devkit.benchmark test-scorer` -> PASS
  * `python -m machine_edition_devkit.benchmark parity` -> PASS
* **Isolated Clean-Room Test**: `test_isolated_clean_room_reproduction` in temporary directory -> PASS
* **Full Test Suite**: `57/57 PASS`

---

## 9. Commit & Follow-On Status
* **Commit SHA**: `efe014baabbdb4971f3d862a2b08cb1b3848ac5e`
* **Known Follow-ons**:
  * `ME-RES-001` (Experimental model evaluation study)
  * `ME-DIST-001` (Public artifact distribution & verification)
  * `ME-SROW-PUBLIC-DISTRIBUTION-RECONCILIATION-001`
