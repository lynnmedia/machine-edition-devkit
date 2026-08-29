"""Machine Edition Representation Benchmark (ME-BENCH-001) v0.1 evaluation suite."""

from machine_edition_devkit.benchmark.constants import (
    BENCHMARK_ID,
    BENCHMARK_TITLE,
    BENCHMARK_VERSION,
    BENCHMARK_STATUS,
    SPECIFICATION_AUTHORITY,
    CORPUS_LINEAGE,
    TASK_FAMILIES,
    FAILURE_TAXONOMY,
    SCORING_DIMENSIONS,
)
from machine_edition_devkit.benchmark.evaluator import (
    BenchmarkScorer,
    EvaluationRecord,
    run_synthetic_scorer_fixtures,
)
from machine_edition_devkit.benchmark.integrity import (
    verify_benchmark_integrity,
)
from machine_edition_devkit.benchmark.parity import (
    verify_information_parity,
)
from machine_edition_devkit.benchmark.rebuild import (
    rebuild_all_benchmark_artifacts,
)

__all__ = [
    "BENCHMARK_ID",
    "BENCHMARK_TITLE",
    "BENCHMARK_VERSION",
    "BENCHMARK_STATUS",
    "SPECIFICATION_AUTHORITY",
    "CORPUS_LINEAGE",
    "TASK_FAMILIES",
    "FAILURE_TAXONOMY",
    "SCORING_DIMENSIONS",
    "BenchmarkScorer",
    "EvaluationRecord",
    "run_synthetic_scorer_fixtures",
    "verify_benchmark_integrity",
    "verify_information_parity",
    "rebuild_all_benchmark_artifacts",
]
