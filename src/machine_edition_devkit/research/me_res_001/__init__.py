"""ME-RES-001: Controlled comparative evaluation of PDF, EPUB, RAG, and Machine Edition."""

from machine_edition_devkit.research.me_res_001.protocol import (
    MODEL_CONFIG,
    SYSTEM_INSTRUCTION,
    SCHEDULE_SEED,
    build_condition_context,
    generate_execution_schedule,
)
from machine_edition_devkit.research.me_res_001.runner import (
    execute_full_trial,
    execute_model_inference,
)
from machine_edition_devkit.research.me_res_001.analysis import (
    perform_statistical_analysis,
    compute_paired_bootstrap_ci,
)
from machine_edition_devkit.research.me_res_001.verify import (
    verify_research_integrity,
)

__all__ = [
    "MODEL_CONFIG",
    "SYSTEM_INSTRUCTION",
    "SCHEDULE_SEED",
    "build_condition_context",
    "generate_execution_schedule",
    "execute_full_trial",
    "execute_model_inference",
    "perform_statistical_analysis",
    "compute_paired_bootstrap_ci",
    "verify_research_integrity",
]
