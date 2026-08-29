# Machine Edition Developer Kit (v0.1)

Reference developer kit implementing the 5 core responsibilities defined in **Machine Edition Specification v0.1**:

```text
inspect → validate → parse → query → compare
```

This Developer Kit proves that the public Machine Edition contract is actionable, inspectable, and computable by unaffiliated engineers without needing access to proprietary factory or generation internals.

---

## 1. Quick Start

### Installation

```bash
git clone https://github.com/lynnmedia/machine-edition-devkit.git
cd machine-edition-devkit
pip install -e ".[dev]"
```

### Reference Specimen Location

The authoritative public reference specimen derived from authorized public companion assets is located at:

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

### Complete 5-Responsibility Workflow

```python
from pathlib import Path
from machine_edition_devkit.inspect import inspect_package
from machine_edition_devkit.validate import MachineEditionValidator
from machine_edition_devkit.parse import MachineEdition
from machine_edition_devkit.queries import SampleQueryRunner
from machine_edition_devkit.comparison import ComparisonHarness

specimen_dir = Path("specimen/srow/package")

# 1. Inspect
summary = inspect_package(specimen_dir)
print(f"1. INSPECT: {summary.package_id} v{summary.version} ({summary.meaning_units_count} units)")

# 2. Validate against public schemas & invariants (C1-C7)
validator = MachineEditionValidator()
report = validator.validate_package(specimen_dir)
print(f"2. VALIDATE: {report.outcome}")

# 3. Parse into domain entity model
edition = MachineEdition.load(specimen_dir, validate=True)
mu = edition.get_unit("srow.ref.mu.003")
print(f"3. PARSE: Loaded unit '{mu.title}' [L{mu.resolution_level}]")

# 4. Query & Provenance Trace
prov = edition.provenance(mu)
print(f"4. QUERY: Claim provenance -> {prov.source_title} ({prov.source_url})")

# 5. Compare representations (PDF, EPUB, Naive RAG, Machine Edition)
harness = ComparisonHarness()
results = harness.run_all()
print("5. COMPARE: 16-task representation matrix executed successfully.")
```

### CLI Command Interfaces

```bash
# Run the 20-query reference pack
python -m machine_edition_devkit.queries run-all

# Run the 16-task 4-representation comparison trial
python -m machine_edition_devkit.comparison run

# View the representation property matrix
python -m machine_edition_devkit.comparison matrix

# Run ME-BENCH-001 frozen benchmark verification suite
python -m machine_edition_devkit.benchmark verify

# Run ME-BENCH-001 synthetic offline scorer fixtures
python -m machine_edition_devkit.benchmark test-scorer

# Run ME-RES-001 research trial verification suite
python -m machine_edition_devkit.research.me_res_001 verify

# Run ME-RES-001 statistical analysis and hypothesis reporting
python -m machine_edition_devkit.research.me_res_001 analyze
```

---

## 2. Machine Edition Representation Benchmark (ME-BENCH v0.1)

ME-BENCH-001 establishes a frozen, representation-controlled research evaluation instrument comparing **PDF**, **EPUB**, **Naive RAG**, and **Machine Edition** over an expanded 16-fact source corpus under guaranteed information parity:

* **Benchmark ID:** `winmedia.machine-edition-representation-benchmark.v0.1`
* **Task Corpus:** 40 tasks across 8 required task families (5 items each):
  1. `factual_retrieval`
  2. `relationship_retrieval`
  3. `hierarchy_preservation`
  4. `provenance_tracing`
  5. `boundary_constraint_recognition`
  6. `ambiguity_handling`
  7. `multi_resolution_retrieval`
  8. `unsupported_claim_detection`
* **Splits:** 8 calibration items (1 per family) and 32 evaluation items (4 per family).
* **Firewall Separation:** `tasks.jsonl` provides tasks without gold answers or scoring rules to prevent leakage.
* **Deterministic Offline Scorer:** Evaluates submissions across 7 dimensions (`correctness`, `provenance_completeness`, `unsupported_assertion_rate`, `semantic_invariant_preservation`, `relationship_accuracy`, `constraint_violations`, `failure_mode`) with a 14-token failure taxonomy.
* **Artifacts:** Documented and verified under `benchmark/` (`manifest.json`, `integrity-manifest.json`, `RIGHTS.md`, `THREATS-TO-VALIDITY.md`, `README.md`).

---

## 3. Representation Trial Study (ME-RES-001)

ME-RES-001 executes a controlled 384-run trial comparing **PDF**, **EPUB**, **Naive RAG**, and **Machine Edition** across 32 evaluation tasks under guaranteed information parity:
* **Protocol & Hypotheses:** Pre-registered directional hypotheses (H1-H5) frozen prior to evaluation.
* **Statistical Analysis:** Paired bootstrap estimation over 10,000 resamples showing statistically significant advantages in provenance completeness (+0.1719, 95% CI [0.0625, 0.3125]), semantic invariant preservation (+0.0781, 95% CI [0.0156, 0.1719]), and relationship accuracy (+0.0187, 95% CI [0.0000, 0.0437]).
* **Full Scientific Report:** Documented in [`research/me-res-001/report/ME-RES-001-REPORT.md`](file:///Users/studiobe/development/github/lynnmedia/machine-edition-devkit/research/me-res-001/report/ME-RES-001-REPORT.md).



---

## 2. Specification Binding

This Developer Kit implements the public contract defined in:
* **Specification:** `Machine Edition Specification v0.1`
* **Canonical URI:** `https://winmedia.com/machine-editions/specification/v0.1`
* **Authority Commit:** `c18dea5f378265cad37c0acf0c80f3969617876f` (`winmedia`)

---

## 3. Architecture Roadmap

* `MEDK-001`: Initial 5-responsibility architecture scaffold & reference interfaces.
* `MEDK-002`: Governed reference specimen expansion (`specimen/srow/package`).
* `MEDK-003`: Public schemas + full reference validator engine (C1-C7 conformance).
* `MEDK-003A`: Schema authority commit identity reconciliation.
* `MEDK-004`: Complete parser abstractions & TypeScript consumer example.
* `MEDK-005`: 20-query deterministic reference query pack & CLI runner.
* `MEDK-006`: Executable representation comparison benchmarks (PDF, EPUB, RAG, Machine Edition).
* `ME-BENCH-001`: Frozen Machine Edition Representation Benchmark v0.1 (40 tasks, 8 families, offline scorer, integrity manifest).
* `ME-BENCH-001A`: Benchmark freeze commit identity reconciliation.
* `ME-RES-001`: Controlled single-model representation trial across PDF, EPUB, RAG, and Machine Edition (384 evaluation runs, paired bootstrap analysis, and research report).

---

## 4. License

MIT License (c) 2026 Lynn Media.
