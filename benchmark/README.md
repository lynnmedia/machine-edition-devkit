# Machine Edition Representation Benchmark (ME-BENCH v0.1)

## Purpose & Research Question
> What properties of machine consumption change when the same source information is represented as a conventional document (PDF), EPUB publication, retrieval corpus (RAG), or governed Machine Edition?

ME-BENCH v0.1 is an evaluation instrument. It does not itself establish that one representation universally outperforms another.
RAG systems vary substantially. The frozen RAG condition is one transparent reproducible baseline, not a claim about every possible retrieval architecture.

## Corpus Lineage & Rights
* **Lineage**: `SROW Public Companion v0.1 (archive sha256: 0cd42e724bcd7d4b54c0f850a51ef7b875152cd01f7a20f5b7b34e0d73b5d181) -> SROW Public Reference Specimen -> MEDK-006 -> ME-BENCH-001`
* **Rights**: Creative Commons Attribution 4.0 International (CC BY 4.0) within authorized public companion scope (see `RIGHTS.md`).
* **Source Hash**: `cceb69fea9bfb4a2c84f8829bd7bff5cd185037c21023b37ab4ae144d7b32509`

## Representation Conditions
1. **PDF** (`benchmark/representations/pdf/`): Fixed-layout document (`benchmark-document.pdf`).
2. **EPUB** (`benchmark/representations/epub/`): Standard reflowable EPUB 3.0 publication (`benchmark-document.epub`).
3. **Naive RAG** (`benchmark/representations/rag/`): Sliding-window lexical chunks (`rag-corpus.json`).
4. **Machine Edition** (`benchmark/representations/machine-edition/`): Specimen package adhering to Machine Edition Specification v0.1 (`package/`).

## Task Families & Splits
Total Items: 40 (8 calibration + 32 evaluation).

1. `factual_retrieval` (5 items: 1 calibration, 4 evaluation)
2. `relationship_retrieval` (5 items: 1 calibration, 4 evaluation)
3. `hierarchy_preservation` (5 items: 1 calibration, 4 evaluation)
4. `provenance_tracing` (5 items: 1 calibration, 4 evaluation)
5. `boundary_constraint_recognition` (5 items: 1 calibration, 4 evaluation)
6. `ambiguity_handling` (5 items: 1 calibration, 4 evaluation)
7. `multi_resolution_retrieval` (5 items: 1 calibration, 4 evaluation)
8. `unsupported_claim_detection` (5 items: 1 calibration, 4 evaluation)

## Gold Firewall
* Experimental runners consume `tasks.jsonl` and representation conditions.
* Gold adjudication ledgers (`gold/answers.jsonl`, `gold/provenance.jsonl`, `gold/relationships.jsonl`, `gold/constraints.jsonl`) are strictly separated to prevent leakage.

## Reproduction
```bash
# Verify integrity, parity, schema validity, and scorer
python -m machine_edition_devkit.benchmark verify

# Rebuild all representations deterministically
python -m machine_edition_devkit.benchmark rebuild

# Run offline scorer test fixture suite
python -m machine_edition_devkit.benchmark test-scorer
```
