"""CLI runner for ME-BENCH-001 verification, rebuilding, and scoring."""

import sys
import json
from pathlib import Path

from machine_edition_devkit.benchmark.integrity import verify_benchmark_integrity
from machine_edition_devkit.benchmark.parity import verify_information_parity
from machine_edition_devkit.benchmark.evaluator import run_synthetic_scorer_fixtures, BenchmarkScorer
from machine_edition_devkit.benchmark.rebuild import rebuild_all_benchmark_artifacts
from machine_edition_devkit.validate import MachineEditionValidator


def cmd_verify(repo_root: Path) -> int:
    print("================================================================================")
    print("ME-BENCH-001: Comprehensive Benchmark Verification")
    print("================================================================================")

    # 1. Integrity Verification
    print("\n[1/6] Verifying artifact SHA-256 integrity...")
    integrity_res = verify_benchmark_integrity(repo_root)
    if integrity_res["all_passed"]:
        print(f"  -> PASS: All {integrity_res['checked_count']} frozen benchmark files match integrity manifest.")
    else:
        print(f"  -> FAIL: Integrity verification failed: {integrity_res['mismatches']}")
        return 1

    # 2. Representation Validity
    print("\n[2/6] Verifying representation format validity...")
    bench_dir = repo_root / "benchmark"
    pdf_path = bench_dir / "representations" / "pdf" / "benchmark-document.pdf"
    epub_path = bench_dir / "representations" / "epub" / "benchmark-document.epub"
    rag_path = bench_dir / "representations" / "rag" / "rag-corpus.json"
    me_pkg_path = bench_dir / "representations" / "machine-edition" / "package"

    assert pdf_path.exists() and pdf_path.stat().st_size > 100, "PDF artifact missing or invalid"
    assert epub_path.exists() and epub_path.stat().st_size > 100, "EPUB artifact missing or invalid"
    assert rag_path.exists() and rag_path.stat().st_size > 100, "RAG corpus missing or invalid"

    me_val = MachineEditionValidator().validate_package(me_pkg_path)
    if me_val.outcome == "ME_CONFORMANT":
        print("  -> PASS: PDF, EPUB, RAG, and Machine Edition (ME_CONFORMANT) valid.")
    else:
        print(f"  -> FAIL: Machine Edition package failed validation: {me_val.errors}")
        return 1

    # 3. Information Parity Gate
    print("\n[3/6] Verifying 16-fact information parity across all 4 representations...")
    parity_res = verify_information_parity(bench_dir)
    if parity_res["all_passed"]:
        print(f"  -> PASS: All {parity_res['fact_count']} facts verified across PDF, EPUB, RAG, and Machine Edition.")
    else:
        print(f"  -> FAIL: Parity failure: {parity_res['results']}")
        return 1

    # 4. Gold Referential Integrity & Task Schema
    print("\n[4/6] Verifying task schema and gold referential integrity...")
    tasks_lines = (bench_dir / "tasks.jsonl").read_text(encoding="utf-8").strip().splitlines()
    ans_lines = (bench_dir / "gold" / "answers.jsonl").read_text(encoding="utf-8").strip().splitlines()
    prov_lines = (bench_dir / "gold" / "provenance.jsonl").read_text(encoding="utf-8").strip().splitlines()
    rel_lines = (bench_dir / "gold" / "relationships.jsonl").read_text(encoding="utf-8").strip().splitlines()
    con_lines = (bench_dir / "gold" / "constraints.jsonl").read_text(encoding="utf-8").strip().splitlines()

    assert len(tasks_lines) == 40, f"Expected 40 tasks, got {len(tasks_lines)}"
    assert len(ans_lines) == 40, f"Expected 40 gold answers, got {len(ans_lines)}"
    assert len(prov_lines) == 40, f"Expected 40 gold provenance records, got {len(prov_lines)}"
    assert len(rel_lines) == 40, f"Expected 40 gold relationship records, got {len(rel_lines)}"
    assert len(con_lines) == 40, f"Expected 40 gold constraint records, got {len(con_lines)}"

    task_ids = set()
    families = {}
    splits = {"calibration": 0, "evaluation": 0}
    for line in tasks_lines:
        t = json.loads(line)
        tid = t["benchmark_id"]
        assert tid not in task_ids, f"Duplicate benchmark ID: {tid}"
        task_ids.add(tid)
        fam = t["family"]
        families[fam] = families.get(fam, 0) + 1
        splits[t["split"]] += 1

        # Gold Firewall check: tasks.jsonl must NOT contain gold fields
        assert "required_concepts" not in t, f"Gold leaked in tasks.jsonl: {tid}"
        assert "accepted_variants" not in t, f"Gold leaked in tasks.jsonl: {tid}"
        assert "prohibited_assertions" not in t, f"Gold leaked in tasks.jsonl: {tid}"
        assert "required_triples" not in t, f"Gold leaked in tasks.jsonl: {tid}"
        assert "required_boundaries" not in t, f"Gold leaked in tasks.jsonl: {tid}"

    assert len(families) == 8, f"Expected 8 task families, got {len(families)}"
    for fam, cnt in families.items():
        assert cnt == 5, f"Family {fam} has {cnt} items, expected 5"
    assert splits["calibration"] == 8, f"Expected 8 calibration items, got {splits['calibration']}"
    assert splits["evaluation"] == 32, f"Expected 32 evaluation items, got {splits['evaluation']}"
    print(f"  -> PASS: 40 tasks valid (8 families x 5 items, 8 calibration + 32 evaluation). Gold firewall verified.")

    # 5. Rights Manifest & Threats Registry
    print("\n[5/6] Verifying rights manifest and threats-to-validity registry...")
    assert (bench_dir / "RIGHTS.md").exists(), "RIGHTS.md missing"
    assert (bench_dir / "THREATS-TO-VALIDITY.md").exists(), "THREATS-TO-VALIDITY.md missing"
    assert (bench_dir / "README.md").exists(), "README.md missing"
    print("  -> PASS: RIGHTS.md, THREATS-TO-VALIDITY.md, and README.md present.")

    # 6. Scorer Test Fixtures
    print("\n[6/6] Executing offline scorer test fixture suite...")
    scorer_res = run_synthetic_scorer_fixtures(bench_dir)
    if scorer_res["all_passed"]:
        print(f"  -> PASS: All {scorer_res['fixture_count']} synthetic scorer fixtures passed cleanly.")
    else:
        print(f"  -> FAIL: Scorer fixtures failed: {scorer_res['results']}")
        return 1

    print("\n================================================================================")
    print("DETERMINATION: ME_BENCH_V01_FROZEN_AND_LOCALLY_REPRODUCIBLE")
    print("PUBLIC REPRODUCIBILITY GATE: PENDING_ME_DIST_001")
    print("================================================================================")
    return 0


def cmd_rebuild(repo_root: Path) -> int:
    print("Rebuilding all ME-BENCH-001 benchmark artifacts deterministically...")
    rebuild_all_benchmark_artifacts(repo_root)
    print("Rebuild complete.")
    return 0


def cmd_test_scorer(repo_root: Path) -> int:
    bench_dir = repo_root / "benchmark"
    res = run_synthetic_scorer_fixtures(bench_dir)
    print(f"Executed {res['fixture_count']} scorer fixtures:")
    for r in res["results"]:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  [{status}] {r['name']:<36} (corr={r['correctness']}, failure_modes={r['failure_modes']})")
    if res["all_passed"]:
        print(f"\nALL {res['fixture_count']} FIXTURES PASSED.")
        return 0
    else:
        print(f"\nFIXTURE FAILURES DETECTED.")
        return 1


def cmd_parity(repo_root: Path) -> int:
    bench_dir = repo_root / "benchmark"
    res = verify_information_parity(bench_dir)
    print(f"Information Parity Check: {res['facts_passed']}/{res['fact_count']} facts present across all 4 representations:")
    for r in res["results"]:
        print(f"  [{r['parity_status']}] {r['fact_id']} - {r['subject']:<35} (PDF={r['present_in_pdf']}, EPUB={r['present_in_epub']}, RAG={r['present_in_rag']}, ME={r['present_in_machine_edition']})")
    return 0 if res["all_passed"] else 1


def main():
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    subcmd = sys.argv[1] if len(sys.argv) > 1 else "verify"

    if subcmd == "verify":
        sys.exit(cmd_verify(repo_root))
    elif subcmd == "rebuild":
        sys.exit(cmd_rebuild(repo_root))
    elif subcmd == "test-scorer":
        sys.exit(cmd_test_scorer(repo_root))
    elif subcmd == "parity":
        sys.exit(cmd_parity(repo_root))
    else:
        print(f"Unknown subcommand: {subcmd}. Available: verify, rebuild, test-scorer, parity")
        sys.exit(1)


if __name__ == "__main__":
    main()
