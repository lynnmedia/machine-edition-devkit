# Statistical Analysis Plan — ME-RES-002

## 1. Primary Analysis Unit
* Unit of Analysis: Benchmark Evaluation Task Item ($N = 32$).
* Replicate Aggregation: 3 replicates are averaged within task-condition before computing item-level paired contrasts.

## 2. Contrast Estimations
* Contrasts: $\text{ME} - \text{PDF}$, $\text{ME} - \text{EPUB}$, $\text{ME} - \text{RAG}$.
* Primary Estimator: Mean paired delta with 95% paired bootstrap confidence intervals ($10,000$ resamples, seed `2476533847`).
* Metrics:
  * `correctness` (higher is better)
  * `provenance_completeness` (higher is better)
  * `unsupported_assertion_rate` (lower is better)
  * `semantic_invariant_preservation` (higher is better)
  * `relationship_accuracy` (higher is better)
  * `constraint_violations` (lower is better)

## 3. Real-Model Special Analyses
* **Replicate Stability**: Measure identical-output rate and support-status agreement across replicates within cell.
* **Token Efficiency**: Report input tokens, output tokens, total tokens, and correctness/provenance per 1,000 input tokens.
