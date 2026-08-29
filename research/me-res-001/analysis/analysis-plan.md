# Statistical Analysis Plan — ME-RES-001

## 1. Primary Analysis Unit
* Unit of Analysis: Benchmark Evaluation Task Item (N = 32).
* Replicate Aggregation: 3 replicates are averaged within task-condition before computing item-level paired contrasts.

## 2. Contrast Estimations
* Contrasts: ME - PDF, ME - EPUB, ME - RAG.
* Primary Estimator: Mean paired delta with 95% paired bootstrap confidence intervals (10,000 resamples, seed 44527555).
* Metrics:
  * `correctness` (higher is better)
  * `provenance_completeness` (higher is better)
  * `unsupported_assertion_rate` (lower is better)
  * `semantic_invariant_preservation` (higher is better)
  * `relationship_accuracy` (higher is better)
  * `constraint_violations` (lower is better)

## 3. Decision Rules
* Confidence intervals strictly excluding zero confirm directional treatment effects.
* Factual retrieval neutrality tested via two-sided bound equivalence.
