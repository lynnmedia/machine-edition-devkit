# ME-RES-001 Protocol Specification

## 1. Research Question
> What properties of model performance change when the same source information is supplied through PDF, EPUB, retrieval-corpus (RAG), and governed Machine Edition representation conditions?

## 2. Experimental Design
* **Design**: Controlled within-item comparative representation trial.
* **Unit of Analysis**: Benchmark evaluation task (N=32 items across 8 families).
* **Replicates**: 3 independent executions per task-condition cell.
* **Total Executions**: 32 evaluation items x 4 conditions x 3 replicates = 384 evaluation calls (+ 32 calibration calls).
* **Randomization**: Deterministic pseudo-random execution order using seed `44527555` (derived from first 8 hex characters of `benchmark-source.md` SHA-256: `02a76fc3`).

## 3. Representation Conditions
* **C1 — PDF**: Extracted text stream and document lines from `benchmark-document.pdf`.
* **C2 — EPUB**: Reflowable XHTML section text from `benchmark-document.epub`.
* **C3 — Naive RAG**: Top-4 retrieved chunks from `rag-corpus.json` using frozen sliding-window BM25 lexical ranking (target: 250 chars, overlap: 40 chars).
* **C4 — Machine Edition**: Structured JSONL packages containing meaning units, definitions, boundaries, typed relationships, and provenance ledgers.

## 4. Model Configuration
* **Provider**: `local-deterministic-reference`
* **Model ID**: `eval-model-v01-deterministic`
* **Parameters**: `temperature = 0.0`, `top_p = 1.0`, `max_output_tokens = 600`, `seed = 44527555`.
* **Tools / Web / Memory**: Disabled.

## 5. Standardized Answer Contract
Representation-neutral system instruction requiring JSON formatted answers with:
* `answer`: factual response string or explicit lack-of-support statement.
* `source_references`: exact provenance IDs or document locations.
* `relationships`: typed subject-predicate-object triples.
* `constraints_observed`: boundary limits observed.
* `support_status`: `supported` | `partially_supported` | `unsupported`.

## 6. Gold Firewall
Zero gold answer, accepted variant, prohibited claim, or scoring rule is accessible to the context builder or inference runtime.
