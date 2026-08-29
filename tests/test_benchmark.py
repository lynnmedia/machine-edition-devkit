"""Tests for ME-BENCH-001 Machine Edition Representation Benchmark v0.1."""

from pathlib import Path
import json
import tempfile
import shutil
import pytest

from machine_edition_devkit.benchmark import (
    BENCHMARK_ID,
    BENCHMARK_TITLE,
    BENCHMARK_VERSION,
    TASK_FAMILIES,
    FAILURE_TAXONOMY,
    SCORING_DIMENSIONS,
    BenchmarkScorer,
    verify_benchmark_integrity,
    verify_information_parity,
    run_synthetic_scorer_fixtures,
    rebuild_all_benchmark_artifacts,
)
from machine_edition_devkit.validate import MachineEditionValidator


@pytest.fixture
def repo_root():
    return Path(__file__).resolve().parent.parent


def test_benchmark_constants():
    assert BENCHMARK_ID == "winmedia.machine-edition-representation-benchmark.v0.1"
    assert BENCHMARK_VERSION == "0.1.0"
    assert len(TASK_FAMILIES) == 8
    assert len(FAILURE_TAXONOMY) == 14
    assert len(SCORING_DIMENSIONS) == 7


def test_benchmark_integrity(repo_root):
    res = verify_benchmark_integrity(repo_root)
    assert res["all_passed"] is True, f"Integrity mismatches: {res['mismatches']}"
    assert res["checked_count"] >= 25


def test_benchmark_representation_validity(repo_root):
    bench_dir = repo_root / "benchmark"
    pdf_path = bench_dir / "representations" / "pdf" / "benchmark-document.pdf"
    epub_path = bench_dir / "representations" / "epub" / "benchmark-document.epub"
    rag_path = bench_dir / "representations" / "rag" / "rag-corpus.json"
    me_pkg_path = bench_dir / "representations" / "machine-edition" / "package"

    assert pdf_path.exists() and pdf_path.stat().st_size > 100
    assert epub_path.exists() and epub_path.stat().st_size > 100
    assert rag_path.exists() and rag_path.stat().st_size > 100

    val = MachineEditionValidator().validate_package(me_pkg_path)
    assert val.outcome == "ME_CONFORMANT", f"Validation errors: {val.errors}"


def test_benchmark_information_parity(repo_root):
    bench_dir = repo_root / "benchmark"
    res = verify_information_parity(bench_dir)
    assert res["all_passed"] is True
    assert res["facts_passed"] == 16
    assert res["fact_count"] == 16


def test_benchmark_task_structure_and_counts(repo_root):
    bench_dir = repo_root / "benchmark"
    tasks = [json.loads(line) for line in (bench_dir / "tasks.jsonl").read_text(encoding="utf-8").strip().splitlines()]

    assert len(tasks) == 40, f"Expected 40 tasks, got {len(tasks)}"

    task_ids = [t["benchmark_id"] for t in tasks]
    assert len(set(task_ids)) == 40, "All benchmark IDs must be unique"

    family_counts = {}
    split_counts = {"calibration": 0, "evaluation": 0}
    for t in tasks:
        fam = t["family"]
        assert fam in TASK_FAMILIES, f"Unknown family: {fam}"
        family_counts[fam] = family_counts.get(fam, 0) + 1
        assert t["split"] in ("calibration", "evaluation")
        split_counts[t["split"]] += 1

    assert len(family_counts) == 8
    for fam, cnt in family_counts.items():
        assert cnt == 5, f"Family {fam} has {cnt} items; expected 5"

    assert split_counts["calibration"] == 8
    assert split_counts["evaluation"] == 32


def test_benchmark_gold_firewall(repo_root):
    bench_dir = repo_root / "benchmark"
    tasks = [json.loads(line) for line in (bench_dir / "tasks.jsonl").read_text(encoding="utf-8").strip().splitlines()]

    for t in tasks:
        assert "required_concepts" not in t, f"Gold leaked in tasks.jsonl: {t['benchmark_id']}"
        assert "accepted_variants" not in t, f"Gold leaked in tasks.jsonl: {t['benchmark_id']}"
        assert "prohibited_assertions" not in t, f"Gold leaked in tasks.jsonl: {t['benchmark_id']}"
        assert "required_triples" not in t, f"Gold leaked in tasks.jsonl: {t['benchmark_id']}"
        assert "required_boundaries" not in t, f"Gold leaked in tasks.jsonl: {t['benchmark_id']}"


def test_benchmark_gold_referential_integrity(repo_root):
    bench_dir = repo_root / "benchmark"
    tasks = {json.loads(line)["benchmark_id"]: json.loads(line) for line in (bench_dir / "tasks.jsonl").read_text().splitlines() if line.strip()}
    answers = {json.loads(line)["benchmark_id"]: json.loads(line) for line in (bench_dir / "gold" / "answers.jsonl").read_text().splitlines() if line.strip()}
    provs = {json.loads(line)["benchmark_id"]: json.loads(line) for line in (bench_dir / "gold" / "provenance.jsonl").read_text().splitlines() if line.strip()}
    rels = {json.loads(line)["benchmark_id"]: json.loads(line) for line in (bench_dir / "gold" / "relationships.jsonl").read_text().splitlines() if line.strip()}
    cons = {json.loads(line)["benchmark_id"]: json.loads(line) for line in (bench_dir / "gold" / "constraints.jsonl").read_text().splitlines() if line.strip()}

    assert len(tasks) == 40
    assert len(answers) == 40
    assert len(provs) == 40
    assert len(rels) == 40
    assert len(cons) == 40

    for tid in tasks:
        assert tid in answers, f"Missing answer gold for {tid}"
        assert tid in provs, f"Missing provenance gold for {tid}"
        assert tid in rels, f"Missing relationships gold for {tid}"
        assert tid in cons, f"Missing constraints gold for {tid}"


def test_benchmark_scorer_fixtures(repo_root):
    bench_dir = repo_root / "benchmark"
    res = run_synthetic_scorer_fixtures(bench_dir)
    assert res["all_passed"] is True, f"Scorer fixture failures: {res['results']}"
    assert res["passed_count"] == 13


def test_isolated_clean_room_reproduction(repo_root):
    """Proves benchmark can be reconstructed cleanly in an isolated temporary location."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        # Copy minimal necessary specimen schemas to temp repo
        (temp_path / "specimen" / "srow" / "package" / "schemas").mkdir(parents=True, exist_ok=True)
        for sf in (repo_root / "specimen" / "srow" / "package" / "schemas").glob("*.json"):
            shutil.copy2(sf, temp_path / "specimen" / "srow" / "package" / "schemas" / sf.name)

        rebuild_all_benchmark_artifacts(temp_path)

        # Verify integrity in temp repo
        int_res = verify_benchmark_integrity(temp_path)
        assert int_res["all_passed"] is True

        # Verify parity in temp repo
        par_res = verify_information_parity(temp_path / "benchmark")
        assert par_res["all_passed"] is True

        # Verify scorer in temp repo
        fix_res = run_synthetic_scorer_fixtures(temp_path / "benchmark")
        assert fix_res["all_passed"] is True
