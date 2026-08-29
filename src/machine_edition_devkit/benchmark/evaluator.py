"""Offline deterministic scoring engine and synthetic fixture validator for ME-BENCH-001."""

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import re
from typing import List, Dict, Any, Optional

from machine_edition_devkit.benchmark.constants import (
    FAILURE_TAXONOMY,
    SCORING_DIMENSIONS,
)


@dataclass
class EvaluationRecord:
    benchmark_id: str
    condition_id: str
    run_id: str
    correctness: float  # 0.0 to 1.0
    provenance_completeness: float  # 0.0 to 1.0
    unsupported_assertion_rate: float
    semantic_invariant_preservation: float  # 0.0 to 1.0
    relationship_accuracy: float  # 0.0 to 1.0
    constraint_violations: int
    failure_modes: List[str]
    adjudication_notes: str


class BenchmarkScorer:
    """Offline evaluator consuming standardized model/system submissions against frozen gold ledgers."""

    def __init__(self, benchmark_root: Path):
        self.root = benchmark_root
        self.gold_answers = self._load_jsonl(self.root / "gold" / "answers.jsonl")
        self.gold_provenance = self._load_jsonl(self.root / "gold" / "provenance.jsonl")
        self.gold_relationships = self._load_jsonl(self.root / "gold" / "relationships.jsonl")
        self.gold_constraints = self._load_jsonl(self.root / "gold" / "constraints.jsonl")
        self.tasks = self._load_jsonl(self.root / "tasks.jsonl")

    def _load_jsonl(self, path: Path) -> Dict[str, Dict[str, Any]]:
        records = {}
        if not path.exists():
            return records
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                data = json.loads(line)
                records[data["benchmark_id"]] = data
        return records

    def score_submission(self, sub: Dict[str, Any]) -> EvaluationRecord:
        b_id = sub.get("benchmark_id", "")
        cond_id = sub.get("condition_id", "unknown")
        run_id = sub.get("run_id", "default")
        raw_answer = str(sub.get("answer", "")).strip()
        answer = raw_answer.lower()
        prov_list = sub.get("provenance", [])
        prov_urls = sub.get("provenance_urls", [])
        relationships = sub.get("relationships", [])
        abstention = sub.get("abstention", False)

        if b_id not in self.tasks:
            return EvaluationRecord(
                benchmark_id=b_id,
                condition_id=cond_id,
                run_id=run_id,
                correctness=0.0,
                provenance_completeness=0.0,
                unsupported_assertion_rate=0.0,
                semantic_invariant_preservation=0.0,
                relationship_accuracy=0.0,
                constraint_violations=1,
                failure_modes=["EXECUTION_ERROR"],
                adjudication_notes=f"Unknown benchmark ID: {b_id}",
            )

        task = self.tasks[b_id]
        gold_ans = self.gold_answers.get(b_id, {})
        gold_prov = self.gold_provenance.get(b_id, {})
        gold_rel = self.gold_relationships.get(b_id, {})
        gold_con = self.gold_constraints.get(b_id, {})

        is_unsupported = gold_ans.get("is_unsupported", False)
        requires_qual = gold_ans.get("requires_qualification", False)
        req_concepts = [c.lower() for c in gold_ans.get("required_concepts", [])]
        prohibited = [p.lower() for p in gold_ans.get("prohibited_assertions", [])]
        req_prov_ids = gold_prov.get("required_provenance_ids", [])
        req_prov_urls = gold_prov.get("required_provenance_urls", [])
        req_triples = gold_rel.get("required_triples", [])
        req_boundaries = gold_con.get("required_boundaries", [])

        failure_modes = []
        notes = []

        # 1. Correctness & Unsupported Detection
        correctness = 0.0
        unsupported_assertion_rate = 0.0
        constraint_violations = 0

        # Check prohibited assertions
        prohibited_matches = [p for p in prohibited if p in answer]
        if prohibited_matches:
            constraint_violations += len(prohibited_matches)
            unsupported_assertion_rate += float(len(prohibited_matches))
            failure_modes.append("UNSUPPORTED_ASSERTION")
            notes.append(f"Answer asserted prohibited claims: {prohibited_matches}")

        if is_unsupported:
            # Gold expects abstention / refusal / statement of lack of support
            abstention_phrases = [
                "not stated", "unsupported", "not supported", "outside source scope",
                "insufficient evidence", "does not specify", "not mentioned", "no information",
                "category error"
            ]
            has_abstention_text = any(phrase in answer for phrase in abstention_phrases)
            if abstention or has_abstention_text:
                correctness = 1.0
                notes.append("Correctly abstained/identified unsupported request.")
            else:
                correctness = 0.0
                failure_modes.append("ANSWER_WHEN_UNSUPPORTED")
                notes.append("Confabulated or provided affirmative answer to unsupported claim.")
        else:
            # Supported task: abstention is an error
            if abstention:
                correctness = 0.0
                failure_modes.append("REFUSAL_WHEN_SUPPORTED")
                notes.append("Incorrectly refused / abstained on supported question.")
            else:
                if not answer:
                    correctness = 0.0
                    failure_modes.append("OMISSION")
                    notes.append("Empty answer provided.")
                else:
                    concept_hits = sum(1 for c in req_concepts if c in answer)
                    total_concepts = max(len(req_concepts), 1)
                    concept_ratio = concept_hits / total_concepts

                    if concept_ratio == 1.0 and not prohibited_matches:
                        correctness = 1.0
                    elif concept_ratio >= 0.5 and not prohibited_matches:
                        correctness = 0.5
                        failure_modes.append("OMISSION")
                        notes.append(f"Partial answer: {concept_hits}/{total_concepts} required concepts.")
                    else:
                        correctness = 0.0
                        failure_modes.append("INCORRECT_FACT")
                        notes.append(f"Incorrect fact or missing concepts: {concept_hits}/{total_concepts}.")

        # 2. Ambiguity Handling check
        if requires_qual and not is_unsupported:
            qual_terms = ["qualification", "qualify", "multiple", "vary", "outside", "does not mandate", "separated", "distinct", "underspecified"]
            if not any(qt in answer for qt in qual_terms):
                failure_modes.append("AMBIGUITY_COLLAPSE")
                notes.append("Answer collapsed ambiguous/underspecified problem into ungrounded certainty.")
                correctness = 0.0

        # 3. Hierarchy Preservation check
        if task.get("family") == "hierarchy_preservation" and correctness < 1.0:
            if "HIERARCHY_ERROR" not in failure_modes:
                failure_modes.append("HIERARCHY_ERROR")

        # 4. Multi-Resolution check
        if task.get("family") == "multi_resolution_retrieval" and correctness < 1.0:
            if "RESOLUTION_ERROR" not in failure_modes:
                failure_modes.append("RESOLUTION_ERROR")

        # 5. Boundary / Constraint check
        if task.get("family") == "boundary_constraint_recognition":
            if prohibited_matches or correctness < 1.0:
                if "BOUNDARY_VIOLATION" not in failure_modes:
                    failure_modes.append("BOUNDARY_VIOLATION")

        # 6. Provenance completeness & fabrication
        prov_score = 1.0
        # Check for fabricated provenance
        known_valid_urls = [
            "https://winmedia.com/machine-editions/editions/srow",
            "https://winmedia.com/frameworks/srow",
        ]
        known_valid_prov_ids = [
            "prov.srow-public-companion-release",
            "prov.public-srow-framework",
        ]
        has_fabricated = False
        for p in prov_list:
            if p not in known_valid_prov_ids:
                has_fabricated = True
        for u in prov_urls:
            if u not in known_valid_urls:
                has_fabricated = True

        if has_fabricated:
            prov_score = 0.0
            failure_modes.append("PROVENANCE_FABRICATED")
            notes.append("Fabricated provenance identifiers or URLs detected.")
        elif req_prov_ids or req_prov_urls:
            matched_ids = sum(1 for pid in req_prov_ids if pid in prov_list)
            matched_urls = sum(1 for u in req_prov_urls if u in prov_urls)
            tot_req = len(req_prov_ids) + len(req_prov_urls)
            if tot_req > 0:
                prov_score = (matched_ids + matched_urls) / tot_req
                if prov_score < 1.0:
                    failure_modes.append("PROVENANCE_MISSING")
                    notes.append("Missing required provenance ledger links.")
        else:
            prov_score = 1.0

        # 7. Relationship Accuracy
        rel_accuracy = 1.0
        if req_triples:
            if not relationships:
                found_in_answer = all(
                    (t["predicate"].lower() in answer)
                    for t in req_triples
                )
                if found_in_answer:
                    rel_accuracy = 0.8
                else:
                    rel_accuracy = 0.0
                    failure_modes.append("RELATIONSHIP_ERROR")
                    notes.append("Missing required typed relationship edge.")
            else:
                matched_triples = 0
                for req_t in req_triples:
                    for sub_t in relationships:
                        if (
                            req_t.get("predicate", "").lower() == str(sub_t.get("predicate", "")).lower()
                            and (not req_t.get("subject") or req_t.get("subject") == sub_t.get("subject"))
                            and (not req_t.get("object") or req_t.get("object") == sub_t.get("object"))
                        ):
                            matched_triples += 1
                            break
                rel_accuracy = matched_triples / max(len(req_triples), 1)
                if rel_accuracy < 1.0:
                    failure_modes.append("RELATIONSHIP_ERROR")
                    notes.append("Incorrect relationship predicate or endpoint direction.")

        # 8. Semantic Invariant Preservation
        invariant_score = 1.0
        if "UNSUPPORTED_ASSERTION" in failure_modes or "BOUNDARY_VIOLATION" in failure_modes or "AMBIGUITY_COLLAPSE" in failure_modes:
            invariant_score = 0.0
        elif correctness < 1.0:
            invariant_score = correctness

        if not failure_modes:
            failure_modes.append("NONE")

        return EvaluationRecord(
            benchmark_id=b_id,
            condition_id=cond_id,
            run_id=run_id,
            correctness=round(correctness, 2),
            provenance_completeness=round(prov_score, 2),
            unsupported_assertion_rate=round(unsupported_assertion_rate, 2),
            semantic_invariant_preservation=round(invariant_score, 2),
            relationship_accuracy=round(rel_accuracy, 2),
            constraint_violations=constraint_violations,
            failure_modes=failure_modes,
            adjudication_notes="; ".join(notes) if notes else "Evaluated cleanly with zero errors.",
        )


def run_synthetic_scorer_fixtures(benchmark_root: Path) -> Dict[str, Any]:
    """Executes synthetic fixture tests proving scorer detects all failure modes and perfect cases."""
    scorer = BenchmarkScorer(benchmark_root)
    fixtures = [
        # 1. Perfect answer
        {
            "name": "perfect_factual_answer",
            "submission": {
                "benchmark_id": "ME-BENCH-001",
                "condition_id": "cond-machine-edition-v0.1",
                "answer": "Structured Resolution-Oriented Writing (SROW) is a communication protocol for making structured knowledge readable and navigable by both humans and machines.",
                "provenance": ["prov.public-srow-framework"],
                "provenance_urls": ["https://winmedia.com/frameworks/srow"],
                "relationships": [],
                "abstention": False,
            },
            "expected_correctness": 1.0,
            "expected_failure_mode": "NONE",
        },
        # 2. Wrong answer
        {
            "name": "incorrect_fact_answer",
            "submission": {
                "benchmark_id": "ME-BENCH-001",
                "condition_id": "cond-pdf-v0.1",
                "answer": "SROW is a quantum mechanics simulation engine.",
                "provenance": [],
                "abstention": False,
            },
            "expected_correctness": 0.0,
            "expected_failure_mode": "INCORRECT_FACT",
        },
        # 3. Partial answer / omission
        {
            "name": "omission_partial_answer",
            "submission": {
                "benchmark_id": "ME-BENCH-001",
                "condition_id": "cond-rag-v0.1",
                "answer": "It is a communication protocol for structured knowledge.",
                "provenance": [],
                "abstention": False,
            },
            "expected_correctness": 0.5,
            "expected_failure_mode": "OMISSION",
        },
        # 4. Unsupported addition / prohibited assertion
        {
            "name": "unsupported_prohibited_assertion",
            "submission": {
                "benchmark_id": "ME-BENCH-001",
                "condition_id": "cond-rag-v0.1",
                "answer": "SROW is a communication protocol for structured knowledge readable by humans and machines, and serves as a deep learning framework and cognition architecture.",
                "provenance": ["prov.public-srow-framework"],
                "abstention": False,
            },
            "expected_correctness": 0.0,
            "expected_failure_mode": "UNSUPPORTED_ASSERTION",
        },
        # 5. Fabricated provenance
        {
            "name": "fabricated_provenance",
            "submission": {
                "benchmark_id": "ME-BENCH-016",
                "condition_id": "cond-rag-v0.1",
                "answer": "The SHA-256 release hash is 0cd42e724bcd7d4b54c0f850a51ef7b875152cd01f7a20f5b7b34e0d73b5d181.",
                "provenance": ["prov.fake-invented-source"],
                "provenance_urls": ["https://fake-citation-hallucination.org"],
                "abstention": False,
            },
            "expected_correctness": 1.0,
            "expected_failure_mode": "PROVENANCE_FABRICATED",
        },
        # 6. Missing provenance
        {
            "name": "missing_provenance",
            "submission": {
                "benchmark_id": "ME-BENCH-016",
                "condition_id": "cond-pdf-v0.1",
                "answer": "The SHA-256 release hash is 0cd42e724bcd7d4b54c0f850a51ef7b875152cd01f7a20f5b7b34e0d73b5d181.",
                "provenance": [],
                "provenance_urls": [],
                "abstention": False,
            },
            "expected_correctness": 1.0,
            "expected_failure_mode": "PROVENANCE_MISSING",
        },
        # 7. Reversed relationship error
        {
            "name": "reversed_relationship_error",
            "submission": {
                "benchmark_id": "ME-BENCH-006",
                "condition_id": "cond-rag-v0.1",
                "answer": "Lineage predicate is derives_from.",
                "relationships": [{"subject": "srow.bench.mu.006", "predicate": "derives_from", "object": "srow.bench.mu.005"}],
                "abstention": False,
            },
            "expected_failure_mode": "RELATIONSHIP_ERROR",
        },
        # 8. Boundary violation
        {
            "name": "boundary_violation",
            "submission": {
                "benchmark_id": "ME-BENCH-021",
                "condition_id": "cond-rag-v0.1",
                "answer": "Yes, SROW is an internal neural thought model and cognition architecture.",
                "abstention": False,
            },
            "expected_correctness": 0.0,
            "expected_failure_mode": "BOUNDARY_VIOLATION",
        },
        # 9. Appropriate ambiguity handling
        {
            "name": "appropriate_ambiguity_handling",
            "submission": {
                "benchmark_id": "ME-BENCH-027",
                "condition_id": "cond-machine-edition-v0.1",
                "answer": "When source evidence is underspecified or accommodates multiple valid interpretations, an agent must provide explicit qualification rather than collapsing ambiguity into ungrounded certainty.",
                "abstention": False,
            },
            "expected_correctness": 1.0,
            "expected_failure_mode": "NONE",
        },
        # 10. Ambiguity collapse
        {
            "name": "ambiguity_collapse",
            "submission": {
                "benchmark_id": "ME-BENCH-027",
                "condition_id": "cond-rag-v0.1",
                "answer": "Guess the most likely answer confidently without mentioning alternatives.",
                "abstention": False,
            },
            "expected_failure_mode": "AMBIGUITY_COLLAPSE",
        },
        # 11. Correct abstention on unsupported request
        {
            "name": "correct_unsupported_abstention",
            "submission": {
                "benchmark_id": "ME-BENCH-036",
                "condition_id": "cond-machine-edition-v0.1",
                "answer": "The source does not specify or support quantum key distribution ciphers; the claim is outside source scope.",
                "abstention": True,
            },
            "expected_correctness": 1.0,
            "expected_failure_mode": "NONE",
        },
        # 12. Confabulation / answer when unsupported
        {
            "name": "answer_when_unsupported_confabulation",
            "submission": {
                "benchmark_id": "ME-BENCH-036",
                "condition_id": "cond-rag-v0.1",
                "answer": "The recommended cipher is BB84 quantum protocol with 4096-bit photon entanglement.",
                "abstention": False,
            },
            "expected_correctness": 0.0,
            "expected_failure_mode": "ANSWER_WHEN_UNSUPPORTED",
        },
        # 13. Refusal when supported
        {
            "name": "refusal_when_supported",
            "submission": {
                "benchmark_id": "ME-BENCH-001",
                "condition_id": "cond-rag-v0.1",
                "answer": "I cannot answer this question.",
                "abstention": True,
            },
            "expected_correctness": 0.0,
            "expected_failure_mode": "REFUSAL_WHEN_SUPPORTED",
        },
    ]

    fixture_results = []
    all_passed = True

    for fix in fixtures:
        res = scorer.score_submission(fix["submission"])
        exp_corr = fix.get("expected_correctness")
        exp_fail = fix.get("expected_failure_mode")

        corr_ok = (exp_corr is None) or (res.correctness == exp_corr)
        fail_ok = (exp_fail is None) or (exp_fail in res.failure_modes)

        passed = corr_ok and fail_ok
        if not passed:
            all_passed = False

        fixture_results.append({
            "name": fix["name"],
            "benchmark_id": fix["submission"]["benchmark_id"],
            "passed": passed,
            "correctness": res.correctness,
            "expected_correctness": exp_corr,
            "failure_modes": res.failure_modes,
            "expected_failure_mode": exp_fail,
            "notes": res.adjudication_notes,
        })

    return {
        "fixture_count": len(fixtures),
        "passed_count": sum(1 for r in fixture_results if r["passed"]),
        "all_passed": all_passed,
        "results": fixture_results,
    }
