# Representation Comparison: PDF, EPUB, Naive RAG, and Machine Edition

This document details the controlled, executable representation trial conducted in **MEDK-006** across four publication paradigms:
1. **PDF (Fixed Layout Document)**
2. **EPUB (Reflowable Human Reader Document)**
3. **Naive RAG (Heuristic Text Chunks)**
4. **Machine Edition (Structured Publication Package v0.1)**

---

## 1. Methodological Statement

> **Important Boundary:** MEDK-006 does **not** establish that Machine Editions universally outperform PDF, EPUB, or RAG systems. It demonstrates which properties are native to each representation and provides executable evidence of the consequences of those representational choices.

RAG and Machine Editions occupy different layers of the software architecture:
* **RAG:** A retrieval technique operating over unstructured textual corpora, offering low retrofit complexity to arbitrary existing text.
* **Machine Edition:** A structured publication package standardizing meaning units, typed relationships, explicit boundaries, resolution tiers, and verifiable assertion-level provenance.

---

## 2. Information-Parity Doctrine

To ensure a fair trial, all four representations were constructed from a single frozen, representation-neutral source:
* **Source Document:** `comparison/source/comparison-source.md`
* **Authority Inventory:** `comparison/source/source-inventory.json` (8 tracked core facts)
* **Parity Guarantee:** Every task-relevant assertion evaluated exists verbatim across all four formats.

---

## 3. Representation Property Matrix

| Property | PDF | EPUB | Naive RAG | Machine Edition v0.1 |
| :--- | :--- | :--- | :--- | :--- |
| **Human reading** | NATIVE (Fixed visual layout) | NATIVE (Reflowable reading flow) | ABSENT (Fragmented token chunks) | NATIVE (`full-preview.md` entrypoint) |
| **Explicit semantic units** | ABSENT (Linear stream) | ABSENT (Document sections) | ABSENT (Sliding-window strings) | NATIVE (Atomic units with IDs) |
| **Explicit hierarchy** | DERIVED (Visual layout) | NATIVE (TOC & spine) | PIPELINE (Position indices) | NATIVE (Resolution levels L0-L4) |
| **Provenance granularity** | DOCUMENT (File metadata) | DOCUMENT (Dublin Core) | CHUNK (File + offset) | RECORD (Assertion URLs & hashes) |
| **Typed relationships** | ABSENT | ABSENT | ABSENT | NATIVE (Subject-Predicate-Object) |
| **Explicit boundaries** | DERIVED (Unstructured text) | DERIVED (Unstructured text) | DERIVED (Retrieved chunk) | NATIVE (Typed boundary records) |
| **Capability declaration** | ABSENT | ABSENT | ABSENT | NATIVE (Manifest formats & tiers) |
| **Conformance contract** | DERIVED (ISO 32000) | DERIVED (EPUB 3.0 spec) | PIPELINE (Ad-hoc config) | NATIVE (JSON Schemas C1-C7) |
| **Source identity** | DOCUMENT | DOCUMENT (UUID/URN) | PIPELINE | NATIVE (Reverse domain + semver) |
| **Machine traversal** | NO (Heuristic scraping) | PARTIAL (DOM traversal) | PARTIAL (Lexical search) | YES (Typed graph traversal) |
| **Retrofit complexity** | LOW (Export to PDF) | LOW (Export to EPUB) | LOW (Sliding chunk script) | MODERATE (Semantic extraction) |

---

## 4. Executable Task Summary

Across 16 executed tasks spanning 8 families:
* **A_Content_Retrieval:** All four representations successfully locate core textual assertions.
* **B_Structural_Navigation:** PDF and EPUB excel at human document navigation; Machine Edition exposes discrete atomic meaning units.
* **C_Definition_Retrieval:** PDF/EPUB/RAG locate definitions embedded in prose; Machine Edition resolves explicit typed definition records with term bindings.
* **D_Provenance:** PDF/EPUB expose document-level provenance; RAG exposes chunk source files; Machine Edition traces exact assertion-level provenance records and URLs.
* **E_Relationships:** Only Machine Edition natively models typed semantic relationships (`derives_from`, `clarifies`).
* **F_Boundary_Recognition:** Machine Edition natively provides dedicated boundary records declaring negative and epistemic scope limits.
* **G_Resolution:** Machine Edition natively provides multi-tier progressive disclosure (`L0` to `L4`).
* **H_Conformance_Validation:** Machine Edition packages validate against public JSON Schema contracts (C1-C7).

---

## 5. How to Reproduce

```bash
# Inspect the source facts
python -m machine_edition_devkit.comparison inspect

# View the architectural property matrix
python -m machine_edition_devkit.comparison matrix

# Run all 16 comparison tasks across all 4 representations
python -m machine_edition_devkit.comparison run
```
