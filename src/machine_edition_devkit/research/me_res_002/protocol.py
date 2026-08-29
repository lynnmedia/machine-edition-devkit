"""Protocol definitions, real model configuration, and representation context builders for ME-RES-002."""

import json
import hashlib
import random
import dataclasses
from pathlib import Path
from typing import Dict, Any, List, Tuple

from machine_edition_devkit.benchmark.adapters import (
    BenchmarkPDFAdapter,
    BenchmarkEPUBAdapter,
    BenchmarkNaiveRAGAdapter,
    BenchmarkMachineEditionAdapter,
)

SCHEDULE_SEED = int(hashlib.sha256("winmedia.machine-edition-representation-benchmark.v0.1:ME-RES-002".encode()).hexdigest()[:8], 16)
# 2476533847

MODEL_CONFIG = {
    "provider": "ollama",
    "runtime": "ollama-local",
    "model_id": "qwen2.5:0.5b",
    "model_version": "qwen2.5:0.5b-instruct-q4_k_m",
    "architecture_family": "qwen2",
    "parameter_count": "490M",
    "neural_language_model": True,
    "arbitrary_unseen_text_capability": True,
    "temperature": 0.0,
    "top_p": 1.0,
    "max_output_tokens": 600,
    "seed": SCHEDULE_SEED,
    "endpoint": "http://localhost:11434/api/generate",
    "tools_enabled": False,
    "web_enabled": False,
    "memory_enabled": False,
    "incremental_cost": "$0.00",
}

SYSTEM_INSTRUCTION = """You are an objective analytical evaluation system.
Answer the user's task using ONLY the supplied source context.
Do not use external knowledge.
Do not invent source references or relationships.
If the supplied material does not support the requested claim, state explicitly that it is unsupported.

Respond in valid JSON adhering strictly to this schema:
{
  "answer": "factual response string or explicit statement of lack of support",
  "source_references": ["list of exact provenance IDs or document locations from context"],
  "relationships": [{"subject": "...", "predicate": "...", "object": "..."}],
  "constraints_observed": ["list of explicit boundaries or scope limits observed"],
  "support_status": "supported" | "partially_supported" | "unsupported"
}
"""


def build_condition_context(task: Dict[str, Any], condition: str, repo_root: Path) -> Tuple[str, str]:
    """Builds representation context using only representation artifacts and question (Gold Firewall enforced)."""
    bench_dir = repo_root / "benchmark"
    q = task["question"]

    if condition == "PDF":
        adapter = BenchmarkPDFAdapter(bench_dir / "representations" / "pdf" / "benchmark-document.pdf")
        text = adapter.get_full_text()
        ctx = f"--- BEGIN PDF DOCUMENT CONTEXT ---\n{text}\n--- END PDF DOCUMENT CONTEXT ---"
    elif condition == "EPUB":
        adapter = BenchmarkEPUBAdapter(bench_dir / "representations" / "epub" / "benchmark-document.epub")
        text = adapter.get_full_text()
        ctx = f"--- BEGIN EPUB PUBLICATION CONTEXT ---\n{text}\n--- END EPUB PUBLICATION CONTEXT ---"
    elif condition == "RAG":
        adapter = BenchmarkNaiveRAGAdapter(bench_dir / "representations" / "rag" / "rag-corpus.json")
        matches = adapter.search_text(q)
        top_matches = matches[:4]  # Frozen top_k = 4
        chunks_text = "\n\n".join([f"[{m.location}]\n{m.matched_text}" for m in top_matches])
        ctx = f"--- BEGIN RETRIEVED RAG CHUNKS (Top-4 BM25) ---\n{chunks_text}\n--- END RETRIEVED RAG CHUNKS ---"
    elif condition == "Machine_Edition":
        adapter = BenchmarkMachineEditionAdapter(bench_dir / "representations" / "machine-edition" / "package")
        units = adapter.edition.find_units(query=q)
        if not units:
            units = list(adapter.edition.units())
        defs = [d for d in adapter.edition.definitions() if any(w in d.definition.lower() or w in d.term.lower() for w in q.lower().split())]
        if not defs:
            defs = list(adapter.edition.definitions())
        bounds = [b for b in adapter.edition.boundaries() if any(w in b.statement.lower() for w in q.lower().split())]
        if not bounds:
            bounds = list(adapter.edition.boundaries())
        rels = list(adapter.edition.relationships())
        provs = list(adapter.edition.provenance_records())

        lines = [
            "--- BEGIN MACHINE EDITION PACKAGE CONTEXT ---",
            "=== MANIFEST ===",
            json.dumps(adapter.edition.manifest, indent=2),
            "=== MEANING UNITS ===",
            "\n".join([json.dumps(dataclasses.asdict(u)) for u in units]),
            "=== DEFINITIONS ===",
            "\n".join([json.dumps(dataclasses.asdict(d)) for d in defs]),
            "=== BOUNDARIES ===",
            "\n".join([json.dumps(dataclasses.asdict(b)) for b in bounds]),
            "=== RELATIONSHIPS ===",
            "\n".join([json.dumps(dataclasses.asdict(r)) for r in rels]),
            "=== PROVENANCE LEDGER ===",
            "\n".join([json.dumps(dataclasses.asdict(p)) for p in provs]),
            "--- END MACHINE EDITION PACKAGE CONTEXT ---",
        ]
        ctx = "\n".join(lines)
    else:
        raise ValueError(f"Unknown condition: {condition}")

    ctx_sha = hashlib.sha256(ctx.encode("utf-8")).hexdigest()
    return ctx, ctx_sha


def generate_execution_schedule(tasks: List[Dict[str, Any]], conditions: List[str], replicates: int, seed: int) -> List[Dict[str, Any]]:
    """Generates deterministic pseudo-randomized execution schedule."""
    schedule = []
    cell_id = 1
    for t in tasks:
        for cond in conditions:
            for rep in range(1, replicates + 1):
                schedule.append({
                    "cell_id": cell_id,
                    "benchmark_id": t["benchmark_id"],
                    "family": t["family"],
                    "condition": cond,
                    "replicate": rep,
                    "question": t["question"],
                })
                cell_id += 1

    rng = random.Random(seed)
    rng.shuffle(schedule)
    for idx, item in enumerate(schedule, start=1):
        item["execution_order"] = idx
    return schedule
