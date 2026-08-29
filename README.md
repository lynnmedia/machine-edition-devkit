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

### End-to-End Developer Workflow

```python
from pathlib import Path
from machine_edition_devkit.inspect import inspect_package
from machine_edition_devkit.validate import MachineEditionValidator
from machine_edition_devkit.parse import MachineEdition
from machine_edition_devkit.queries import SampleQueryRunner

specimen_dir = Path("specimen/srow/package")

# 1. Inspect
summary = inspect_package(specimen_dir)
print(f"Package: {summary.package_id} v{summary.version} ({summary.meaning_units_count} units)")

# 2. Validate against public schemas & invariants (C1-C7)
validator = MachineEditionValidator()
report = validator.validate_package(specimen_dir)
print(f"Outcome: {report.outcome}")
print(report.render_summary())

# 3. Load into domain entity model
edition = MachineEdition.load(specimen_dir, validate=True)

# 4. Retrieve atomic meaning units and trace provenance
mu = edition.get_unit("srow.ref.mu.003")
print(f"Meaning Unit [L{mu.resolution_level}]: {mu.title}")
print(f"Claim: {mu.claim}")
prov = edition.provenance(mu)
print(f"Source: {prov.source_title} ({prov.source_url})")

# 5. Follow inter-unit relationships
outgoing = edition.related("srow.ref.mu.002", direction="outgoing")
print(f"Relationship: {outgoing[0].subject_id} --({outgoing[0].predicate})--> {outgoing[0].object_id}")

# 6. Run the 20-query deterministic sample pack
runner = SampleQueryRunner()
results = runner.run_all(edition)
print(runner.render_matrix(results))
```

### Running Queries from the CLI

```bash
# List all 20 sample queries
python -m machine_edition_devkit.queries list

# Run a single query by ID
python -m machine_edition_devkit.queries run Q015

# Run the complete test and acceptance matrix
python -m machine_edition_devkit.queries run-all
```

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
* `MEDK-006`: Executable representation comparison benchmarks.

---

## 4. License

MIT License (c) 2026 Lynn Media.
