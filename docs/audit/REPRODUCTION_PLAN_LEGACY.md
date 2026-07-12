# SnatchPhaseBench — Reproduction Plan

**Goal:** Reproduce the original TFM LSTM experiment **before** implementing new benchmark models.  
**Scope:** Exact checkpoint evaluation first; dataset rebuild second; optional retraining third.  
**Status:** Plan only — **no step below has been confirmed successful in the SnatchPhaseBench environment**.

---

## 0. Prerequisites and assumptions

### Verified preconditions in the student repository

- Scripts exist for verification, rebuild, training, and evaluation.
- 208 keypoint CSVs and full annotation masters are present as real files.
- Saved test metrics and predictions exist under `outputs/lstm_phases/`.
- Athlete split is fixed in `outputs/lstm_phases/athlete_split.json`.

### Known blockers on the audit machine

| Blocker | Required resolution |
|---------|---------------------|
| `X.npy`, `y.npy`, `best_model.pt` are Git LFS stubs | `git lfs pull` from original remote **or** student-provided binaries |
| Python deps not installed | Create venv and install requirements |
| `data/rebuilt/` absent | Will be created by rebuild script |
| Raw videos absent | **Not required** for keypoint-based reproduction |

---

## 1. Environment creation

### 1.1 Recommended: isolated Python 3.12 environment (Linux)

```bash
cd /home/cesar/papers/Paper_TFM-main

python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 1.2 Verify core imports

```bash
python -c "import numpy, pandas, torch, sklearn, mediapipe; print('numpy', numpy.__version__); print('torch', torch.__version__)"
```

**Expected:** No import errors.  
**Actual on audit machine:** Failed (`ModuleNotFoundError: numpy`).

### 1.3 Optional GPU check

```bash
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

Training/evaluation should work on CPU; README states metrics must match regardless of device for checkpoint evaluation.

---

## 2. Resolve Git LFS artifacts (critical)

If the student repository is available as a git remote with LFS:

```bash
cd /path/to/Paper_TFM-main
git lfs install
git lfs pull
```

### Files that must become real binaries

| File | Expected size (bytes) | Expected SHA-256 (from manifest) |
|------|----------------------:|-----------------------------------|
| `data/processed/X.npy` | 260,852,852 | `8497a69a2c6d80f24c0fc6242500aa931ab2c00e8172b534a98f86d92ed698b4` |
| `data/processed/y.npy` | 170,120 | `0175c1c314fd22fef37d4b16a96b038d4643765c323c8b13599ff9a9a17c3546` |
| `outputs/lstm_phases/best_model.pt` | 478,137 | `ea5ff9ca8a6dd163ad88efe06e1e221ae1b06393538c365b6c185faa7ef6b7fb` |
| `models/pose_landmarker_full.task` | 9,398,198 | `4eaa5eb7a98365221087693fcc286334cf0858e2eb6e15b506aa4a7ecdcec4ad` |

**Quick sanity check:**

```bash
file data/processed/X.npy
# Must NOT say "ASCII text" / must NOT contain "git-lfs"
```

**If LFS pull is impossible:** proceed to Section 3 (rebuild tensors) and Section 6 (retrain). Exact checkpoint reproduction will **not** be achievable until weights are obtained.

---

## 3. Data verification (no training)

### 3.1 Static baseline verification

```bash
cd /home/cesar/papers/Paper_TFM-main
python scripts/verify_project.py
```

Add `--evaluate` only after LFS binaries are available.

**Expected static outputs:**

```
Raw videos included: 0
Keypoint CSV files: 208
Dataset: (21249, 31, 99), 21249 samples, 70 athletes
Split: 49 train / 10 validation / 11 test athletes
Static verification: PASS
```

### 3.2 Annotation/keypoint alignment

```bash
python scripts/check_dataset_mismatches.py
```

**Expected:** `Dataset alignment: PASS`  
**Note:** Raw-video checks are skipped when videos are absent (by design).

### 3.3 Manual counts (optional cross-check)

| Quantity | Expected |
|----------|----------|
| Keypoint CSV files | 208 |
| Athlete folders under `data/keypoints/` | 70 |
| Rows in `data/processed/meta.csv` | 21,249 (+ header) |
| Rows in `master_frame_labels.csv` | 37,125 (+ header) |
| Test windows | 3,877 |

---

## 4. Split verification

### 4.1 Inspect fixed split

File: `outputs/lstm_phases/athlete_split.json`

**Verified composition:**

- Train: 49 athletes
- Validation: 10 athletes
- Test: 11 athletes
- Total: 70 athletes, mutually disjoint

### 4.2 Confirm no athlete overlap (automated)

`verify_project.py` already checks set disjointness and coverage.

### 4.3 Overlap audit (manual / future SnatchPhaseBench test)

Not implemented in student repo. Planned checks for SnatchPhaseBench:

- [ ] No `(video_relpath, center_frame)` duplicated across splits
- [ ] Quantify window overlap rate within each video (stride 1, window 31)
- [ ] Compare window-level vs frame-voted metrics (future)

---

## 5. Preprocessing / dataset rebuild

### 5.1 Rebuild processed tensors from canonical inputs

```bash
python scripts/build_phase_dataset.py
```

**Default behavior (verified in code):**

- Input labels: `data/annotations/master_frame_labels.csv`
- Input keypoints: `data/keypoints/`
- Output: `data/rebuilt/{X.npy,y.npy,meta.csv,label_map.csv}`
- Window size: 31, stride: 1
- Features: x, y, z for 33 landmarks → 99 dims/frame
- Drops windows whose center label is `unlabeled` (phase_id 0)

**Expected console summary:**

```
Videos: 208
X shape: (21249, 31, 99)
y shape: (21249,)
Output: .../data/rebuilt
```

### 5.2 Compare rebuild to frozen baseline

Requires real baseline tensors in `data/processed/`.

```bash
python scripts/compare_rebuild_to_baseline.py
```

**Expected:**

```
X.npy: MATCH - exact match (21249, 31, 99) float32
y.npy: MATCH - exact match (21249,) int64
meta.csv: MATCH
label_map.csv: MATCH
All rebuilt artifacts exactly match the frozen TFM baseline.
```

**If baseline tensors unavailable:** compare rebuilt `meta.csv` row count and label distribution against committed `data/processed/meta.csv` instead (weaker check).

---

## 6. Model training (optional validation path)

Use only after successful rebuild.

```bash
python scripts/train_lstm_phases.py \
  --data-dir data/rebuilt \
  --output-dir outputs/experiments/lstm_from_scratch \
  --device auto
```

**Important:** Retraining initializes new weights. README documents that metrics may differ slightly from the thesis checkpoint even with the same split/seed.

**Documented approximate retrain result (from README, not re-verified here):**

- Test accuracy ≈ 0.9435
- Test macro-F1 ≈ 0.9072

---

## 7. Evaluation — exact reproduction target

### 7.1 Checkpoint evaluation (primary success criterion)

Requires real `best_model.pt` and `data/processed/X.npy`.

```bash
python scripts/evaluate_checkpoint.py --device cpu --batch-size 4096 --write-results
```

Or via verifier:

```bash
python scripts/verify_project.py --evaluate
```

### 7.2 Expected outputs

**Console:**

```
Device: cpu
Test samples: 3877
Accuracy: 0.9517668300
Macro-F1: 0.9186193965
Matches saved report: YES
Checkpoint evaluation: PASS
```

**Files referenced:**

- `outputs/lstm_phases/classification_report.json`
- `outputs/lstm_phases/confusion_matrix.csv`
- `outputs/lstm_phases/test_predictions.csv`
- `outputs/verification/reproduced_evaluation.json` (if `--write-results`)

### 7.3 Per-class F1 (from saved report — not re-run)

| Phase | F1 (saved) | Support |
|-------|------------|--------:|
| setup | 0.9787 | 820 |
| first_pull | 0.9199 | 397 |
| transition | 0.8220 | 117 |
| second_pull | 0.9231 | 204 |
| turnover | 0.9236 | 302 |
| catch | 0.8819 | 376 |
| recovery | 0.9810 | 1661 |

---

## 8. End-to-end orchestration

### Windows (student README)

```powershell
.\run_reproduction.ps1
# Optional retrain:
.\run_reproduction.ps1 -Train
```

### Linux equivalent (manual sequence)

```bash
source .venv/bin/activate
python scripts/verify_project.py --evaluate
python scripts/build_phase_dataset.py
python scripts/compare_rebuild_to_baseline.py
```

---

## 9. Criteria for declaring reproduction successful

### Tier A — Exact reproduction (required for baseline claim)

- [ ] Real LFS binaries present and pass manifest hash checks
- [ ] `verify_project.py --evaluate` exits with `Checkpoint evaluation: PASS`
- [ ] Rebuilt dataset matches frozen baseline byte-for-byte
- [ ] Reproduced metrics match saved report within `atol=1e-12`

### Tier B — Functional reproduction (if checkpoint unavailable)

- [ ] Rebuild produces shape `(21249, 31, 99)` and 21,249 labels
- [ ] Retrained LSTM reaches test macro-F1 **≥ 0.90** (threshold provisional)
- [ ] Qualitative confusion matrix similar to saved matrix
- [ ] Document deviation from thesis metrics explicitly

### Tier C — Not sufficient alone

- Reading saved JSON metrics without re-execution
- Training on partial/corrupted tensors
- Evaluating on random or video-level splits

---

## 10. Likely blockers and mitigations

| Blocker | Mitigation |
|---------|------------|
| Git LFS stubs | Obtain full git clone with LFS, or binary bundle from student |
| Filename trailing spaces in 3 keypoint CSVs | Normalize names **in SnatchPhaseBench copy only**, not student repo |
| `meta.csv` size mismatch vs manifest | Investigate during rebuild; compare rebuilt meta to committed meta |
| Windows-centric docs | Add Linux wrapper script in SnatchPhaseBench artifact |
| PyTorch/CUDA version drift on retrain | Pin exact versions from `requirements-original.txt`; accept small metric drift |
| No segment-level metrics | Implement in SnatchPhaseBench after Tier A/B |

---

## 11. First command to run (recommended)

After obtaining real binaries and creating the venv:

```bash
cd /home/cesar/papers/Paper_TFM-main && source .venv/bin/activate && python scripts/verify_project.py --evaluate
```

If binaries are still missing, run instead:

```bash
cd /home/cesar/papers/Paper_TFM-main && source .venv/bin/activate && python scripts/build_phase_dataset.py
```

This establishes whether the **rebuild path** works even when the frozen checkpoint path is blocked.

---

## 12. What this plan deliberately does not do yet

- Implement new benchmark models (GRU, TCN, MS-TCN, ST-GCN, Transformer)
- Publish or copy raw videos into SnatchPhaseBench
- Modify the student repository
- Claim reproduced results without executed checks
