# ME-RES-002: Statistical Claim Calibration & Publication Semantics

## 1. Overview
This document records the official calibrated interpretation of experimental findings from the ME-RES-002 real generative model trial (`qwen2.5:0.5b`, Qwen 2.5 0.5B Instruct, 490M parameters).

All headline claims and publication interpretations must adhere strictly to these determinations.

---

## 2. Hypothesis Calibrations

### H1 — Provenance Tracing
* **Observed**: ME mean = `0.8490`, PDF/EPUB/RAG mean = `0.7812`.
* **Paired Delta vs RAG**: `+0.0677` (95% Bootstrap CI: `[-0.0573, +0.1927]`, 4 wins / 27 ties / 1 loss).
* **Calibrated Classification**: `DIRECTIONALLY_SUPPORTED_BUT_INCONCLUSIVE`.
* **Publication Rule**: Because the confidence interval crosses zero, do NOT state "H1 CONFIRMED". State that Machine Edition produced a higher point estimate and reduced provenance omissions from 21 to 12, but does not establish a statistically resolved advantage for this model.

### H2 — Relationship Retrieval
* **Observed**: PDF = `0.8750`, EPUB = `0.8750`, RAG = `0.8750`, ME = `0.8750`.
* **Paired Delta**: `0.0000` (95% CI: `[0.0000, 0.0000]`).
* **Calibrated Classification**: `NOT_SUPPORTED_NO_OBSERVED_DIFFERENCE`.
* **Publication Rule**: Do NOT state "H2 CONFIRMED". The model trial showed identical relationship retrieval accuracy across all four representations.

### H3 — Boundaries and Semantic Invariants
* **Observed**: PDF = `0.2969`, EPUB = `0.2656`, ME = `0.2344`, RAG = `0.2188`. Constraint violations = `0.0000` across all four conditions.
* **Paired Delta vs RAG**: `+0.0156` (95% CI: `[-0.1562, +0.1719]`).
* **Calibrated Classification**: `PARTIALLY_DIRECTIONALLY_SUPPORTED_BUT_INCONCLUSIVE`.
* **Publication Rule**: Do NOT describe this as a general ME invariant-preservation advantage. ME slightly exceeded RAG (+0.0156) but not PDF or EPUB.

### H4 — Unsupported Claims
* **Observed**: Unsupported assertion rate was `0.0000` across all four conditions.
* **Calibrated Classification**: `CONSISTENT_WITH_HYPOTHESIS_NO_DIFFERENTIAL_EFFECT`.
* **Publication Rule**: This demonstrates zero unsupported assertions were generated under this trial; it does not claim ME reduced unsupported assertions relative to other conditions.

### H5 — Factual Retrieval Neutrality
* **Observed Correctness**: PDF = `0.2969`, EPUB = `0.2656`, ME = `0.2344`, RAG = `0.2188`.
* **Calibrated Classification**: `DESCRIPTIVE_MIXED_RESULT_NO_ME_SUPERIORITY`.
* **Publication Rule**: State that factual correctness differed by consumption path under shared information parity: PDF produced the highest point estimate, followed by EPUB, Machine Edition, and RAG.

---

## 3. Canonical ME-RES-002 Result Statement
> ME-RES-002 tested one small local instruction-tuned generative model (`qwen2.5:0.5b`) across frozen PDF, EPUB, lexical-RAG, and Machine Edition representation conditions. The trial did not establish a general overall accuracy advantage for Machine Editions. The Machine Edition condition produced the highest provenance-completeness point estimate and the greatest number of zero-defect clean passes, while PDF produced the highest overall correctness point estimate. Relationship accuracy and unsupported-assertion behavior showed no differential effect. Machine Edition contexts were substantially larger than the other conditions (~2,789 tokens vs ~415 for RAG). Results should therefore be interpreted as model- and protocol-specific evidence concerning representational affordances, not as a universal ranking of publication formats.
