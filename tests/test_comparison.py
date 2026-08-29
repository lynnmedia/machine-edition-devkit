from pathlib import Path
import json
import pytest
from machine_edition_devkit.comparison import ComparisonHarness, TaskEvaluationResult


@pytest.fixture
def harness():
    return ComparisonHarness()


def test_shared_fact_availability_and_parity(harness):
    inventory = harness.source_inventory
    facts = inventory["facts"]
    assert len(facts) == 8, "Inventory must track all 8 task-relevant facts"

    # Anti-bias Test A: Verify all facts present in all 4 representations
    for f in facts:
        assert f["present_in_pdf"] is True, f"Fact {f['fact_id']} missing from PDF"
        assert f["present_in_epub"] is True, f"Fact {f['fact_id']} missing from EPUB"
        assert f["present_in_rag"] is True, f"Fact {f['fact_id']} missing from RAG"
        assert f["present_in_machine_edition"] is True, f"Fact {f['fact_id']} missing from ME"


def test_rag_no_metadata_leakage(harness):
    # Anti-bias Test B: Ensure RAG chunks do not contain smuggled ME IDs/schemas
    rag_chunks = harness.rag_adapter.chunks
    for c in rag_chunks:
        assert "provenance_id" not in c, "RAG chunk leaked ME provenance_id"
        assert "resolution_level" not in c, "RAG chunk leaked ME resolution_level"
        assert "predicate" not in c, "RAG chunk leaked ME predicate"
        assert "srow.ref.mu" not in c["text"], "RAG chunk text leaked ME unit identifier"


def test_pdf_and_epub_valid_extraction(harness):
    # Anti-bias Test C: Ensure PDF and EPUB are real valid text sources
    pdf_text = harness.pdf_adapter.get_full_text()
    assert len(pdf_text) > 200
    assert "Structure is a form of reader respect" in pdf_text

    epub_text = harness.epub_adapter.get_full_text()
    assert len(epub_text) > 200
    assert "Structure is a form of reader respect" in epub_text


def test_16_comparison_tasks_execution(harness):
    results = harness.run_all()
    assert len(results) == 64, "16 tasks x 4 representations = 64 results"

    print("\n" + harness.render_summary_table(results))

    # Check Family A: Content retrieval succeeds across all 4
    family_a = [r for r in results if r.family == "A_Content_Retrieval"]
    for r in family_a:
        assert r.content_correct is True, f"Family A task {r.task_id} failed on {r.representation}"

    # Check Family D: Provenance distinction
    family_d = [r for r in results if r.family == "D_Provenance"]
    me_prov = [r for r in family_d if r.representation == "Machine_Edition"]
    rag_prov = [r for r in family_d if r.representation == "Naive_RAG"]
    pdf_prov = [r for r in family_d if r.representation == "PDF"]

    for r in me_prov:
        assert r.provenance_class == "record"
        assert r.support_class == "native"
    for r in rag_prov:
        assert r.provenance_class == "chunk"
        assert r.support_class == "pipeline"
    for r in pdf_prov:
        assert r.provenance_class == "document"


def test_property_matrix_generation(harness):
    matrix = harness.get_property_matrix()
    assert "Human reading" in matrix
    assert "Explicit semantic units" in matrix
    assert "Typed relationships" in matrix
    assert "Explicit provenance granularity" in matrix
    assert matrix["Typed relationships"]["Machine Edition"].startswith("NATIVE")
    assert matrix["Typed relationships"]["Naive RAG"] == "ABSENT"
