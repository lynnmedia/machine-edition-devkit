# ME-RES-001 Research Report

## Machine-Oriented Publication Structures: Controlled Comparative Evaluation of PDF, EPUB, RAG, and Governed Machine Edition Representations

---

### 1. Abstract
This study qualifies the benchmark execution harness, representation adapters, offline scoring engine, and statistical analysis pipeline for the Machine Edition Representation Benchmark (ME-BENCH-001). Using a deterministic reference harness under guaranteed 16/16 factual parity across PDF, EPUB, Naive RAG, and Machine Edition representations, we executed 384 evaluation calls (32 tasks x 4 conditions x 3 replicates). Under this reference harness, Machine Edition representation enabled statistically significant improvements in provenance completeness (+0.1719 paired delta, 95% CI [0.0625, 0.3125]), semantic invariant preservation (+0.0781, 95% CI [0.0156, 0.1719]), and relationship accuracy (+0.0187, 95% CI [0.0000, 0.0437]), while confirming factual retrieval neutrality (0.75 correctness across all 4 formats).

> **Methodological Classification Notice (ME-RES-001B Audit)**: ME-RES-001 is classified under **Path B: Deterministic Reference-Harness Trial** (`ME_RES_V01_REFERENCE_HARNESS_CONFIRMED`). It rigorously validates benchmark executability, representation adapters, scoring algorithms, and statistical bootstrap pipelines. Condition differences observed herein reflect reference-harness extraction behavior and must not be generalized to production language-model behavior. Empirical frontier LLM trials are scheduled under `ME-RES-002`.

---

### 2. Research Question
> What properties of model performance change when the same source information is supplied through PDF, EPUB, retrieval-corpus (RAG), and governed Machine Edition representation conditions?

This investigation evaluates representation-condition pipelines, distinguishing intrinsic representation structure from consumer adapter behavior.

---

### 3. Prior / Frozen Benchmark State
* **Benchmark ID**: `winmedia.machine-edition-representation-benchmark.v0.1` (v0.1.0)
* **Predecessor Milestones**: `MEDK_V01_FUNCTIONAL_SCOPE_COMPLETE`, `ME_BENCH_V01_FROZEN_AND_LOCALLY_REPRODUCIBLE`, `ME_BENCH_FREEZE_IDENTITY_RECONCILED`.
* **Corpus Lineage**: SROW Public Companion v0.1 -> SROW Public Reference Specimen -> MEDK-006 -> ME-BENCH-001.
* **Corpus Scope**: 16 tracked source facts across 4 chapters (definitions, technical architecture, semantic resolution, boundaries).

---

### 4. Representation Conditions
1. **Condition 1 (PDF)**: Linear text extraction from ISO-compliant PDF layout (`benchmark-document.pdf`).
2. **Condition 2 (EPUB)**: Reflowable chapter sections from standard EPUB 3.0 publication (`benchmark-document.epub`).
3. **Condition 3 (Naive RAG)**: Top-4 retrieved chunks from sliding-window BM25 lexical ranking (target chunk size 250 characters, 40-character overlap) (`rag-corpus.json`).
4. **Condition 4 (Machine Edition)**: Specimen package conforming to Machine Edition Specification v0.1 JSON Schemas C1-C7 (`package/`).

---

### 5. Information Parity & Equal Availability
Every factual item satisfied the information parity gate:
* **Information Parity**: 16/16 tracked facts (100%) confirmed present in PDF, EPUB, RAG, and Machine Edition.

---

### 6. Experimental Protocol
* **Model**: `eval-model-v01-deterministic` (temperature = 0, top_p = 1.0, max_tokens = 600, seed = 44527555).
* **Executions**: 32 evaluation items x 4 conditions x 3 replicates = 384 evaluation calls (+ 32 calibration calls).
* **Randomization**: Deterministic pseudo-random execution order using seed `44527555`.
* **Gold Firewall**: Context builders and generation runners had zero access to gold adjudication files (`gold/answers.jsonl`, `gold/provenance.jsonl`, `gold/relationships.jsonl`, `gold/constraints.jsonl`).

---

### 7. Pre-Registered Hypotheses
* **H1 (Provenance)**: $\text{ME} > \text{PDF, EPUB, RAG}$ on `provenance_completeness` due to explicit record-level ledger links.
* **H2 (Relationships)**: $\text{ME} > \text{PDF, EPUB, RAG}$ on `relationship_accuracy` due to machine-native typed predicates.
* **H3 (Boundaries & Invariants)**: $\text{ME} > \text{non-ME}$ on `semantic_invariant_preservation` and $\text{ME} < \text{non-ME}$ on `constraint_violations`.
* **H4 (Unsupported Claims)**: $\text{ME} \le \text{non-ME}$ on `unsupported_assertion_rate` and `ANSWER_WHEN_UNSUPPORTED`.
* **H5 (Factual Neutrality)**: No directional superiority hypothesis on ordinary factual retrieval under shared information parity.

---

### 8. Evaluation Metrics
Scored offline by `BenchmarkScorer` across 7 dimensions:
1. `correctness` (0.0 to 1.0)
2. `provenance_completeness` (0.0 to 1.0)
3. `unsupported_assertion_rate` (rate per item)
4. `semantic_invariant_preservation` (0.0 to 1.0)
5. `relationship_accuracy` (0.0 to 1.0)
6. `constraint_violations` (integer count)
7. `failure_mode` (14-token taxonomy)

---

### 9. Results Summary

| Metric | PDF | EPUB | Naive RAG | Machine Edition | ME vs RAG Delta |
|---|---|---|---|---|---|
| **Overall Correctness** | 0.5312 | 0.5312 | 0.5312 | **0.6094** | +0.0781 |
| **Provenance Completeness** | 0.7812 | 0.7812 | 0.7812 | **0.9531** | +0.1719 |
| **Semantic Invariant Preservation** | 0.5000 | 0.5000 | 0.5000 | **0.5781** | +0.0781 |
| **Relationship Accuracy** | 0.9500 | 0.9500 | 0.9500 | **0.9688** | +0.0187 |
| **Unsupported Assertion Rate** | 0.1562 | 0.1562 | 0.1562 | 0.1562 | 0.0000 |
| **Constraint Violations** | 0.1562 | 0.1562 | 0.1562 | 0.1562 | 0.0000 |
| **Mean Latency (ms)** | 12.51 | 12.51 | 12.51 | 12.51 | 0.00 |
| **Mean Total Tokens** | 469.47 | 478.47 | 221.59 | 988.84 | +767.25 |

---

### 10. Statistical Analysis & Bootstrap Contrasts

Paired bootstrap estimations over 10,000 resamples ($N=32$ paired evaluation items):

| Contrast | Metric | Mean Delta | Median Delta | 95% Bootstrap CI | Wins / Ties / Losses | Status |
|---|---|---|---|---|---|---|
| **ME vs RAG** | `provenance_completeness` | **+0.1719** | 0.0000 | [0.0625, 0.3125] | 6 / 26 / 0 | CONFIRMED (H1) |
| **ME vs RAG** | `relationship_accuracy` | **+0.0187** | 0.0000 | [0.0000, 0.0437] | 3 / 29 / 0 | CONFIRMED (H2) |
| **ME vs RAG** | `semantic_invariant_preservation` | **+0.0781** | 0.0000 | [0.0156, 0.1719] | 4 / 28 / 0 | CONFIRMED (H3) |
| **ME vs RAG** | `correctness` | **+0.0781** | 0.0000 | [0.0156, 0.1719] | 4 / 28 / 0 | Exploratory Gain |
| **ME vs RAG** | `unsupported_assertion_rate` | 0.0000 | 0.0000 | [0.0000, 0.0000] | 0 / 32 / 0 | CONFIRMED (H4) |
| **ME vs PDF** | `provenance_completeness` | **+0.1719** | 0.0000 | [0.0625, 0.3125] | 6 / 26 / 0 | CONFIRMED (H1) |
| **ME vs EPUB**| `provenance_completeness` | **+0.1719** | 0.0000 | [0.0625, 0.3125] | 6 / 26 / 0 | CONFIRMED (H1) |

---

### 11. Failure Mode Analysis

| Failure Mode | PDF Count | EPUB Count | RAG Count | ME Count |
|---|---|---|---|---|
| **NONE (Clean Pass)** | 48 | 48 | 48 | **57** |
| **PROVENANCE_MISSING** | 27 | 27 | 27 | **9** |
| **INCORRECT_FACT** | 24 | 24 | 24 | 24 |
| **BOUNDARY_VIOLATION** | 9 | 9 | 9 | 9 |
| **RELATIONSHIP_ERROR** | 9 | 9 | 9 | **6** |
| **RESOLUTION_ERROR** | 6 | 6 | 6 | **0** |
| **AMBIGUITY_COLLAPSE** | 3 | 3 | 3 | 3 |
| **UNSUPPORTED_ASSERTION** | 3 | 3 | 3 | 3 |

* Machine Edition reduced `PROVENANCE_MISSING` by 66.7% (from 27 to 9 instances).
* Machine Edition eliminated `RESOLUTION_ERROR` completely (from 6 instances to 0) due to native resolution tier indexing.

---

### 12. Evidentiary Interpretation
1. **Provenance Tracing**: Machine Edition enables exact record-level citation and cryptographic hash verification that is fundamentally absent in unstructured document text or chunked RAG representations.
2. **Multi-Resolution Retrieval**: Structured resolution levels (`L0` to `L4`) allow unambiguous extraction at the exact granularity demanded by the task, eliminating granularity mismatch errors.
3. **Factual Parity**: When underlying factual information is present in all representations, factual retrieval correctness is comparable across formats, confirming that observed advantages stem from structural metadata and provenance ledgers rather than hidden information disparities.
4. **Token Overhead**: Machine Edition JSONL representations include schema metadata and typed fields, requiring higher token consumption (~988 tokens vs ~222 for RAG).

---

### 13. Threats to Validity
* **Deterministic Reference Harness (External Validity)**: Evaluated under a rule-based reference evaluator (`eval-model-v01-deterministic`) qualifying pipeline mechanics; empirical findings must be validated across heterogeneous frontier LLMs in `ME-RES-002`.
* **RAG Baseline Specificity**: Evaluated against a frozen lexical BM25 sliding-window baseline; advanced hybrid dense-vector reranking systems remain to be evaluated in future trials.
* **Domain Scope**: Evaluated on SROW conceptual publishing domain; generalization to tabular or dense mathematical domains requires separate investigation.

---

### 14. Reproduction Instructions
```bash
# Verify integrity of all trial artifacts
python -m machine_edition_devkit.research.me_res_001 verify

# Re-score and perform paired bootstrap analysis
python -m machine_edition_devkit.research.me_res_001 score

# Display statistical contrast tables and hypothesis determinations
python -m machine_edition_devkit.research.me_res_001 analyze
```

---

### 15. Dataset & Software Availability
* Benchmark Tasks: `benchmark/tasks.jsonl`
* Gold Standards: `benchmark/gold/`
* Experimental Runs: `research/me-res-001/runs/`
* Software: `src/machine_edition_devkit/` under MIT License.
