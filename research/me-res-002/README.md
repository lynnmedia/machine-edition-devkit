# ME-RES-002: Real Generative Model Representation Trial

Controlled comparative evaluation of **PDF**, **EPUB**, **Naive RAG**, and **Machine Edition** representation conditions using a genuine neural generative language model (`qwen2.5:0.5b` via Ollama) across 32 frozen evaluation tasks.

## Protocol Summary
* **Tasks**: 32 evaluation items (4 items x 8 task families) from `ME-BENCH-001`.
* **Replicates**: 3 independent runs per cell = 384 evaluation runs.
* **Model**: `qwen2.5:0.5b` (Qwen 2.5 0.5B Instruct, 490M dense parameters, temperature = 0, top_p = 1.0, max_tokens = 600).
* **Schedule Seed**: `2476533847`.

## Reproduction Commands
```bash
# Verify integrity and run completeness
python -m machine_edition_devkit.research.me_res_002 verify

# Score and compute statistical contrasts
python -m machine_edition_devkit.research.me_res_002 score

# Display statistical summary, replicate stability, and hypothesis conclusions
python -m machine_edition_devkit.research.me_res_002 analyze
```
