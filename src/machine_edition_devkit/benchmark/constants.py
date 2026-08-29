"""Constants and taxonomy definitions for ME-BENCH-001."""

BENCHMARK_ID = "winmedia.machine-edition-representation-benchmark.v0.1"
BENCHMARK_TITLE = "Machine Edition Representation Benchmark v0.1"
BENCHMARK_VERSION = "0.1.0"
BENCHMARK_STATUS = "frozen"
SPECIFICATION_AUTHORITY = "Machine Edition Specification v0.1 (c18dea52074ba278ec6bc4a544c80300df6d8882)"
CORPUS_LINEAGE = "SROW Public Companion v0.1 (archive sha256: 0cd42e724bcd7d4b54c0f850a51ef7b875152cd01f7a20f5b7b34e0d73b5d181) -> SROW Public Reference Specimen -> MEDK-006 -> ME-BENCH-001"

TASK_FAMILIES = [
    "factual_retrieval",
    "relationship_retrieval",
    "hierarchy_preservation",
    "provenance_tracing",
    "boundary_constraint_recognition",
    "ambiguity_handling",
    "multi_resolution_retrieval",
    "unsupported_claim_detection",
]

FAILURE_TAXONOMY = [
    "NONE",
    "INCORRECT_FACT",
    "OMISSION",
    "UNSUPPORTED_ASSERTION",
    "PROVENANCE_MISSING",
    "PROVENANCE_FABRICATED",
    "RELATIONSHIP_ERROR",
    "HIERARCHY_ERROR",
    "BOUNDARY_VIOLATION",
    "AMBIGUITY_COLLAPSE",
    "RESOLUTION_ERROR",
    "REFUSAL_WHEN_SUPPORTED",
    "ANSWER_WHEN_UNSUPPORTED",
    "EXECUTION_ERROR",
]

SCORING_DIMENSIONS = [
    "correctness",
    "provenance_completeness",
    "unsupported_assertion_rate",
    "semantic_invariant_preservation",
    "relationship_accuracy",
    "constraint_violations",
    "failure_mode",
]
