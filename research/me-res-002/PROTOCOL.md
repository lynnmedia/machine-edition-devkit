# ME-RES-002 Protocol Specification

## 1. Research Question
> What properties of a genuine generative language model's behavior change when the same source information is supplied through PDF, EPUB, retrieval-corpus (RAG), and governed Machine Edition representation conditions?

## 2. Experimental Design
* **Design**: Controlled within-item comparative representation trial using a genuine neural generative language model.
* **Unit of Analysis**: Benchmark evaluation task (N=32 items across 8 families).
* **Replicates**: 3 independent executions per task-condition cell.
* **Total Executions**: 32 evaluation items x 4 conditions x 3 replicates = 384 evaluation calls (+ 32 calibration calls).
* **Execution Schedule**: Deterministic pseudo-randomized execution order using seed `2476533847` (derived from `winmedia.machine-edition-representation-benchmark.v0.1:ME-RES-002`).

## 3. Representation Conditions
* **C1 — PDF**: Extracted text stream and layout from `benchmark-document.pdf`.
* **C2 — EPUB**: Reflowable XHTML section text from `benchmark-document.epub`.
* **C3 — Naive RAG**: Top-4 retrieved chunks from `rag-corpus.json` using frozen sliding-window BM25 lexical ranking (target chunk: 250 chars, overlap: 40 chars).
* **C4 — Machine Edition**: Structured JSONL packages containing meaning units, definitions, boundaries, typed relationships, and provenance ledgers.

## 4. Model Configuration
* **Provider / Runtime**: `ollama` (`ollama-local`)
* **Model ID**: `qwen2.5:0.5b` (Qwen/Qwen2.5-0.5B-Instruct GGUF Q4_K_M)
* **Architecture Family**: `qwen2` (dense autoregressive transformer, 490M parameters)
* **Parameters**: `temperature = 0.0`, `top_p = 1.0`, `max_output_tokens = 600`, `seed = 2476533847`.
* **Cost**: `$0.00` (strictly local inference with zero metered spend).
* **Tools / Web / External Retrieval**: Disabled.

## 5. Standardized Answer Contract
Representation-neutral system instruction demanding structured JSON format:
* `answer`: factual response string or explicit lack-of-support statement.
* `source_references`: list of exact provenance IDs or document locations.
* `relationships`: typed subject-predicate-object triples.
* `constraints_observed`: boundary limits observed.
* `support_status`: `supported` | `partially_supported` | `unsupported`.

## 6. Gold Firewall
Generation runtime has zero access to gold adjudication files (`gold/answers.jsonl`, `gold/provenance.jsonl`, `gold/relationships.jsonl`, `gold/constraints.jsonl`).
