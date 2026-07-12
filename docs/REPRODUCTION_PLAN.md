# Reproduction Plan (Canonical Workspace)

Reproduce the original TFM LSTM experiment **without modifying** `~/papers/Paper_TFM-main`.

**Policy:** See [`WORKSPACE_POLICY.md`](WORKSPACE_POLICY.md).

---

## 1. Environment (this repository only)

```bash
cd ~/papers/snatch-phase-bench/snatch-phase-bench
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
```

Never create `.venv` or run `pip install` inside `Paper_TFM-main`.

---

## 2. Stage read-only source data

Copy required inputs from the archived snapshot into this repo:

```bash
cd ~/papers/snatch-phase-bench/snatch-phase-bench

mkdir -p data/interim/keypoints data/interim/annotations data/processed

cp -a ~/papers/Paper_TFM-main/data/keypoints/. data/interim/keypoints/
cp ~/papers/Paper_TFM-main/data/annotations/master_frame_labels.csv data/interim/
cp ~/papers/Paper_TFM-main/data/annotations/master_segment_labels.csv data/interim/
cp ~/papers/Paper_TFM-main/outputs/lstm_phases/athlete_split.json data/processed/
```

Optional reference metadata (if needed before rebuild):

```bash
cp ~/papers/Paper_TFM-main/data/processed/meta.csv data/processed/meta_baseline_ref.csv
cp ~/papers/Paper_TFM-main/data/processed/label_map.csv data/processed/label_map_ref.csv
```

---

## 3. Obtain missing LFS binaries (outside the snapshot)

If `Paper_TFM-main` contains LFS pointer stubs, request real files from the student and copy **here**:

| File | Destination |
|------|-------------|
| `X.npy` | `data/processed/X.npy` |
| `y.npy` | `data/processed/y.npy` |
| `best_model.pt` | `outputs/baseline/best_model.pt` |
| `pose_landmarker_full.task` | `models/pose_landmarker_full.task` (if pose re-extraction is needed) |

Do **not** run `git lfs pull` inside `Paper_TFM-main`.

Expected baseline tensor shape: `(21249, 31, 99)`.

---

## 4. Rebuild dataset (canonical implementation — TODO)

Once `build_phase_dataset` is ported to `src/snatch_phase_bench/`:

```bash
# Planned CLI — not yet implemented
# snatch-phase-bench build-dataset \
#   --labels-csv data/interim/master_frame_labels.csv \
#   --keypoints-dir data/interim/keypoints \
#   --output-dir data/processed
```

Until porting is complete, you may run the student's script **read-only** by invoking it with paths pointing at copies:

```bash
python ~/papers/Paper_TFM-main/scripts/build_phase_dataset.py \
  --labels-csv data/interim/master_frame_labels.csv \
  --keypoints-dir data/interim/keypoints \
  --output-dir data/processed/rebuilt
```

This executes student code but writes **only** into this repository.

---

## 5. Exact checkpoint evaluation (success criterion)

After real `best_model.pt` and `X.npy`/`y.npy` are available under this repo:

```bash
# Planned — port evaluate_checkpoint into src/snatch_phase_bench/
```

**Target metrics (from saved student report, not yet re-verified here):**

- Test samples: 3877
- Accuracy: 0.9517668300
- Macro-F1: 0.9186193965

---

## 6. Criteria for declaring reproduction successful

### Tier A — Exact

- [ ] Real binaries present under this repo (not LFS stubs)
- [ ] Rebuilt tensors match baseline byte-for-byte OR match manifest hashes
- [ ] Checkpoint evaluation matches saved report within `1e-12`

### Tier B — Functional (if checkpoint unavailable)

- [ ] Rebuild produces `(21249, 31, 99)` from copied keypoints + labels
- [ ] Retrained LSTM reaches comparable test macro-F1 (≥ 0.90 provisional)

---

## 7. First command to run now

```bash
cd ~/papers/snatch-phase-bench/snatch-phase-bench
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/
```

Then stage keypoints and labels using the copy commands in Section 2.
