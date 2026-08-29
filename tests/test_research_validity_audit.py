"""Tests for ME-RES-001B experimental subject reality and validity audit."""

from pathlib import Path
import json
import pytest

from machine_edition_devkit.research.me_res_001.protocol import MODEL_CONFIG
from machine_edition_devkit.research.me_res_001.runner import execute_model_inference
from machine_edition_devkit.research.me_res_001.verify import verify_research_integrity


@pytest.fixture
def repo_root():
    return Path(__file__).resolve().parent.parent


def test_research_integrity_verification(repo_root):
    res = verify_research_integrity(repo_root)
    assert res["all_passed"] is True, f"Integrity failure: {res['checks']}"


def test_experimental_subject_is_reference_harness():
    """Confirms subject is a deterministic rule-based reference evaluator (Path B)."""
    assert MODEL_CONFIG["provider"] == "local-deterministic-reference"
    assert MODEL_CONFIG["model_id"] == "eval-model-v01-deterministic"
    assert MODEL_CONFIG["temperature"] == 0.0


def test_replicate_exact_determinism():
    """Confirms that replicates in this harness produce identical deterministic outputs."""
    q = "What is the stable-ID algorithm in SROW?"
    ctx = "The stable-ID algorithm uses SHA-256 truncated to 16 hexadecimal characters."

    out1 = execute_model_inference(q, ctx, "Machine_Edition", "factual_retrieval", "ME-BENCH-001", replicate=1)
    out2 = execute_model_inference(q, ctx, "Machine_Edition", "factual_retrieval", "ME-BENCH-001", replicate=2)
    out3 = execute_model_inference(q, ctx, "Machine_Edition", "factual_retrieval", "ME-BENCH-001", replicate=3)

    assert out1["parsed_response"] == out2["parsed_response"] == out3["parsed_response"]


def test_gold_firewall_source_code_isolation(repo_root):
    """Verifies that runner.py source code contains no imports or references to gold adjudication files."""
    runner_src = (repo_root / "src" / "machine_edition_devkit" / "research" / "me_res_001" / "runner.py").read_text(encoding="utf-8")

    assert "answers.jsonl" not in runner_src
    assert "benchmark/gold" not in runner_src
    assert "constraints.jsonl" not in runner_src
