"""CLI entrypoint for ME-RES-002 research trial execution, scoring, and verification."""

import sys
import json
from pathlib import Path

from machine_edition_devkit.research.me_res_002.verify import verify_me_res_002_integrity
from machine_edition_devkit.research.me_res_002.runner import execute_calibration_phase, execute_full_evaluation_trial
from machine_edition_devkit.research.me_res_002.analysis import perform_me_res_002_statistical_analysis


def cmd_verify(repo_root: Path) -> int:
    print("================================================================================")
    print("ME-RES-002: Real Generative Model Research Trial Verification")
    print("================================================================================")
    res = verify_me_res_002_integrity(repo_root)
    for c in res["checks"]:
        status = "PASS" if c["passed"] else "FAIL"
        print(f"  [{status}] {c['name']:<35} -> {c['details']}")

    if res["all_passed"]:
        print("\n================================================================================")
        print("DETERMINATION: ME_RES_002_CONTROLLED_TRIAL_EXECUTED")
        print("EVIDENCE DETERMINATION: ME_RES_002_EVIDENCE_PACKAGE_COMPLETE")
        print("================================================================================")
        return 0
    else:
        print("\nVerification failed.")
        return 1


def cmd_calibrate(repo_root: Path) -> int:
    print("Executing ME-RES-002 calibration phase across 8 tasks x 4 conditions (32 runs)...")
    res = execute_calibration_phase(repo_root)
    print(f"Calibration completed: {res['calibration_count']}/32 runs. Scorer compatibility: {res['all_compatible']}.")
    return 0 if res["all_compatible"] else 1


def cmd_run(repo_root: Path) -> int:
    print("Executing full ME-RES-002 384-cell real model trial...")
    res = execute_full_evaluation_trial(repo_root)
    print(f"Evaluation completed: {res['evaluation_runs']} runs.")
    print("Performing statistical analysis...")
    perform_me_res_002_statistical_analysis(repo_root)
    print("Analysis complete.")
    return 0


def cmd_score(repo_root: Path) -> int:
    print("Re-scoring evaluation runs and recalculating statistical contrasts...")
    perform_me_res_002_statistical_analysis(repo_root)
    print("Scoring and statistical analysis complete.")
    return 0


def cmd_analyze(repo_root: Path) -> int:
    res = perform_me_res_002_statistical_analysis(repo_root)
    print("\n--- CONDITION SUMMARY ---")
    for cond, stats in res["condition_summary"].items():
        print(f"{cond:<16}: Corr={stats['mean_correctness']:.4f}, Prov={stats['mean_provenance_completeness']:.4f}, Invariant={stats['mean_semantic_invariant_preservation']:.4f}, Rel={stats['mean_relationship_accuracy']:.4f}, Violations={stats['mean_constraint_violations']:.4f}, InTokens={stats['mean_input_tokens']:.1f}")

    print("\n--- REPLICATE STABILITY ---")
    stab = res["replicate_stability"]
    print(f"Identical output rate: {stab['identical_output_rate'] * 100:.1f}%, Consistent support rate: {stab['consistent_support_rate'] * 100:.1f}%")

    print("\n--- TOKEN EFFICIENCY ---")
    for cond, eff in res["token_efficiency"].items():
        print(f"{cond:<16}: Corr/1k={eff['correctness_per_1k_input_tokens']:.4f}, Prov/1k={eff['provenance_per_1k_input_tokens']:.4f}")

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
    elif subcmd == "calibrate":
        sys.exit(cmd_calibrate(repo_root))
    elif subcmd == "run":
        sys.exit(cmd_run(repo_root))
    elif subcmd == "score":
        sys.exit(cmd_score(repo_root))
    elif subcmd == "analyze":
        sys.exit(cmd_analyze(repo_root))
    else:
        print(f"Unknown subcommand: {subcmd}. Available: verify, calibrate, run, score, analyze")
        sys.exit(1)


if __name__ == "__main__":
    main()
