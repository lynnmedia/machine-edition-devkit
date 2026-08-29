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

### 5-Step Core Workflow

```python
from pathlib import Path
from machine_edition_devkit.inspect import inspect_package
from machine_edition_devkit.validate import MachineEditionValidator
from machine_edition_devkit.parse import MachineEditionParser
from machine_edition_devkit.query import MachineEditionQueryEngine
from machine_edition_devkit.compare import RepresentationComparator

specimen_dir = Path("specimen/srow/package")

# 1. Inspect
summary = inspect_package(specimen_dir)
print(f"Package: {summary.package_id} v{summary.version} ({summary.meaning_units_count} units)")

# 2. Validate against public schemas & invariants (C1-C7)
validator = MachineEditionValidator()
report = validator.validate_package(specimen_dir)
print(f"Outcome: {report.outcome}")
print(report.render_summary())

# 3. Parse into domain entities
parser = MachineEditionParser(specimen_dir)
meaning_units = list(parser.iter_meaning_units())

# 4. Query across resolution levels and trace provenance
query = MachineEditionQueryEngine(parser)
l1_claims = query.filter_by_resolution("L1")
prov = query.trace_provenance(l1_claims[0].id)
print(f"Claim: {l1_claims[0].claim}")
print(f"Source: {prov.source_title} ({prov.source_url})")

# 5. Compare representations
matrix = RepresentationComparator.get_standard_matrix()
print("Machine Edition vs PDF explicit boundaries:", matrix["Machine_Edition_v0.1"].has_explicit_boundaries)
```

---

## 2. Specification Binding

This Developer Kit implements the public contract defined in:
* **Specification:** `Machine Edition Specification v0.1`
* **Canonical URI:** `https://winmedia.com/machine-editions/specification/v0.1`

---

## 3. Architecture Roadmap

* `MEDK-001`: Initial 5-responsibility architecture scaffold & reference interfaces.
* `MEDK-002`: Governed reference specimen expansion (`specimen/srow/package`).
* `MEDK-003`: Public schemas + full reference validator engine (C1-C7 conformance).
* `MEDK-004`: Complete parser abstractions.
* `MEDK-005`: Multi-tier query pack.
* `MEDK-006`: Executable representation comparison benchmarks.

---

## 4. License

MIT License (c) 2026 Lynn Media.
