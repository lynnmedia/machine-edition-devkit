"""Comparison module comparing Machine Editions against PDF, EPUB, and naive RAG representations."""

from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass(frozen=True)
class RepresentationMetrics:
    format_name: str
    has_explicit_boundaries: bool
    has_deterministic_provenance: bool
    has_atomic_meaning_units: bool
    has_resolution_hierarchy: bool
    requires_heuristic_chunking: bool
    verifiable_via_json_schema: bool


class RepresentationComparator:
    """Provides analytical and programmatic comparison across publication formats."""

    @staticmethod
    def get_standard_matrix() -> Dict[str, RepresentationMetrics]:
        return {
            "PDF": RepresentationMetrics(
                format_name="PDF",
                has_explicit_boundaries=False,
                has_deterministic_provenance=False,
                has_atomic_meaning_units=False,
                has_resolution_hierarchy=False,
                requires_heuristic_chunking=True,
                verifiable_via_json_schema=False,
            ),
            "EPUB": RepresentationMetrics(
                format_name="EPUB",
                has_explicit_boundaries=False,
                has_deterministic_provenance=False,
                has_atomic_meaning_units=False,
                has_resolution_hierarchy=False,
                requires_heuristic_chunking=True,
                verifiable_via_json_schema=False,
            ),
            "Naive_RAG": RepresentationMetrics(
                format_name="Naive RAG Chunks",
                has_explicit_boundaries=False,
                has_deterministic_provenance=False,
                has_atomic_meaning_units=False,
                has_resolution_hierarchy=False,
                requires_heuristic_chunking=True,
                verifiable_via_json_schema=False,
            ),
            "Machine_Edition_v0.1": RepresentationMetrics(
                format_name="Machine Edition v0.1",
                has_explicit_boundaries=True,
                has_deterministic_provenance=True,
                has_atomic_meaning_units=True,
                has_resolution_hierarchy=True,
                requires_heuristic_chunking=False,
                verifiable_via_json_schema=True,
            ),
        }
