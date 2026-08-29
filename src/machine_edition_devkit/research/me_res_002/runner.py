"""Real generative model execution engine for ME-RES-002 trial."""

import os
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, List, Tuple

from machine_edition_devkit.research.me_res_002.protocol import (
    MODEL_CONFIG,
    SYSTEM_INSTRUCTION,
    SCHEDULE_SEED,
    build_condition_context,
    generate_execution_schedule,
)
from machine_edition_devkit.benchmark.evaluator import BenchmarkScorer


def query_ollama_model(prompt: str, seed: int = SCHEDULE_SEED, max_retries: int = 2) -> Dict[str, Any]:
    """Sends inference request to local Ollama runtime with retry policy."""
    payload = {
        "model": MODEL_CONFIG["model_id"],
        "prompt": prompt,
        "format": "json",
        "stream": False,
        "options": {
            "temperature": MODEL_CONFIG["temperature"],
            "top_p": MODEL_CONFIG["top_p"],
            "num_predict": MODEL_CONFIG["max_output_tokens"],
            "seed": seed,
        },
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        MODEL_CONFIG["endpoint"],
        data=data,
        headers={"Content-Type": "application/json"}
    )

    last_error = None
    for attempt in range(max_retries + 1):
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                raw_body = resp.read().decode("utf-8")
                res = json.loads(raw_body)
                t1 = time.perf_counter()
                latency_ms = round((t1 - t0) * 1000, 2)
                response_text = res.get("response", "").strip()

                input_tokens = res.get("prompt_eval_count", 0)
                if not input_tokens:
                    input_tokens = len(prompt.split()) + 20
                output_tokens = res.get("eval_count", 0)
                if not output_tokens:
                    output_tokens = len(response_text.split()) + 10
                total_tokens = input_tokens + output_tokens

                return {
                    "raw_response": response_text,
                    "latency_ms": latency_ms,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens,
                    "attempt": attempt,
                    "status": "SUCCESS",
                }
        except Exception as e:
            last_error = str(e)
            time.sleep(1.0)

    return {
        "raw_response": "",
        "latency_ms": 0.0,
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "attempt": max_retries,
        "status": "EXECUTION_ERROR",
        "error": last_error,
    }


def execute_real_model_inference(
    question: str,
    context: str,
    condition: str,
    task_id: str,
    replicate: int,
) -> Dict[str, Any]:
    """Formats prompt, invokes real model, and parses standardized structured answer."""
    prompt = f"""{SYSTEM_INSTRUCTION}

---
CONTEXT:
{context}
---

QUESTION:
{question}
"""
    # Deterministic seed per cell
    cell_seed = (SCHEDULE_SEED + replicate * 1000 + int(task_id.replace("ME-BENCH-", ""))) % (2**31 - 1)
    call_res = query_ollama_model(prompt, seed=cell_seed)

    if call_res["status"] != "SUCCESS":
        return {
            "raw_response": "",
            "parsed_response": {
                "answer": "Execution error during inference.",
                "source_references": [],
                "relationships": [],
                "constraints_observed": [],
                "support_status": "unsupported",
            },
            "latency_ms": call_res["latency_ms"],
            "input_tokens": call_res["input_tokens"],
            "output_tokens": call_res["output_tokens"],
            "total_tokens": call_res["total_tokens"],
            "parse_status": "EXECUTION_ERROR",
            "error": call_res.get("error"),
        }

    raw_text = call_res["raw_response"]
    parsed_obj = {}
    parse_status = "SUCCESS"

    try:
        parsed_obj = json.loads(raw_text)
    except Exception:
        # Attempt to extract JSON from markdown fencing if present
        if "```json" in raw_text:
            try:
                extracted = raw_text.split("```json")[1].split("```")[0].strip()
                parsed_obj = json.loads(extracted)
            except Exception:
                parse_status = "JSON_PARSE_ERROR"
        elif "{" in raw_text and "}" in raw_text:
            try:
                start = raw_text.find("{")
                end = raw_text.rfind("}") + 1
                parsed_obj = json.loads(raw_text[start:end])
            except Exception:
                parse_status = "JSON_PARSE_ERROR"
        else:
            parse_status = "JSON_PARSE_ERROR"

    if parse_status == "JSON_PARSE_ERROR":
        parsed_obj = {
            "answer": raw_text,
            "source_references": [],
            "relationships": [],
            "constraints_observed": [],
            "support_status": "supported",
        }

    # Ensure required fields exist in parsed object
    if "answer" not in parsed_obj:
        parsed_obj["answer"] = str(parsed_obj)
    if "source_references" not in parsed_obj:
        parsed_obj["source_references"] = []
    if "relationships" not in parsed_obj:
        parsed_obj["relationships"] = []
    if "constraints_observed" not in parsed_obj:
        parsed_obj["constraints_observed"] = []
    if "support_status" not in parsed_obj:
        parsed_obj["support_status"] = "supported"

    return {
        "raw_response": raw_text,
        "parsed_response": parsed_obj,
        "latency_ms": call_res["latency_ms"],
        "input_tokens": call_res["input_tokens"],
        "output_tokens": call_res["output_tokens"],
        "total_tokens": call_res["total_tokens"],
        "parse_status": parse_status,
    }


def execute_calibration_phase(repo_root: Path) -> Dict[str, Any]:
    """Executes the 8 calibration tasks across 4 conditions (32 runs) to verify scorer compatibility."""
    bench_dir = repo_root / "benchmark"
    res_dir = repo_root / "research" / "me-res-002"
    calib_dir = res_dir / "runs" / "calibration"
    calib_dir.mkdir(parents=True, exist_ok=True)

    tasks = [json.loads(line) for line in (bench_dir / "tasks.jsonl").read_text(encoding="utf-8").strip().splitlines()]
    calib_tasks = [t for t in tasks if t["split"] == "calibration"]
    conditions = ["PDF", "EPUB", "RAG", "Machine_Edition"]

    scorer = BenchmarkScorer(bench_dir)
    calib_records = []
    scored_records = []

    for t in calib_tasks:
        for cond in conditions:
            run_id = f"calib-{t['benchmark_id']}-{cond}"
            ctx, ctx_sha = build_condition_context(t, cond, repo_root)
            inf = execute_real_model_inference(t["question"], ctx, cond, t["benchmark_id"], replicate=1)

            rec = {
                "run_id": run_id,
                "task_id": t["benchmark_id"],
                "family": t["family"],
                "condition": cond,
                "replicate": 1,
                "model_id": MODEL_CONFIG["model_id"],
                "question": t["question"],
                "context_sha256": ctx_sha,
                "context_length": len(ctx),
                "latency_ms": inf["latency_ms"],
                "input_tokens": inf["input_tokens"],
                "output_tokens": inf["output_tokens"],
                "total_tokens": inf["total_tokens"],
                "raw_response": inf["raw_response"],
                "parsed_response": inf["parsed_response"],
                "parse_status": inf["parse_status"],
                "status": "SUCCESS" if inf["parse_status"] != "EXECUTION_ERROR" else "EXECUTION_ERROR",
            }
            (calib_dir / f"{run_id}.json").write_text(json.dumps(rec, indent=2), encoding="utf-8")
            calib_records.append(rec)

            # Test Scorer Compatibility
            clean_rels = []
            for r in inf["parsed_response"].get("relationships", []):
                if isinstance(r, dict):
                    clean_rels.append(r)
                elif isinstance(r, str):
                    clean_rels.append({"predicate": r})

            sub = {
                "benchmark_id": t["benchmark_id"],
                "condition_id": f"cond-{cond.lower()}-v0.1",
                "run_id": run_id,
                "answer": inf["parsed_response"].get("answer", ""),
                "provenance": [str(r) for r in inf["parsed_response"].get("source_references", []) if str(r).startswith("prov.")],
                "provenance_urls": [str(r) for r in inf["parsed_response"].get("source_references", []) if str(r).startswith("http")],
                "relationships": clean_rels,
                "abstention": inf["parsed_response"].get("support_status") == "unsupported",
            }
            eval_res = scorer.score_submission(sub)
            scored_records.append(eval_res)

    return {
        "calibration_count": len(calib_records),
        "scorer_compatible_count": len(scored_records),
        "all_compatible": len(scored_records) == len(calib_records) == 32,
    }


def execute_full_evaluation_trial(repo_root: Path) -> Dict[str, Any]:
    """Executes the full 384-cell evaluation trial over the frozen schedule."""
    bench_dir = repo_root / "benchmark"
    res_dir = repo_root / "research" / "me-res-002"
    raw_dir = res_dir / "runs" / "raw"
    parsed_dir = res_dir / "runs" / "parsed"
    scores_dir = res_dir / "scores"

    for d in [raw_dir, parsed_dir, scores_dir]:
        d.mkdir(parents=True, exist_ok=True)

    tasks = [json.loads(line) for line in (bench_dir / "tasks.jsonl").read_text(encoding="utf-8").strip().splitlines()]
    eval_tasks = [t for t in tasks if t["split"] == "evaluation"]
    conditions = ["PDF", "EPUB", "RAG", "Machine_Edition"]

    # Load frozen schedule
    schedule_file = res_dir / "RUN-SCHEDULE.json"
    if schedule_file.exists():
        schedule = json.loads(schedule_file.read_text(encoding="utf-8"))
    else:
        schedule = generate_execution_schedule(eval_tasks, conditions, replicates=3, seed=SCHEDULE_SEED)
        schedule_file.write_text(json.dumps(schedule, indent=2), encoding="utf-8")

    task_map = {t["benchmark_id"]: t for t in eval_tasks}
    raw_eval_runs = []
    scorer = BenchmarkScorer(bench_dir)
    scored_records = []

    for item in schedule:
        t_id = item["benchmark_id"]
        task = task_map[t_id]
        cond = item["condition"]
        rep = item["replicate"]
        run_id = f"eval-{t_id}-{cond}-rep{rep}"

        ctx, ctx_sha = build_condition_context(task, cond, repo_root)
        inf = execute_real_model_inference(task["question"], ctx, cond, t_id, rep)

        run_record = {
            "run_id": run_id,
            "cell_id": item["cell_id"],
            "execution_order": item["execution_order"],
            "task_id": t_id,
            "family": task["family"],
            "condition": cond,
            "replicate": rep,
            "model_id": MODEL_CONFIG["model_id"],
            "question": task["question"],
            "context_sha256": ctx_sha,
            "context_length": len(ctx),
            "latency_ms": inf["latency_ms"],
            "input_tokens": inf["input_tokens"],
            "output_tokens": inf["output_tokens"],
            "total_tokens": inf["total_tokens"],
            "raw_response": inf["raw_response"],
            "parsed_response": inf["parsed_response"],
            "parse_status": inf["parse_status"],
            "status": "SUCCESS" if inf["parse_status"] != "EXECUTION_ERROR" else "EXECUTION_ERROR",
        }
        (raw_dir / f"{run_id}.json").write_text(json.dumps(run_record, indent=2), encoding="utf-8")
        (parsed_dir / f"{run_id}.json").write_text(json.dumps(inf["parsed_response"], indent=2), encoding="utf-8")
        raw_eval_runs.append(run_record)

        # Scorer submission
        clean_rels = []
        for r in inf["parsed_response"].get("relationships", []):
            if isinstance(r, dict):
                clean_rels.append(r)
            elif isinstance(r, str):
                clean_rels.append({"predicate": r})

        sub = {
            "benchmark_id": t_id,
            "condition_id": f"cond-{cond.lower()}-v0.1",
            "run_id": run_id,
            "answer": inf["parsed_response"].get("answer", ""),
            "provenance": [str(r) for r in inf["parsed_response"].get("source_references", []) if str(r).startswith("prov.")],
            "provenance_urls": [str(r) for r in inf["parsed_response"].get("source_references", []) if str(r).startswith("http")],
            "relationships": clean_rels,
            "abstention": inf["parsed_response"].get("support_status") == "unsupported",
        }
        eval_res = scorer.score_submission(sub)

        scored_item = {
            "run_id": run_id,
            "benchmark_id": t_id,
            "family": task["family"],
            "condition": cond,
            "replicate": rep,
            "correctness": eval_res.correctness,
            "provenance_completeness": eval_res.provenance_completeness,
            "unsupported_assertion_rate": eval_res.unsupported_assertion_rate,
            "semantic_invariant_preservation": eval_res.semantic_invariant_preservation,
            "relationship_accuracy": eval_res.relationship_accuracy,
            "constraint_violations": eval_res.constraint_violations,
            "failure_modes": eval_res.failure_modes,
            "latency_ms": inf["latency_ms"],
            "input_tokens": inf["input_tokens"],
            "output_tokens": inf["output_tokens"],
            "total_tokens": inf["total_tokens"],
            "adjudication_notes": eval_res.adjudication_notes,
        }
        scored_records.append(scored_item)

    # Save item-scores.jsonl
    scores_jsonl = "\n".join([json.dumps(r) for r in scored_records]) + "\n"
    (scores_dir / "item-scores.jsonl").write_text(scores_jsonl, encoding="utf-8")

    return {
        "evaluation_runs": len(raw_eval_runs),
        "scored_records": scored_records,
    }
