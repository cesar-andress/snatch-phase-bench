# SnatchPhaseBench — Project Audit (Phase 1)

**Audit date:** 2026-07-12  
**Original repository audited (read-only):** `/home/cesar/papers/Paper_TFM-main`  
**Thesis PDF consulted (read-only):** `BMEM_49028285-54566-260531200716 - TFM_-_IA_para_la_deteccion_del_gesto_tecnico_de_la_arrancada_en_halterofilia (1).pdf`  
**Auditor note:** No files in the original repository were modified during this audit.

---

## Executive summary

The student repository is a **partially packaged reproducibility bundle** for an MSc thesis on snatch phase classification using MediaPipe pose keypoints and an LSTM. The codebase is **more mature than a typical thesis dump**: it includes frozen baseline manifests, verification scripts, dataset rebuild tooling, and saved evaluation artifacts.

However, on the machine where this audit was performed, **several critical binary artifacts are Git LFS pointer stubs rather than real files**. As a result, **exact checkpoint reproduction cannot currently be executed here** without fetching LFS objects or obtaining the binaries from the student.

Reconstruction of processed tensors from the included keypoint CSVs and annotations appears **feasible in principle**, and retraining the LSTM from rebuilt data also appears feasible. **No reproduction command was executed successfully during this audit** because the Python environment was not yet installed and the frozen tensors/checkpoint are unavailable locally.

---

## 1. Summary of the original repository

### Verified facts

| Item | Value |
|------|-------|
| Repository path | `/home/cesar/papers/Paper_TFM-main` |
| Primary language | Python |
| Notebooks | **None** (script-only pipeline) |
| Main task | Window-level classification of snatch biomechanical phases from pose sequences |
| Key scripts | `build_phase_dataset.py`, `train_lstm_phases.py`, `evaluate_checkpoint.py`, `verify_project.py` |
| Saved baseline outputs | `outputs/lstm_phases/` |
| Baseline manifest | `baseline_tfm/manifest.json` with SHA-256 checksums |
| Recommended Python | **3.12** (`README.md`, `requirements-original.txt`) |
| Local Python available during audit | **3.12.3** (system), dependencies **not installed** |
| Local git repository in student folder | **No** (directory is not a git checkout on this machine) |

### Reasonable inferences

- The repository was likely exported or copied **without Git LFS pull**, which explains the pointer stubs for large binaries.
- The README and manifest were written **after** thesis submission to improve reproducibility.
- The thesis text still references an older internal layout (`wl_clips/...`) while the packaged repository uses `Paper_TFM-main/...`.

---

## 2. Inventory of important files

### Code and orchestration

| Path | Role |
|------|------|
| `scripts/build_phase_dataset.py` | Builds sliding-window dataset from annotations + keypoints |
| `scripts/train_lstm_phases.py` | Trains LSTM with athlete-level split |
| `scripts/evaluate_checkpoint.py` | Evaluates frozen checkpoint on test athletes |
| `scripts/verify_project.py` | Static integrity checks + optional checkpoint eval |
| `scripts/compare_rebuild_to_baseline.py` | Byte-level comparison of rebuilt vs frozen tensors |
| `scripts/extract_pose.py` | MediaPipe extraction from raw videos |
| `scripts/annotate_phases.py` | Interactive annotation tool (requires videos) |
| `scripts/check_dataset_mismatches.py` | Alignment check across annotations/keypoints/videos |
| `scripts/legacy/*` | Older annotation/training scripts (superseded) |
| `run_reproduction.ps1` | Windows PowerShell end-to-end verification flow |

### Data

| Path | Status on audit machine | Notes |
|------|-------------------------|-------|
| `data/annotations/master_frame_labels.csv` | **Present, real** | 35,825 data rows (+ header) |
| `data/annotations/master_segment_labels.csv` | **Present, real** | Segment-level annotations |
| `data/annotations/frame_labels/` | **Present** | Per-video frame labels |
| `data/annotations/segment_labels/` | **Present** | Per-video segment labels |
| `data/keypoints/` | **Present, real** | **208 CSV files**, ~90 MB total |
| `data/processed/X.npy` | **LFS pointer stub** | 134 bytes, expected ~249 MB |
| `data/processed/y.npy` | **LFS pointer stub** | 131 bytes, expected ~170 KB |
| `data/processed/meta.csv` | **Present, real** | 21,249 rows (+ header); size differs slightly from manifest |
| `data/processed/label_map.csv` | **Present, real** | 8 phase entries incl. `unlabeled` |
| `data/raw_videos/` | **Missing** | Directory does not exist |
| `data/rebuilt/` | **Missing** | Expected after running rebuild script |
| `models/pose_landmarker_full.task` | **LFS pointer stub** | 132 bytes, expected ~9.4 MB |

### Model outputs and reports

| Path | Status on audit machine | Notes |
|------|-------------------------|-------|
| `outputs/lstm_phases/best_model.pt` | **LFS pointer stub** | Cannot load weights |
| `outputs/lstm_phases/athlete_split.json` | **Present, real** | 49 / 10 / 11 athletes |
| `outputs/lstm_phases/classification_report.json` | **Present, real** | Saved test metrics |
| `outputs/lstm_phases/history.csv` | **Present, real** | 13 epochs logged |
| `outputs/lstm_phases/test_predictions.csv` | **Present, real** | 3,877 test windows (inferred from report) |
| `outputs/lstm_phases/confusion_matrix.csv` | **Present, real** | 7×7 matrix |
| `outputs/verification/reproduced_evaluation.json` | **Present, real** | Matches saved report values |
| `outputs/tfm_figures/` | **Present** | Thesis figures |
| `baseline_tfm/manifest.json` | **Present, real** | Checksums for all baseline artifacts |

### Environment

| Path | Notes |
|------|-------|
| `requirements.txt` | Includes `-r requirements-original.txt` |
| `requirements-original.txt` | Frozen pip environment (Python 3.12-era packages) |
| Notable pinned packages | `torch==2.10.0`, `mediapipe==0.10.32`, `scikit-learn==1.8.0`, `numpy==2.4.3` |
| Unused dependency | `openai==2.32.0` listed but **not referenced in code** |

---

## 3. Mapping: thesis methodology vs actual implementation

| Thesis claim | Repository evidence | Match? |
|--------------|---------------------|--------|
| 208 videos | 208 keypoint CSVs; 208 unique videos in annotations | **Yes (verified)** |
| 70 athletes | 70 keypoint subdirectories; split covers 70 athletes | **Yes (verified)** |
| 7 useful classes (+ `unlabeled`) | `label_map.csv`, `build_phase_dataset.py` | **Yes (verified)** |
| MediaPipe Pose Landmarker, 33 landmarks | `extract_pose.py`, keypoint CSV headers | **Yes (verified)** |
| x, y, z → 99 vars/frame | `build_phase_dataset.py` default (`--no-z` optional) | **Yes (verified)** |
| Window size 31, stride 1 | `build_phase_dataset.py` defaults | **Yes (verified)** |
| 21,249 windows, shape `(21249, 31, 99)` | `meta.csv` row count; manifest; README | **Yes (verified metadata)**; **tensors not locally available** |
| Athlete-level split 49/10/11 | `athlete_split.json` | **Yes (verified)** |
| Test accuracy ≈ 0.9518, macro F1 ≈ 0.9186 | `classification_report.json`, `reproduced_evaluation.json` | **Present in saved reports**; **not re-executed here** |
| LSTM: hidden 128, 1 layer, dropout 0.2 | `train_lstm_phases.py` defaults | **Yes (verified)** |
| Batch 64, epochs 40, lr 1e-3, wd 1e-4, patience 8 | `train_lstm_phases.py` defaults | **Yes (verified)** |
| Train-only standardization | `train_lstm_phases.py::standardize_by_train` | **Yes (verified)** |
| Class-weighted cross-entropy | `train_lstm_phases.py::class_weights` | **Yes (verified)** |
| Evaluation on window samples | `evaluate_checkpoint.py`, saved `test_predictions.csv` | **Yes (verified)** |
| Segment-level metrics (F1@k, edit score) | Not implemented | **No** |
| Path prefix `wl_clips/` | Current repo uses project root paths | **Thesis outdated** |
| Script `annotate_phases_final2.py` | Repo has `annotate_phases.py` + legacy variants | **Name mismatch** |

---

## 4. What can currently be reproduced

### Likely reproducible now (after environment setup)

1. **Static inspection** of annotations, keypoints, split file, saved metrics, confusion matrix, and test predictions.
2. **Dataset rebuild** from `master_frame_labels.csv` + `data/keypoints/` → `data/rebuilt/{X,y,meta,label_map}.npy/csv`.
3. **LSTM retraining** from rebuilt tensors using fixed `athlete_split.json`.
4. **Dataset alignment checks** via `check_dataset_mismatches.py` (without raw videos).

### Not reproducible on this machine without additional artifacts

1. **Exact checkpoint evaluation** (`Accuracy: 0.9517668300`, `Macro-F1: 0.9186193965`) — requires real `best_model.pt` and `X.npy`.
2. **Byte-identical comparison** to frozen `data/processed/X.npy` / `y.npy`.
3. **MediaPipe re-extraction from videos** — no raw videos present; model task file is an LFS stub.
4. **Interactive re-annotation** — requires raw videos.
5. **`verify_project.py --evaluate` end-to-end PASS** — blocked by missing binaries and missing Python deps.

---

## 5. Missing files, dependencies, and blockers

### Critical blockers

| Blocker | Impact | Severity |
|---------|--------|----------|
| Git LFS objects not fetched (`X.npy`, `y.npy`, `best_model.pt`, `pose_landmarker_full.task`) | Cannot run exact baseline evaluation or tensor comparison | **Critical** |
| Python environment not installed | No script execution verified | **High** |
| Raw competition videos absent | Cannot verify pose extraction or annotation UI | **High for full pipeline** |
| `data/rebuilt/` not yet generated | Rebuild path not yet executed | **Medium** |

### Git LFS pointer files detected (verified)

```
data/processed/X.npy          → oid sha256:8497a69a... size 260852852
data/processed/y.npy          → oid sha256:0175c1c3... size 170120
outputs/lstm_phases/best_model.pt → oid sha256:ea5ff9ca... size 478137
models/pose_landmarker_full.task  → oid sha256:4eaa5eb7... size 9398198
```

The manifest SHA-256 values match the **LFS object IDs**, not the pointer file hashes — consistent with an LFS-managed release that was copied without `git lfs pull`.

### Minor data quality issues (verified)

- **3 keypoint CSV filenames contain trailing spaces** before `.csv`:
  - `nagashima/snatch_-86kg_nagashima_wakana_i1_ok_000182 .csv`
  - `nakajima/snatch_-86kg_nakajima_motoka_i1_fail_000183 .csv`
  - `nakajima/snatch_-86kg_nakajima_motoka_i2_fail_000184 .csv`
- `data/processed/meta.csv` size is **1,756,579 bytes** vs manifest expectation **1,777,829 bytes**, despite matching row count (21,249). Cause unresolved.

---

## 6. Inconsistencies between thesis and code

| Topic | Thesis | Code/repo | Assessment |
|-------|--------|-----------|------------|
| Directory naming | `wl_clips/...` | Project-root relative paths | Documentation drift |
| Annotation script name | `annotate_phases_final2.py` | `annotate_phases.py` | Likely renamed |
| Results directory | `wl_clips/outputs/lstm_phases/` | `outputs/lstm_phases/` | Documentation drift |
| Abstract/resumen | Placeholder text ("Insertar aquí...") | N/A | Thesis PDF appears incomplete in front matter |
| Overlapping windows | Mentions athlete split prevents leakage | No analysis of stride-1 overlap bias within splits | **Methodological gap** |
| Evaluation type | Window-level metrics | Window-level only | Confirmed; not full temporal segmentation benchmark |
| Video source/licensing | "Olympic video search and download" | No license file, no source URLs in repo | **Legal gap** |

---

## 7. Data availability

| Asset | Included? | Redistribution risk |
|-------|-----------|---------------------|
| Raw competition videos | **No** | Unknown — likely **high** (broadcast/organizer rights) |
| Athlete names in filenames | **Yes** (in paths/filenames) | **Medium** — public athletes, but needs review for publication |
| Extracted keypoints | **Yes** | Lower than video, but derived from copyrighted footage |
| Phase annotations | **Yes** | Publishable only with video/keypoint rights clarified |
| Processed tensors | **Stub only locally** | Depends on upstream rights |
| Trained checkpoint | **Stub only locally** | Same as above |

---

## 8. Model availability

| Artifact | Available locally? | Notes |
|----------|-------------------|-------|
| `best_model.pt` | **No (LFS stub)** | Required for exact metric reproduction |
| Architecture/code | **Yes** | `train_lstm_phases.py`, `evaluate_checkpoint.py` |
| Training history | **Yes** | Best val macro-F1 at epoch 5 (inferred from `history.csv`) |
| Test predictions | **Yes** | Enables offline audit of reported confusion structure |

---

## 9. Environment status

| Check | Result |
|-------|--------|
| System Python | 3.12.3 |
| Recommended Python | 3.12 |
| Dependencies installed | **No** (`numpy` import failed) |
| CUDA availability | **Not tested** (PyTorch not installed) |
| OS assumed by README | Windows + PowerShell |
| Audit OS | Linux |
| Portability of paths in code | **Good** — uses `Path(__file__).resolve().parent.parent` |
| Hard-coded absolute local paths | **None found** |

---

## 10. Methodological risks (for benchmark redesign)

### A. Overlapping-window bias — status: partially assessed, not resolved

**Verified facts:**
- Window size = 31, stride = 1 (`build_phase_dataset.py`).
- Consecutive windows share 30/31 frames (~97% overlap).
- Split is **by athlete**, not by window (`athlete_split.json`, `train_lstm_phases.py`).
- No athlete appears in more than one split (verified from split JSON).
- Evaluation metrics in `evaluate_checkpoint.py` are computed on **individual windows**, not deduplicated frames or segments.

**Reasonable inferences:**
- This is **not classic train/test leakage across splits** at the athlete level.
- Metrics are still **strongly autocorrelated** within each split because neighboring windows overlap almost completely.
- Reported test accuracy/F1 likely **overstate effective independent-sample performance** relative to frame-level or segment-level evaluation.
- The thesis discusses athlete-level leakage but **does not discuss within-split overlap inflation**.

**Unresolved questions:**
- Whether any frame appears in multiple test windows from different videos of the same athlete (yes, across videos; overlap only within each video).
- How much metrics would drop under frame-level majority vote or one-sample-per-frame evaluation.

### B. Window classification vs temporal segmentation

The pipeline converts segmentation into **center-frame-labeled sequence classification**. There is no:
- segmental F1 / edit score,
- boundary detection evaluation,
- post-processing (smoothing, Viterbi, etc.).

This is appropriate as a baseline but **not sufficient** for a segmentation benchmark paper.

### C. Class imbalance

Verified from thesis tables and consistent with saved report supports (e.g., `recovery` dominates test set).

### D. Single split vs cross-validation

Only one fixed athlete split is provided. No k-fold or repeated splits.

---

## 11. Legal and redistribution concerns

| Concern | Status |
|---------|--------|
| License for repository code | **Not specified** in student repo |
| License for dataset/video-derived assets | **Not specified** |
| Raw video redistribution | **Not included**; thesis mentions Olympic footage acquisition |
| Athlete identifying information | Present in filenames and folder names |
| MediaPipe model file | Google MediaPipe license applies if redistributed |
| Recommended action | **Do not choose a public license or publish data** until student/supervisor confirms rights |

The new project `LICENSE` file intentionally contains a **TODO** pending legal review.

---

## 12. Recommended next steps

### Immediate (before any new modeling)

1. Obtain real LFS objects or direct binary delivery for `X.npy`, `y.npy`, `best_model.pt`.
2. Create Python 3.12 virtual environment and install `requirements.txt`.
3. Run `verify_project.py --evaluate` on a machine with complete artifacts.
4. Run `build_phase_dataset.py` and compare rebuilt tensors to baseline.
5. Document video source, license, and annotator protocol (see `QUESTIONS_FOR_STUDENT.md`).

### Short-term (SnatchPhaseBench artifact)

1. Port split logic and dataset builder into the new package with tests.
2. Implement segment-level metrics alongside window-level reporting.
3. Add overlap-aware evaluation (frame voting, stride ablation).
4. Treat original LSTM as baseline #1, not as the contribution.

---

## 13. Audit status legend

Throughout this document:

- **Verified fact** — directly observed in files or command output during audit.
- **Reasonable inference** — logically follows from verified facts; not independently executed.
- **Unresolved question** — requires student input or future experiments.

**Reproduction status as of this audit:** **NOT VERIFIED**. Saved metrics exist, but no successful execution was performed in the SnatchPhaseBench environment.
