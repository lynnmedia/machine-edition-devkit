# ME-RES-001: Structured Publication Representation Trial

Controlled comparative evaluation of **PDF**, **EPUB**, **Naive RAG**, and **Machine Edition** representation conditions across 32 frozen evaluation tasks.

## Protocol Summary
* **Tasks**: 32 evaluation items (4 items x 8 task families) from `ME-BENCH-001`.
* **Replicates**: 3 independent runs per cell = 384 evaluation runs.
* **Model**: `eval-model-v01-deterministic` (temperature = 0, top_p = 1.0, max_tokens = 600).
* **Randomization Seed**: `44527555`.

## Reproduction Commands
```bash
# Verify integrity and run completeness
python -m machine_edition_devkit.research.me_res_001 verify

# Score and compute statistical contrasts
python -m machine_edition_devkit.research.me_res_001 score

# Display statistical summary and hypothesis conclusions
python -m machine_edition_devkit.research.me_res_001 analyze
```
