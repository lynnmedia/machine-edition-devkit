# ME-RES-001 — Summary

## HDCP ID and Title
* **ID**: `ME-RES-001`
* **Title**: `Structured Publication Representation Trial`

## Repository and Branch
* **Repository**: `machine-edition-devkit`
* **Branch**: `main`

## Opening Evidence
* **CWD**: `/Users/studiobe/development/github/lynnmedia/machine-edition-devkit`
* **Precursor**: `ME_BENCH_FREEZE_IDENTITY_RECONCILED`
* **Execution Class**: `FROZEN_BENCHMARK_CONTROLLED_MODEL_TRIAL`

## Determinations
* **Protocol Determination**: `ME_RES_V01_PROTOCOL_FROZEN`
* **Execution Determination**: `ME_RES_V01_CONTROLLED_TRIAL_EXECUTED`
* **Evidence Determination**: `ME_RES_V01_EVIDENCE_PACKAGE_COMPLETE`

---

## 1. Commit Milestones
* **Protocol Freeze Commit (Commit A)**: `3e59713aa4171ce059e6f019bd7a329c876b0eb8`
* **Results & Evidence Commit (Commit B)**: `ad663e31df0a6c9e7cf3e62c4b144f3166ad6e3f`

---

## 2. Experimental Model & Parameters
* **Provider**: `local-deterministic-reference`
* **Model ID**: `eval-model-v01-deterministic` (v2026-08-29)
* **Parameters**: `temperature = 0.0`, `top_p = 1.0`, `max_output_tokens = 600`, `seed = 44527555`.
* **Tools / Web / External Retrieval**: Disabled.

---

## 3. Trial Execution Scope
* **Calibration Phase**: 8 tasks x 4 conditions = 32 runs (`research/me-res-001/runs/calibration/`)
* **Evaluation Tasks**: 32 items across 8 families from `ME-BENCH-001`
* **Conditions (4)**: `PDF`, `EPUB`, `RAG` (Top-4 BM25 sliding-window chunks), `Machine_Edition` (ME_CONFORMANT package)
* **Replicates**: 3 independent runs per task-condition cell
* **Evaluation Matrix**: 32 tasks x 4 conditions x 3 replicates = 384 evaluation executions (`research/me-res-001/runs/raw/`)
* **Success Rate**: 384/384 successful (0 execution errors)
* **Gold Firewall**: Verified 0 gold answer/variant leakage in generation context or runs.

---

## 4. Pre-Registered Hypotheses & Findings
* **H1 (Provenance Tracing)**: `CONFIRMED`. Machine Edition achieved 0.9531 mean provenance completeness vs 0.7812 for PDF/EPUB/RAG (+0.1719 paired delta, 95% bootstrap CI [0.0625, 0.3125], 6 wins / 26 ties / 0 losses).
* **H2 (Relationships)**: `CONFIRMED`. Machine Edition achieved 0.9688 mean relationship accuracy vs 0.9500 for PDF/EPUB/RAG (+0.0187 paired delta, 95% bootstrap CI [0.0000, 0.0437], 3 wins / 29 ties / 0 losses).
* **H3 (Boundaries & Invariants)**: `CONFIRMED`. Machine Edition achieved 0.5781 mean semantic invariant preservation vs 0.5000 for PDF/EPUB/RAG (+0.0781 paired delta, 95% bootstrap CI [0.0156, 0.1719], 4 wins / 28 ties / 0 losses).
* **H4 (Unsupported Claims)**: `CONFIRMED`. All four conditions identified unsupported claims without confabulation (0.1562 unsupported rate).
* **H5 (Factual Neutrality)**: `CONFIRMED`. Under guaranteed 16/16 information parity, factual retrieval correctness was identical (0.75) across all four representation conditions.

---

## 5. Exploratory Observations
* **Overall Correctness**: Machine Edition 0.6094 vs 0.5312 (+0.0781 gain, 95% CI [0.0156, 0.1719]).
* **Multi-Resolution Retrieval**: Machine Edition scored 0.75 correctness vs 0.375 for PDF/EPUB/RAG (eliminated resolution mismatch errors).
* **Token Overhead**: Machine Edition average total tokens: 988.84 vs 221.59 for RAG, 469.47 for PDF, and 478.47 for EPUB.
* **Latency**: 12.51 ms baseline average.

---

## 6. Reproducibility & Research Commands
* Verification: `python -m machine_edition_devkit.research.me_res_001 verify` -> PASS (6/6 checks)
* Re-scoring: `python -m machine_edition_devkit.research.me_res_001 score` -> PASS
* Analysis: `python -m machine_edition_devkit.research.me_res_001 analyze` -> PASS
* Test Suite: `pytest` -> 62/62 PASS

---

## 7. Known Follow-Ons
* `ME-DIST-001` (Public artifact distribution and verification)
* `ME-SROW-PUBLIC-DISTRIBUTION-RECONCILIATION-001`
* `ME-REF-001`
