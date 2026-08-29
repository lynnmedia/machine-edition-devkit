# Conformance Crosswalk: SROW Machine Edition Public Companion v0.1 vs Machine Edition Specification v0.1

This crosswalk audits the historical authoritative release `srow-machine-edition-v0.1-public-companion.zip` (SHA-256: `0cd42e724bcd7d4b54c0f850a51ef7b875152cd01f7a20f5b7b34e0d73b5d181`) against the newly frozen public `Machine Edition Specification v0.1` (commit: `c18dea52074ba278ec6bc4a544c80300df6d8882`).

---

## 1. Specification Crosswalk Matrix

| Spec Requirement | Source Artifact / Path in Public Companion | Status | Directly Conformant | Adaptation Required | Reason |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **C1: Manifest Presence** (`manifest.json`) | `metadata/package-manifest.json` | Adaptation Required | No | Yes | Source manifest used historical internal keys (`package_name`, `file_inventory`) rather than normative v0.1 contract keys (`package_id`, `human_readable_entrypoint`, `provenance_file`). |
| **C2: Required Files** (`meaning-units.jsonl`, `provenance.jsonl`, `LICENSE.txt`, `full-preview.md`) | `samples/approved-public-samples.json`, `contracts/LICENSE.md`, `README.md` | Adaptation Required | No | Yes | Source distributed samples as a JSON array (`samples/approved-public-samples.json`) and license in `contracts/LICENSE.md`. Normative package structure requires root-level JSONL files and standard entrypoints. |
| **C3: Valid JSONL** | N/A (Source used JSON array) | Adaptation Required | No | Yes | Source used formatted JSON arrays; normalized to NDJSON (`.jsonl`). |
| **C4: Meaning Unit Validation** (`meaning-unit.schema.json`) | `samples/approved-public-samples.json` | Adaptation Required | No | Yes | Source schema used `text`, `blocks`, `semantic_role`; normalized to normative fields (`claim`, `title`, `resolution_level`, `provenance_id`, `scope`). |
| **C5: Referential Integrity** | N/A (Implicit in sample metadata) | Adaptation Required | No | Yes | Explicit `provenance.jsonl` constructed from authorized public companion metadata and bound via `provenance_id`. |
| **C6: Human Entrypoint Linkage** | `README.md` / `full-preview.md` | Directly Conformant | Yes | No | Provided via `full-preview.md` synthesizing authorized public sample documentation. |
| **C7: License Alignment** | `contracts/LICENSE.md`, `contracts/USAGE-BOUNDARIES.md` | Directly Conformant | Yes | No | Declared CC BY 4.0 within the authorized public scope, preserving strict boundaries against governed manuscript data. |

---

## 2. Derivation Decision

* **Path Chosen:** **Path B — Explicitly Derived Reference Specimen** (`SROW Public Reference Specimen for Machine Edition Specification v0.1`).
* **Justification:** The SROW Public Companion release (tag `v0.1-srow-rc4`, build `2026-08-19`) predates the formal freezing of the public `Machine Edition Specification v0.1` (`2026-08-29`). Deriving a clean, structurally normalized package from the authorized companion ensures full C1–C7 conformance without modifying the frozen specification or exposing governed assets.
