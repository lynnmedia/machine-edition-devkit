"""ME-RES-002: Real Generative Model Representation Trial."""

from machine_edition_devkit.research.me_res_002.protocol import (
    MODEL_CONFIG,
    SYSTEM_INSTRUCTION,
    SCHEDULE_SEED,
    build_condition_context,
    generate_execution_schedule,
)
from machine_edition_devkit.research.me_res_002.runner import (
    execute_calibration_phase,
    execute_full_evaluation_trial,
    execute_real_model_inference,
)
from machine_edition_devkit.research.me_res_002.analysis import (
    perform_me_res_002_statistical_analysis,
    compute_paired_bootstrap_ci,
)
from machine_edition_devkit.research.me_res_002.verify import (
    verify_me_res_002_integrity,
)

__all__ = [
    "MODEL_CONFIG",
    "SYSTEM_INSTRUCTION",
    "SCHEDULE_SEED",
    "build_condition_context",
    "generate_execution_schedule",
    "execute_calibration_phase",
    "execute_full_evaluation_trial",
    "execute_real_model_inference",
    "perform_me_res_002_statistical_analysis",
    "compute_paired_bootstrap_ci",
    "verify_me_res_002_integrity",
]
