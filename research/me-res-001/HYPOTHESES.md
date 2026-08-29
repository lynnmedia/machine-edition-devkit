# Pre-Registered Hypotheses — ME-RES-001

## Directional Hypotheses

### H1 — Provenance Tracing
On provenance-tracing tasks:
Machine Edition > PDF, EPUB, RAG
on `provenance_completeness` because record-level provenance bindings and cryptographic release hashes are natively declared in the Machine Edition package.

### H2 — Relationship Retrieval
On relationship-retrieval tasks:
Machine Edition > PDF, EPUB, RAG
on `relationship_accuracy` because typed relationship predicates (`derives_from`, `clarifies`, `depends_on`, `exemplifies`) are machine-native in the Machine Edition condition.

### H3 — Boundary and Semantic Invariant Preservation
On boundary constraint, ambiguity handling, and multi-resolution tasks:
Machine Edition > non-ME conditions
on `semantic_invariant_preservation` and
Machine Edition < non-ME conditions
on `constraint_violations`.

### H4 — Unsupported Claims
On unsupported-claim detection tasks:
Machine Edition <= non-ME conditions
on `unsupported_assertion_rate` and `ANSWER_WHEN_UNSUPPORTED` failure incidence.

### H5 — Factual Retrieval Neutrality
For ordinary factual retrieval:
NO DIRECTIONAL SUPERIORITY HYPOTHESIS
All four representations contain 100% information parity (16/16 verified facts); observed factual performance should remain comparable across conditions.
