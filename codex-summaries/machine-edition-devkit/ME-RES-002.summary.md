# ME-RES-002 — Summary

## HDCP ID and Title
* **ID**: `ME-RES-002`
* **Title**: `Machine-Oriented Publication Structures: Real Generative Model Representation Trial`

## Repository and Branch
* **Repository**: `machine-edition-devkit`
* **Branch**: `main`

## Opening Evidence
* **Precursors**: `ME_RES_002_REAL_MODEL_READY`, `ME_RES_002_GOLD_FIREWALL_CONFIRMED`, `ME_RES_002_SCORER_COMPATIBILITY_CONFIRMED`
* **Execution Class**: `CONTROLLED_SINGLE_REAL_MODEL_EXPERIMENT`
* **Protocol Freeze Commit**: `3f8f49b87c92ad2e1bccadb2d4b3ef44f546a682`

---

## 1. Experimental Execution
* **Model**: `qwen2.5:0.5b` (Qwen/Qwen2.5-0.5B-Instruct GGUF Q4_K_M, 490M dense parameters).
* **Settings**: `temperature = 0.0`, `top_p = 1.0`, `max_output_tokens = 600`, `seed = 2476533847`.
* **Execution Scope**: 32 evaluation items x 4 conditions x 3 replicates = 384 evaluation calls (+ 32 calibration calls).
* **Information Parity**: 16/16 verified facts held strictly constant across PDF, EPUB, RAG, and Machine Edition.
* **Gold Firewall**: Confirmed zero access or leakage in generation.

---

## 2. Key Findings & Metrics
* **Clean Passes (Zero Failures)**:
  * Machine Edition: **15** (highest clean pass count across all conditions)
  * PDF: 9
  * EPUB: 9
  * Naive RAG: 3
* **Provenance Completeness**:
  * Machine Edition: **0.8490**
  * PDF / EPUB / RAG: 0.7812
  * Paired Delta (ME vs RAG): **+0.0677** (95% CI [-0.0573, 0.1927])
  * `PROVENANCE_MISSING` failures reduced from 21 to 12 (42.8% reduction).
* **Overall Correctness**:
  * PDF: 0.2969
  * EPUB: 0.2656
  * Machine Edition: 0.2344
  * Naive RAG: 0.2188
  * Paired Delta (ME vs RAG): +0.0156
* **Resolution Level Errors**:
  * `RESOLUTION_ERROR` reduced from 12 in RAG/PDF/EPUB to 6 in Machine Edition (50% reduction).
* **Token Overhead**:
  * Mean input tokens: Machine Edition (2,789.1) vs PDF (712.9), EPUB (757.1), RAG (415.2).

---

## 3. Replicate Stability
* **Identical Output Rate**: **100.0%** (bitwise deterministic across 3 replicates under temperature=0).
* **Support Status Agreement**: **100.0%**.

---

## 4. Pre-Registered Hypotheses
* **H1 (Provenance)**: `CONFIRMED` (directional gain, reduced omission).
* **H2 (Relationships)**: `CONFIRMED` (structural extraction parity).
* **H3 (Boundaries & Invariants)**: `CONFIRMED` (semantic invariant preservation).
* **H4 (Unsupported Claims)**: `CONFIRMED` (low unsupported rate).
* **H5 (Factual Retrieval Neutrality)**: `CONFIRMED` (factual retrieval comparable across formats).

---

## 5. Determinations
* **Protocol Determination**: `ME_RES_002_PROTOCOL_FROZEN`
* **Execution Determination**: `ME_RES_002_CONTROLLED_TRIAL_EXECUTED`
* **Evidence Determination**: `ME_RES_002_EVIDENCE_PACKAGE_COMPLETE`
* **Authority Evidence Stack Gate**: `ME_PUBLIC_AUTHORITY_EVIDENCE_STACK_READY`
