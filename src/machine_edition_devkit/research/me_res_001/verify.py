"""Verification engine for ME-RES-001 research artifacts and execution integrity."""

from pathlib import Path
import json
import hashlib
from typing import Dict, Any, List

from machine_edition_devkit.benchmark.integrity import verify_benchmark_integrity
from machine_edition_devkit.benchmark.parity import verify_information_parity


def verify_research_integrity(repo_root: Path) -> Dict[str, Any]:
    """Verifies all ME-RES-001 research artifacts, run completeness, gold firewall, and analysis integrity."""
    bench_dir = repo_root / "benchmark"
    res_dir = repo_root / "research" / "me-res-001"
    runs_dir = res_dir / "runs"
    calib_dir = runs_dir / "calibration"
    raw_dir = runs_dir / "raw"
    parsed_dir = runs_dir / "parsed"
    scores_dir = res_dir / "scores"
    analysis_dir = res_dir / "analysis"

    checks = []
    all_passed = True

    # 1. Benchmark Integrity & Parity
    bench_int = verify_benchmark_integrity(repo_root)
    if not bench_int["all_passed"]:
        all_passed = False
    checks.append({"name": "benchmark_integrity", "passed": bench_int["all_passed"], "details": f"{bench_int['checked_count']}/{bench_int['file_count']} files verified"})

    bench_par = verify_information_parity(bench_dir)
    if not bench_par["all_passed"]:
        all_passed = False
    checks.append({"name": "information_parity", "passed": bench_par["all_passed"], "details": f"{bench_par['facts_passed']}/16 facts verified"})

    # 2. Protocol Files Presence
    protocol_files = [
        res_dir / "PROTOCOL.md",
        res_dir / "HYPOTHESES.md",
        res_dir / "MODEL.json",
        res_dir / "PROMPT.md",
        res_dir / "CONDITIONS.json",
        res_dir / "RUN-SCHEDULE.json",
        res_dir / "EXECUTION-MANIFEST.json",
        res_dir / "README.md",
        res_dir / "report" / "ME-RES-001-REPORT.md",
    ]
    missing_proto = [str(f.relative_to(repo_root)) for f in protocol_files if not f.exists()]
    proto_passed = len(missing_proto) == 0
    if not proto_passed:
        all_passed = False
    checks.append({"name": "protocol_artifacts_presence", "passed": proto_passed, "details": f"Missing: {missing_proto}" if missing_proto else "All protocol documents present"})

    # 3. Run Completeness
    calib_files = list(calib_dir.glob("*.json"))
    raw_files = list(raw_dir.glob("*.json"))
    parsed_files = list(parsed_dir.glob("*.json"))

    calib_ok = len(calib_files) == 32  # 8 tasks x 4 conditions
    raw_ok = len(raw_files) == 384     # 32 tasks x 4 conditions x 3 reps
    parsed_ok = len(parsed_files) == 384

    runs_ok = calib_ok and raw_ok and parsed_ok
    if not runs_ok:
        all_passed = False
    checks.append({
        "name": "run_completeness",
        "passed": runs_ok,
        "details": f"Calibration: {len(calib_files)}/32, Raw Eval: {len(raw_files)}/384, Parsed Eval: {len(parsed_files)}/384"
    })

    # 4. Gold Firewall Verification
    gold_leaked = []
    for rf in raw_files:
        content = rf.read_text(encoding="utf-8")
        if "prohibited_assertions" in content or "accepted_variants" in content or "required_concepts" in content:
            gold_leaked.append(rf.name)
    firewall_ok = len(gold_leaked) == 0
    if not firewall_ok:
        all_passed = False
    checks.append({"name": "gold_firewall", "passed": firewall_ok, "details": f"Leaked in: {gold_leaked}" if gold_leaked else "ZERO gold leakage in raw runs"})

    # 5. Scoring & Analysis Completeness
    score_file = scores_dir / "item-scores.jsonl"
    score_count = len(score_file.read_text(encoding="utf-8").strip().splitlines()) if score_file.exists() else 0
    scores_ok = score_count == 384

    analysis_files = [
        scores_dir / "condition-summary.json",
        scores_dir / "family-summary.json",
        scores_dir / "failure-modes.json",
        analysis_dir / "contrasts.json",
        analysis_dir / "bootstrap-results.json",
        analysis_dir / "statistical-results.json",
    ]
    missing_analysis = [str(f.relative_to(repo_root)) for f in analysis_files if not f.exists()]
    analysis_ok = scores_ok and len(missing_analysis) == 0
    if not analysis_ok:
        all_passed = False
    checks.append({
        "name": "scoring_and_analysis_completeness",
        "passed": analysis_ok,
        "details": f"Scored records: {score_count}/384; Missing analysis: {missing_analysis}"
    })

    return {
        "trial_id": "ME-RES-001",
        "all_passed": all_passed,
        "checks": checks,
    }
