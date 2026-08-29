# Hugging Face Dataset Publication Handoff

* **Target Dataset**: `https://huggingface.co/datasets/lynnmedia/machine-edition-benchmark`
* **Local Export Staging**: `dist/hf-dataset/`
* **Upload Manifest**: `dist/hf-dataset/UPLOAD-MANIFEST.json` (33 files, verified sha256 checksums)

---

## 1. Summary of Dataset Contents
The local export staging directory `dist/hf-dataset/` is prepared and self-contained:
* **`README.md`**: Complete conforming Dataset Card with task taxonomy, evaluation guidelines, limitation disclosures, and citation bindings.
* **`tasks.jsonl`**: 40 benchmark task definitions (8 calibration, 32 evaluation items across 8 task families) under the gold firewall.
* **`gold/`**: Complete gold response ledgers for offline scoring (`factual_retrieval.jsonl`, `relationship_retrieval.jsonl`, `hierarchy_preservation.jsonl`, `provenance_tracing.jsonl`, `boundary_constraint_recognition.jsonl`, `ambiguity_handling.jsonl`, `multi_resolution_retrieval.jsonl`, `unsupported_claim_detection.jsonl`).
* **`representations/`**: 4 representation corpora under guaranteed 16/16 information parity (`pdf/`, `epub/`, `rag/`, `package/`).
* **`manifest.json` & `integrity-manifest.json`**: Package and sha256 verification ledgers.
* **`RIGHTS.md` & `THREATS-TO-VALIDITY.md`**: Legal governance, evaluation-only usage constraints, and threats to validity disclosures.

---

## 2. Minimal Human Publication Procedure

### Option A: Via Hugging Face Web UI (Easiest)
1. Sign in to [Hugging Face](https://huggingface.co) under the `lynnmedia` organization (or personal account).
2. Navigate to [New Dataset](https://huggingface.co/new-dataset).
   * **Owner**: `lynnmedia`
   * **Dataset name**: `machine-edition-benchmark`
   * **License**: `MIT`
   * **Visibility**: `Public`
3. Click **Create Dataset**.
4. In the created repository, click **Add file** → **Upload folder** (or drag & drop the contents of `dist/hf-dataset/`).
5. Commit the files to `main`.

### Option B: Via Git / Hugging Face CLI
```bash
# 1. Authenticate with Hugging Face CLI
huggingface-cli login

# 2. Clone the remote repo
git clone https://huggingface.co/datasets/lynnmedia/machine-edition-benchmark /tmp/hf-repo

# 3. Copy prepared export files into repo
cp -R dist/hf-dataset/* /tmp/hf-repo/

# 4. Commit and push
cd /tmp/hf-repo
git add .
git commit -m "feat: initial publication of ME-BENCH v0.1 evaluation dataset"
git push origin main
```

---

## 3. Post-Publication Verification
Once published, verify anonymous public retrieval:
```bash
curl -I https://huggingface.co/datasets/lynnmedia/machine-edition-benchmark
```
When HTTP 200 is returned anonymously, the program determination `ME_DIST_HF_PUBLIC_SURFACE_VERIFIED` is officially earned.
