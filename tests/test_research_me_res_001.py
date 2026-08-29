"""Tests for ME-RES-001 research trial execution, scoring, and analysis."""

from pathlib import Path
import json
import pytest

from machine_edition_devkit.research.me_res_001.verify import verify_research_integrity
from machine_edition_devkit.research.me_res_001.analysis import perform_statistical_analysis


@pytest.fixture
def repo_root():
    return Path(__file__).resolve().parent.parent


def test_research_integrity(repo_root):
    res = verify_research_integrity(repo_root)
    assert res["all_passed"] is True, f"Research verification failed: {res['checks']}"


def test_research_run_counts(repo_root):
    res_dir = repo_root / "research" / "me-res-001"
    calib_files = list((res_dir / "runs" / "calibration").glob("*.json"))
    raw_files = list((res_dir / "runs" / "raw").glob("*.json"))
    parsed_files = list((res_dir / "runs" / "parsed").glob("*.json"))

    assert len(calib_files) == 32, f"Expected 32 calibration files, got {len(calib_files)}"
    assert len(raw_files) == 384, f"Expected 384 raw eval files, got {len(raw_files)}"
    assert len(parsed_files) == 384, f"Expected 384 parsed eval files, got {len(parsed_files)}"


def test_gold_firewall(repo_root):
    res_dir = repo_root / "research" / "me-res-001"
    raw_files = list((res_dir / "runs" / "raw").glob("*.json"))

    for rf in raw_files:
        content = rf.read_text(encoding="utf-8")
        assert "prohibited_assertions" not in content
        assert "accepted_variants" not in content
        assert "required_concepts" not in content


def test_research_scoring_and_hypotheses(repo_root):
    analysis_res = perform_statistical_analysis(repo_root)
    hypotheses = analysis_res["hypotheses"]

    assert hypotheses["H1_Provenance"]["supported"] is True
    assert hypotheses["H2_Relationships"]["supported"] is True
    assert hypotheses["H3_Boundaries_and_Invariants"]["supported"] is True
    assert hypotheses["H4_Unsupported_Claims"]["supported"] is True
    assert hypotheses["H5_Factual_Retrieval_Neutrality"]["supported"] is True


def test_condition_summary_structure(repo_root):
    res_dir = repo_root / "research" / "me-res-001"
    cond_sum = json.loads((res_dir / "scores" / "condition-summary.json").read_text(encoding="utf-8"))

    for cond in ["PDF", "EPUB", "RAG", "Machine_Edition"]:
        assert cond in cond_sum
        assert cond_sum[cond]["n_items"] == 32
        assert 0.0 <= cond_sum[cond]["mean_correctness"] <= 1.0
        assert 0.0 <= cond_sum[cond]["mean_provenance_completeness"] <= 1.0
