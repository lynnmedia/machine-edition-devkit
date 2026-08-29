# Machine Edition Developer Kit (v0.1)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Reference developer kit, validation engine, parser, query suite, evaluation benchmark (`ME-BENCH-001`), and research trial execution packages implementing the 5 core responsibilities defined in **Machine Edition Specification v0.1**:

```text
inspect → validate → parse → query → compare
```

---

## 1. What is this?

A **Machine Edition** is a structured, computable publication package designed for reliable, auditable, and multi-resolution consumption by automated AI agents and software systems alongside human readers.

This Developer Kit serves as the canonical open reference implementation of the public **Machine Edition Specification v0.1**, demonstrating that Machine Edition packages can be inspected, validated, queried, and evaluated without proprietary dependencies.

* **Conceptual Authority**: [WinMedia](https://winmedia.com) (`https://winmedia.com/machine-editions/specification/v0.1`)
* **Executable Implementation**: [GitHub](https://github.com/lynnmedia/machine-edition-devkit) (`lynnmedia/machine-edition-devkit`)
* **Evaluation Benchmark**: `ME-BENCH-001` (`winmedia.machine-edition-representation-benchmark.v0.1`)
* **Research Trials**:
  * `ME-RES-001`: Deterministic reference-harness qualification trial
  * `ME-RES-002`: Controlled real generative model trial (`qwen2.5:0.5b`)

---

## 2. Quick Start

### Installation

```bash
git clone https://github.com/lynnmedia/machine-edition-devkit.git
cd machine-edition-devkit
pip install -e ".[dev]"
```

### Reference Specimen

An authoritative public reference specimen derived from authorized public companion material is located at:

```text
specimen/
  srow/
    package/                     <-- Normative Machine Edition Package
      manifest.json
      meaning-units.jsonl
      provenance.jsonl
      definitions.jsonl
      boundaries.jsonl
      relationships.jsonl
      full-preview.md
      LICENSE.txt
    SOURCE.json                  <-- Authority provenance & archive SHA-256
    DERIVATION.json              <-- Normalization log
    CONFORMANCE-CROSSWALK.md     <-- Audit crosswalk against Spec v0.1 C1-C7
```

---

## 3. Validate Specimen

Inspect and validate package compliance against Machine Edition Specification v0.1 JSON schemas (C1-C7) and structural invariants:

```python
from pathlib import Path
from machine_edition_devkit.inspect import inspect_package
from machine_edition_devkit.validate import MachineEditionValidator

specimen_dir = Path("specimen/srow/package")

# 1. Inspect
summary = inspect_package(specimen_dir)
print(f"INSPECT: {summary.package_id} v{summary.version} ({summary.meaning_units_count} units)")

# 2. Validate against C1-C7 schemas and invariants
validator = MachineEditionValidator()
report = validator.validate_package(specimen_dir)
print(f"VALIDATE: {report.outcome} (Errors: {len(report.errors)})")
```

---

## 4. Parse & Query Specimen

Load the edition into a structured entity model and perform deterministic queries with provenance tracking:

```python
from machine_edition_devkit.parse import MachineEdition

edition = MachineEdition.load("specimen/srow/package", validate=True)
unit = edition.get_unit("srow.ref.mu.003")
print(f"PARSE: Loaded '{unit.title}' [Resolution Level L{unit.resolution_level}]")

# Provenance tracing
prov = edition.provenance(unit)
print(f"PROVENANCE: {prov.source_title} ({prov.source_url})")

# Typed relationships
rels = edition.relationships_for(unit)
for r in rels:
    print(f"RELATIONSHIP: {r.subject} --[{r.predicate}]--> {r.object}")
```

CLI Interface:
```bash
# Run the 20-query reference pack
python -m machine_edition_devkit.queries run-all
```

---

## 5. Run Representation Comparison

Compare Machine Edition against PDF, EPUB, and Naive RAG representation formats across a 16-task representation matrix:

```bash
# Run comparison trial
python -m machine_edition_devkit.comparison run

# Display representation property matrix
python -m machine_edition_devkit.comparison matrix
```

---

## 6. Reproduce Benchmark (ME-BENCH v0.1)

ME-BENCH-001 is a frozen research benchmark comparing **PDF**, **EPUB**, **Naive RAG**, and **Machine Edition** across 40 tasks (8 calibration, 32 evaluation across 8 task families) over a 16-fact source corpus under guaranteed 100% information parity.

```bash
# Verify artifact integrity and 16/16 information parity
python -m machine_edition_devkit.benchmark verify

# Run synthetic offline scorer test fixtures
python -m machine_edition_devkit.benchmark test-scorer
```

---

## 7. Read Research

### ME-RES-001: Deterministic Reference-Harness Qualification Trial
* **Purpose**: Methodological qualification of the benchmark harness, 4 representation adapters, offline scoring engine, and 10,000-resample paired bootstrap pipeline.
* **Classification**: `deterministic reference-harness trial` (`ME_RES_V01_REFERENCE_HARNESS_CONFIRMED`).
* **Report**: [`research/me-res-001/report/ME-RES-001-REPORT.md`](file:///Users/studiobe/development/github/lynnmedia/machine-edition-devkit/research/me-res-001/report/ME-RES-001-REPORT.md)

### ME-RES-002: Real Generative Model Representation Trial
* **Purpose**: Controlled empirical evaluation using a genuine pretrained neural language model (`qwen2.5:0.5b`, Qwen 2.5 0.5B Instruct, 490M parameters via local Ollama) across 384 evaluation calls.
* **Key Findings**:
  * Machine Edition produced the highest provenance-completeness point estimate (0.8490 vs 0.7812 for RAG, paired delta +0.0677, 95% CI [-0.0573, +0.1927]) and reduced provenance omissions from 21 to 12.
  * Machine Edition produced 5x more clean error-free responses than RAG (15 passes vs 3).
  * PDF full-text extraction achieved the highest factual correctness point estimate (0.2969 vs 0.2656 EPUB, 0.2344 ME, 0.2188 RAG).
  * Machine Edition packages required higher token volume (~2,789 tokens vs ~415 for RAG).
* **Report**: [`research/me-res-002/report/ME-RES-002-REPORT.md`](file:///Users/studiobe/development/github/lynnmedia/machine-edition-devkit/research/me-res-002/report/ME-RES-002-REPORT.md)

```bash
# Verify ME-RES-002 research integrity
python -m machine_edition_devkit.research.me_res_002 verify

# Display statistical contrast tables and calibrated hypothesis conclusions
python -m machine_edition_devkit.research.me_res_002 analyze
```

---

## 8. Citation

```bibtex
@software{lynnmedia_medk_2026,
  author = {{Lynn Media}},
  title = {Machine Edition Developer Kit (v0.1)},
  year = {2026},
  url = {https://github.com/lynnmedia/machine-edition-devkit},
  note = {Implementing Machine Edition Specification v0.1, WinMedia}
}
```

---

## 9. License

MIT License (c) 2026 Lynn Media.
