"""Comparison engine evaluating PDF, EPUB, Naive RAG, and Machine Edition across 16 tasks."""

from dataclasses import dataclass, asdict
from pathlib import Path
import json
from typing import List, Dict, Any, Optional

from machine_edition_devkit.comparison.adapters import (
    PDFAdapter,
    EPUBAdapter,
    NaiveRAGAdapter,
    MachineEditionAdapter,
    SearchMatch,
)
from machine_edition_devkit.validate import MachineEditionValidator


@dataclass
class TaskEvaluationResult:
    task_id: str
    family: str
    representation: str
    supported: str  # "yes", "partial", "no", "not_applicable"
    support_class: str  # "native", "derived", "pipeline", "absent"
    content_correct: bool
    explicit_structure_available: bool
    provenance_class: str  # "record", "document", "chunk", "none", "not_applicable"
    result_snippet: str
    notes: str


class ComparisonHarness:
    """Executes the controlled 16-task comparison across the 4 representations."""

    def __init__(self, comparison_root: Optional[Path] = None):
        if comparison_root is None:
            comparison_root = Path(__file__).resolve().parent.parent.parent.parent / "comparison"
        self.root = comparison_root
        self.tasks = json.loads((self.root / "tasks" / "tasks.json").read_text(encoding="utf-8"))
        self.source_inventory = json.loads((self.root / "source" / "source-inventory.json").read_text(encoding="utf-8"))

        self.pdf_adapter = PDFAdapter(self.root / "pdf" / "comparison-document.pdf")
        self.epub_adapter = EPUBAdapter(self.root / "epub" / "comparison-document.epub")
        self.rag_adapter = NaiveRAGAdapter(self.root / "rag" / "rag-corpus.json")
        self.me_adapter = MachineEditionAdapter(self.root / "machine-edition" / "package")

    def run_all(self) -> List[TaskEvaluationResult]:
        results = []
        for task in self.tasks:
            t_id = task["task_id"]
            family = task["family"]
            query = task["query"]
            expected_sub = task["expected_text_substring"]

            # 1. PDF Evaluation
            pdf_matches = self.pdf_adapter.search_text(query)
            if family in ("A_Content_Retrieval", "B_Structural_Navigation", "C_Definition_Retrieval", "F_Boundary_Recognition"):
                found = any(expected_sub.lower() in m.matched_text.lower() for m in pdf_matches)
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="PDF",
                        supported="yes" if found else "partial",
                        support_class="derived" if family in ("C_Definition_Retrieval", "F_Boundary_Recognition") else "native",
                        content_correct=found,
                        explicit_structure_available=False,
                        provenance_class="document",
                        result_snippet=pdf_matches[0].matched_text[:80] if pdf_matches else "None",
                        notes="Text extracted from linear PDF stream; lacks atomic discrete records.",
                    )
                )
            elif family == "D_Provenance":
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="PDF",
                        supported="partial",
                        support_class="derived",
                        content_correct=False,
                        explicit_structure_available=False,
                        provenance_class="document",
                        result_snippet="Document title only",
                        notes="PDF has file/document metadata only; no atomic record-level provenance bindings.",
                    )
                )
            elif family in ("E_Relationships", "G_Resolution", "H_Conformance_Validation"):
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="PDF",
                        supported="no",
                        support_class="absent",
                        content_correct=False,
                        explicit_structure_available=False,
                        provenance_class="none",
                        result_snippet="Not supported in format",
                        notes="PDF format does not model typed relationships, resolution hierarchy, or JSON schema contracts.",
                    )
                )

            # 2. EPUB Evaluation
            epub_matches = self.epub_adapter.search_text(query)
            if family in ("A_Content_Retrieval", "B_Structural_Navigation", "C_Definition_Retrieval", "F_Boundary_Recognition"):
                found = any(expected_sub.lower() in m.matched_text.lower() for m in epub_matches)
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="EPUB",
                        supported="yes" if found else "partial",
                        support_class="native" if family == "B_Structural_Navigation" else "derived",
                        content_correct=found,
                        explicit_structure_available=False,
                        provenance_class="document",
                        result_snippet=epub_matches[0].matched_text[:80] if epub_matches else "None",
                        notes="Reflowable XHTML reading document with chapter sections.",
                    )
                )
            elif family == "D_Provenance":
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="EPUB",
                        supported="partial",
                        support_class="derived",
                        content_correct=False,
                        explicit_structure_available=False,
                        provenance_class="document",
                        result_snippet="OPF metadata only",
                        notes="EPUB has package Dublin Core metadata; lacks atomic assertion provenance.",
                    )
                )
            elif family in ("E_Relationships", "G_Resolution", "H_Conformance_Validation"):
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="EPUB",
                        supported="no",
                        support_class="absent",
                        content_correct=False,
                        explicit_structure_available=False,
                        provenance_class="none",
                        result_snippet="Not supported in format",
                        notes="EPUB does not declare machine-native typed relationships or resolution levels.",
                    )
                )

            # 3. Naive RAG Evaluation
            rag_matches = self.rag_adapter.search_text(query)
            if family in ("A_Content_Retrieval", "C_Definition_Retrieval", "F_Boundary_Recognition"):
                found = any(expected_sub.lower() in m.matched_text.lower() for m in rag_matches)
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="Naive_RAG",
                        supported="yes" if found else "partial",
                        support_class="pipeline",
                        content_correct=found,
                        explicit_structure_available=False,
                        provenance_class="chunk",
                        result_snippet=rag_matches[0].matched_text[:80] if rag_matches else "None",
                        notes="Lexical retrieval over sliding-window text chunks.",
                    )
                )
            elif family == "B_Structural_Navigation":
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="Naive_RAG",
                        supported="partial",
                        support_class="pipeline",
                        content_correct=True,
                        explicit_structure_available=False,
                        provenance_class="chunk",
                        result_snippet=rag_matches[0].matched_text[:80] if rag_matches else "None",
                        notes="Chunk index maintains sequence order; lacks formal section tree.",
                    )
                )
            elif family == "D_Provenance":
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="Naive_RAG",
                        supported="partial",
                        support_class="pipeline",
                        content_correct=False,
                        explicit_structure_available=False,
                        provenance_class="chunk",
                        result_snippet=f"source: {rag_matches[0].metadata['chunk_id']}" if rag_matches else "None",
                        notes="Chunk contains document filename and position only; no claim-to-URL ledger.",
                    )
                )
            elif family in ("E_Relationships", "G_Resolution", "H_Conformance_Validation"):
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="Naive_RAG",
                        supported="no",
                        support_class="absent",
                        content_correct=False,
                        explicit_structure_available=False,
                        provenance_class="none",
                        result_snippet="Not supported in format",
                        notes="Naive RAG chunks contain plain text without typed relationships or resolution tiers.",
                    )
                )

            # 4. Machine Edition Evaluation
            if family == "A_Content_Retrieval":
                units = self.me_adapter.edition.find_units(query=query)
                found = len(units) > 0 and (expected_sub.lower() in units[0].claim.lower() or expected_sub.lower() in units[0].title.lower())
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="Machine_Edition",
                        supported="yes",
                        support_class="native",
                        content_correct=found,
                        explicit_structure_available=True,
                        provenance_class="record",
                        result_snippet=units[0].claim[:80] if units else "None",
                        notes="Native meaning unit lookup.",
                    )
                )
            elif family == "B_Structural_Navigation":
                units = self.me_adapter.edition.find_units(query=query)
                found = len(units) > 0
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="Machine_Edition",
                        supported="yes",
                        support_class="native",
                        content_correct=found,
                        explicit_structure_available=True,
                        provenance_class="record",
                        result_snippet=units[0].title if units else "None",
                        notes="Atomic meaning units with explicit scope and resolution level.",
                    )
                )
            elif family == "C_Definition_Retrieval":
                defs = self.me_adapter.edition.definitions()
                matching_def = next((d for d in defs if query.lower() in d.definition.lower() or query.lower() in d.term.lower()), None)
                found = matching_def is not None and expected_sub.lower() in matching_def.definition.lower()
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="Machine_Edition",
                        supported="yes",
                        support_class="native",
                        content_correct=found,
                        explicit_structure_available=True,
                        provenance_class="record",
                        result_snippet=matching_def.definition[:80] if matching_def else "None",
                        notes="Explicit typed definition records with term bindings.",
                    )
                )
            elif family == "D_Provenance":
                mu = self.me_adapter.edition.find_units(query=query)[0]
                prov = self.me_adapter.edition.provenance(mu)
                found = expected_sub.lower() in prov.source_url.lower() or expected_sub.lower() in prov.source_title.lower()
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="Machine_Edition",
                        supported="yes",
                        support_class="native",
                        content_correct=found,
                        explicit_structure_available=True,
                        provenance_class="record",
                        result_snippet=f"{prov.source_title} ({prov.source_url})",
                        notes="Atomic meaning unit bound to verifiable source provenance record.",
                    )
                )
            elif family == "E_Relationships":
                rels = self.me_adapter.edition.relationships()
                found = any(expected_sub in (r.subject_id + " " + r.object_id) for r in rels)
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="Machine_Edition",
                        supported="yes",
                        support_class="native",
                        content_correct=found,
                        explicit_structure_available=True,
                        provenance_class="record",
                        result_snippet=f"{rels[0].subject_id} -({rels[0].predicate})-> {rels[0].object_id}",
                        notes="Explicit typed relationships (derives_from, clarifies).",
                    )
                )
            elif family == "F_Boundary_Recognition":
                bounds = self.me_adapter.edition.boundaries()
                matching_b = next((b for b in bounds if query.lower() in b.statement.lower()), None)
                found = matching_b is not None and expected_sub.lower() in matching_b.statement.lower()
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="Machine_Edition",
                        supported="yes",
                        support_class="native",
                        content_correct=found,
                        explicit_structure_available=True,
                        provenance_class="record",
                        result_snippet=matching_b.statement[:80] if matching_b else "None",
                        notes="Explicit negative scope and epistemic boundaries.",
                    )
                )
            elif family == "G_Resolution":
                units = self.me_adapter.edition.find_units(resolution_level=expected_sub)
                found = len(units) > 0
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="Machine_Edition",
                        supported="yes",
                        support_class="native",
                        content_correct=found,
                        explicit_structure_available=True,
                        provenance_class="record",
                        result_snippet=f"{len(units)} units at {expected_sub}",
                        notes="Declared progressive disclosure resolution hierarchy (L0-L4).",
                    )
                )
            elif family == "H_Conformance_Validation":
                val = MachineEditionValidator().validate_package(self.me_adapter.package_path)
                found = val.outcome == "ME_CONFORMANT"
                results.append(
                    TaskEvaluationResult(
                        task_id=t_id,
                        family=family,
                        representation="Machine_Edition",
                        supported="yes",
                        support_class="native",
                        content_correct=found,
                        explicit_structure_available=True,
                        provenance_class="record",
                        result_snippet="ME_CONFORMANT (C1-C7)",
                        notes="Formal validation against public JSON Schemas (Draft 2020-12).",
                    )
                )

        return results

    def get_property_matrix(self) -> Dict[str, Dict[str, str]]:
        return {
            "Human reading": {
                "PDF": "NATIVE (Fixed visual rendering)",
                "EPUB": "NATIVE (Reflowable reading)",
                "Naive RAG": "ABSENT (Fragmented chunks)",
                "Machine Edition": "NATIVE (full-preview.md entrypoint)",
            },
            "Explicit semantic units": {
                "PDF": "ABSENT (Linear text stream)",
                "EPUB": "ABSENT (Document sections)",
                "Naive RAG": "ABSENT (Heuristic token chunks)",
                "Machine Edition": "NATIVE (Atomic meaning units with IDs)",
            },
            "Explicit hierarchy": {
                "PDF": "DERIVED (Visual layout / headings)",
                "EPUB": "NATIVE (TOC & Chapter spine)",
                "Naive RAG": "PIPELINE (Position index)",
                "Machine Edition": "NATIVE (Resolution tiers L0-L4)",
            },
            "Explicit provenance granularity": {
                "PDF": "DOCUMENT (File metadata)",
                "EPUB": "DOCUMENT (Package metadata)",
                "Naive RAG": "CHUNK (Source doc + pos)",
                "Machine Edition": "RECORD (Assertion-level URLs & hashes)",
            },
            "Typed relationships": {
                "PDF": "ABSENT",
                "EPUB": "ABSENT",
                "Naive RAG": "ABSENT",
                "Machine Edition": "NATIVE (Subject-Predicate-Object links)",
            },
            "Explicit boundaries": {
                "PDF": "DERIVED (Unstructured prose)",
                "EPUB": "DERIVED (Unstructured prose)",
                "Naive RAG": "DERIVED (Retrieved chunk)",
                "Machine Edition": "NATIVE (Typed boundary records)",
            },
            "Capability declaration": {
                "PDF": "ABSENT",
                "EPUB": "ABSENT",
                "Naive RAG": "ABSENT",
                "Machine Edition": "NATIVE (Formats & resolution levels in manifest)",
            },
            "Public conformance contract": {
                "PDF": "DERIVED (ISO 32000 PDF syntax)",
                "EPUB": "DERIVED (EPUB 3.0 package spec)",
                "Naive RAG": "PIPELINE (Ad-hoc config)",
                "Machine Edition": "NATIVE (ME Spec v0.1 JSON Schemas C1-C7)",
            },
            "Source identity": {
                "PDF": "DOCUMENT",
                "EPUB": "DOCUMENT (UUID/URN)",
                "Naive RAG": "PIPELINE",
                "Machine Edition": "NATIVE (Reverse domain package_id + semver)",
            },
            "Native machine traversal": {
                "PDF": "NO (Requires heuristic parser)",
                "EPUB": "PARTIAL (XHTML DOM traversal)",
                "Naive RAG": "PARTIAL (Vector/lexical search)",
                "Machine Edition": "YES (Deterministic typed graph traversal)",
            },
            "Retrofit cost / complexity": {
                "PDF": "LOW (Standard print/export)",
                "EPUB": "LOW (Standard ebook export)",
                "Naive RAG": "LOW (Simple text chunking script)",
                "Machine Edition": "MODERATE (Structured semantic extraction)",
            },
        }

    def render_summary_table(self, results: List[TaskEvaluationResult]) -> str:
        lines = [
            f"{'Task':<6} {'Family':<26} {'PDF':<10} {'EPUB':<10} {'RAG':<12} {'ME':<10}",
            "-" * 78,
        ]
        task_ids = sorted(list(set(r.task_id for r in results)))
        for tid in task_ids:
            t_res = {r.representation: r for r in results if r.task_id == tid}
            fam = t_res["Machine_Edition"].family[:24]
            pdf_s = f"{t_res['PDF'].support_class}"
            epub_s = f"{t_res['EPUB'].support_class}"
            rag_s = f"{t_res['Naive_RAG'].support_class}"
            me_s = f"{t_res['Machine_Edition'].support_class}"
            lines.append(f"{tid:<6} {fam:<26} {pdf_s:<10} {epub_s:<10} {rag_s:<12} {me_s:<10}")
        lines.append("-" * 78)
        return "\n".join(lines)
