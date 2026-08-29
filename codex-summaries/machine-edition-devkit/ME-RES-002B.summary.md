# ME-RES-002B — Summary

## HDCP ID and Title
* **ID**: `ME-RES-002B`
* **Title**: `ME-RES-002 Statistical Claim Calibration and Publication Semantics`

## Repository and Branch
* **Repository**: `machine-edition-devkit`
* **Branch**: `main`

## Opening Evidence
* **Precursor**: `ME_RES_002_EVIDENCE_PACKAGE_COMPLETE`
* **Execution Class**: `REPORTING_RECONCILIATION_ONLY`

---

## 1. Calibrated Hypotheses Evaluation
* **H1 (Provenance)**: `DIRECTIONALLY_SUPPORTED_BUT_INCONCLUSIVE`.
  * Point estimate: ME 0.8490 vs RAG 0.7812 (+0.0677 delta).
  * 95% paired bootstrap CI: `[-0.0573, +0.1927]` (crosses zero).
  * Reduced provenance omissions from 21 to 12. Does not establish a statistically resolved advantage for this model.
* **H2 (Relationships)**: `NOT_SUPPORTED_NO_OBSERVED_DIFFERENCE`.
  * Accuracy was identical across all four formats (`0.8750`).
* **H3 (Boundaries & Invariants)**: `PARTIALLY_DIRECTIONALLY_SUPPORTED_BUT_INCONCLUSIVE`.
  * ME slightly exceeded RAG (+0.0156), but not PDF (0.2969) or EPUB (0.2656); constraint violations were 0.0000 across all.
* **H4 (Unsupported Claims)**: `CONSISTENT_WITH_HYPOTHESIS_NO_DIFFERENTIAL_EFFECT`.
  * 0.0000 unsupported assertion rate across all four conditions.
* **H5 (Factual Retrieval Neutrality)**: `DESCRIPTIVE_MIXED_RESULT_NO_ME_SUPERIORITY`.
  * Factual correctness differed by representation: PDF (0.2969) > EPUB (0.2656) > ME (0.2344) > RAG (0.2188).

---

## 2. Canonical Public Conclusion
> ME-RES-002 tested one small local instruction-tuned generative model (`qwen2.5:0.5b`) across frozen PDF, EPUB, lexical-RAG, and Machine Edition representation conditions. The trial did not establish a general overall accuracy advantage for Machine Editions. The Machine Edition condition produced the highest provenance-completeness point estimate and the greatest number of zero-defect clean passes, while PDF produced the highest overall correctness point estimate. Relationship accuracy and unsupported-assertion behavior showed no differential effect. Machine Edition contexts were substantially larger than the other conditions (~2,789 tokens vs ~415 for RAG). Results should therefore be interpreted as model- and protocol-specific evidence concerning representational affordances, not as a universal ranking of publication formats.

---

## 3. Determination
* **Determination**: `ME_RES_002_PUBLICATION_CLAIMS_CALIBRATED`
