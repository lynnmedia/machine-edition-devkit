"""CLI entrypoint for ME-RES-001 research trial execution, scoring, and verification."""

import sys
import json
from pathlib import Path

from machine_edition_devkit.research.me_res_001.verify import verify_research_integrity
from machine_edition_devkit.research.me_res_001.runner import execute_full_trial
from machine_edition_devkit.research.me_res_001.analysis import perform_statistical_analysis


def cmd_verify(repo_root: Path) -> int:
    print("================================================================================")
    print("ME-RES-001: Research Evidence Verification")
    print("================================================================================")
    res = verify_research_integrity(repo_root)
    for c in res["checks"]:
        status = "PASS" if c["passed"] else "FAIL"
        print(f"  [{status}] {c['name']:<35} -> {c['details']}")

    if res["all_passed"]:
        print("\n================================================================================")
        print("DETERMINATION: ME_RES_V01_CONTROLLED_TRIAL_EXECUTED")
        print("EVIDENCE DETERMINATION: ME_RES_V01_EVIDENCE_PACKAGE_COMPLETE")
        print("================================================================================")
        return 0
    else:
        print("\nVerification failed.")
        return 1


def cmd_run(repo_root: Path) -> int:
    print("Executing full ME-RES-001 experimental trial...")
    res = execute_full_trial(repo_root)
    print(f"Executed {res['calibration_runs']} calibration runs + {res['evaluation_runs']} evaluation runs.")
    print("Performing statistical analysis...")
    perform_statistical_analysis(repo_root)
    print("Analysis complete.")
    return 0


def cmd_score(repo_root: Path) -> int:
    print("Re-scoring evaluation runs and recalculating statistical contrasts...")
    perform_statistical_analysis(repo_root)
    print("Scoring and statistical analysis complete.")
    return 0


def cmd_analyze(repo_root: Path) -> int:
    res = perform_statistical_analysis(repo_root)
    print("\n--- CONDITION SUMMARY ---")
    for cond, stats in res["condition_summary"].items():
        print(f"{cond:<16}: Corr={stats['mean_correctness']:.2f}, Prov={stats['mean_provenance_completeness']:.2f}, Invariant={stats['mean_semantic_invariant_preservation']:.2f}, Rel={stats['mean_relationship_accuracy']:.2f}, Violations={stats['mean_constraint_violations']:.2f}")

    print("\n--- STATISTICAL HYPOTHESES CONFIRMATION ---")
    for hid, hres in res["hypotheses"].items():
        status = "CONFIRMED" if hres["supported"] else "UNSUPPORTED"
        print(f"  [{status}] {hid:<30} -> {hres['conclusion']}")
    return 0


def main():
    repo_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    subcmd = sys.argv[1] if len(sys.argv) > 1 else "verify"

    if subcmd == "verify":
        sys.exit(cmd_verify(repo_root))
    elif subcmd == "run":
        sys.exit(cmd_run(repo_root))
    elif subcmd == "score":
        sys.exit(cmd_score(repo_root))
    elif subcmd == "analyze":
        sys.exit(cmd_analyze(repo_root))
    else:
        print(f"Unknown subcommand: {subcmd}. Available: verify, run, score, analyze")
        sys.exit(1)


if __name__ == "__main__":
    main()
