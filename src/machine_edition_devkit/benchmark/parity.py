"""Information-parity verification for ME-BENCH-001 across representations."""

from pathlib import Path
import json
from typing import Dict, Any, List

from machine_edition_devkit.benchmark.adapters import (
    BenchmarkPDFAdapter,
    BenchmarkEPUBAdapter,
    BenchmarkNaiveRAGAdapter,
    BenchmarkMachineEditionAdapter,
)


def verify_information_parity(benchmark_root: Path) -> Dict[str, Any]:
    """Verifies that all 16 facts in source inventory are present across PDF, EPUB, RAG, and Machine Edition."""
    inventory_path = benchmark_root / "source" / "source-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    facts = inventory.get("facts", [])

    pdf_adapter = BenchmarkPDFAdapter(benchmark_root / "representations" / "pdf" / "benchmark-document.pdf")
    epub_adapter = BenchmarkEPUBAdapter(benchmark_root / "representations" / "epub" / "benchmark-document.epub")
    rag_adapter = BenchmarkNaiveRAGAdapter(benchmark_root / "representations" / "rag" / "rag-corpus.json")
    me_adapter = BenchmarkMachineEditionAdapter(benchmark_root / "representations" / "machine-edition" / "package")

    pdf_text = pdf_adapter.get_full_text().lower()
    epub_text = epub_adapter.get_full_text().lower()
    rag_text = rag_adapter.get_full_text().lower()
    me_text = me_adapter.get_full_text().lower()

    results = []
    all_passed = True

    # Primary key substrings for each fact to ensure rigorous textual presence
    fact_keywords = {
        "FACT-001": "communication protocol for making structured knowledge",
        "FACT-002": "structure is a form of reader respect",
        "FACT-003": "progressive disclosure is a staged presentation",
        "FACT-004": "resolution levels range from l0 to l4",
        "FACT-005": "sha-256 truncated to 16 hexadecimal characters",
        "FACT-006": "explicit structural compliance for software and ai validation",
        "FACT-007": "derives_from indicates source lineage",
        "FACT-008": "six core record types: manifest, meaning_unit",
        "FACT-009": "resolution monotonicity requires that higher detail levels",
        "FACT-010": "epistemic authority requires that every atomic assertion",
        "FACT-011": "when source evidence is underspecified",
        "FACT-012": "contextual scope tags define the operational domain",
        "FACT-013": "not a cognition architecture or internal thought representation",
        "FACT-014": "do not guarantee factual truth or eliminate model error",
        "FACT-015": "contains only authorized public companion samples",
        "FACT-016": "schema conformance certifies structural and syntactic compliance",
    }

    for f in facts:
        fid = f["fact_id"]
        needle = fact_keywords.get(fid, f["statement"][:40]).lower()

        in_pdf = needle in pdf_text
        in_epub = needle in epub_text
        in_rag = needle in rag_text
        in_me = needle in me_text

        fact_passed = in_pdf and in_epub and in_rag and in_me
        if not fact_passed:
            all_passed = False

        results.append({
            "fact_id": fid,
            "subject": f.get("subject", ""),
            "present_in_pdf": in_pdf,
            "present_in_epub": in_epub,
            "present_in_rag": in_rag,
            "present_in_machine_edition": in_me,
            "parity_status": "PASS" if fact_passed else "FAIL",
        })

    return {
        "benchmark_id": "winmedia.machine-edition-representation-benchmark.v0.1",
        "fact_count": len(facts),
        "facts_passed": sum(1 for r in results if r["parity_status"] == "PASS"),
        "all_passed": all_passed,
        "results": results
    }
