"""Tests for ME-RES-002 real generative model trial."""

from pathlib import Path
import json
import pytest

from machine_edition_devkit.research.me_res_002.protocol import MODEL_CONFIG, SCHEDULE_SEED
from machine_edition_devkit.research.me_res_002.verify import verify_me_res_002_integrity


@pytest.fixture
def repo_root():
    return Path(__file__).resolve().parent.parent


def test_me_res_002_research_integrity(repo_root):
    res = verify_me_res_002_integrity(repo_root)
    assert res["all_passed"] is True, f"ME-RES-002 integrity check failed: {res['checks']}"


def test_me_res_002_model_is_real_neural_model():
    assert MODEL_CONFIG["provider"] == "ollama"
    assert MODEL_CONFIG["model_id"] == "qwen2.5:0.5b"
    assert MODEL_CONFIG["neural_language_model"] is True
    assert MODEL_CONFIG["arbitrary_unseen_text_capability"] is True
    assert MODEL_CONFIG["incremental_cost"] == "$0.00"


def test_me_res_002_runs_count(repo_root):
    res_dir = repo_root / "research" / "me-res-002"
    raw_files = list((res_dir / "runs" / "raw").glob("*.json"))
    parsed_files = list((res_dir / "runs" / "parsed").glob("*.json"))
    calib_files = list((res_dir / "runs" / "calibration").glob("*.json"))

    assert len(calib_files) == 32
    assert len(raw_files) == 384
    assert len(parsed_files) == 384


def test_me_res_002_scoring_integrity(repo_root):
    scores_file = repo_root / "research" / "me-res-002" / "scores" / "item-scores.jsonl"
    assert scores_file.exists()
    lines = scores_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 384
