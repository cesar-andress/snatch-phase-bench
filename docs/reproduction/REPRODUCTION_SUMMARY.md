# Reproduction Summary — Phase 2

**Generated:** 2026-07-13 (UTC)  
**Canonical repository:** `~/papers/snatch-phase-bench/snatch-phase-bench`  
**Read-only snapshot:** `~/papers/Paper_TFM-main` (unmodified)

---

## 1. Reproduction status overview

| Component | Status |
|-----------|--------|
| Dataset rebuild from keypoints + annotations | **Exact match to manifest SHA-256** |
| `meta.csv` vs baseline snapshot | **Byte-identical** |
| Athlete-level split validation | **PASS** |
| Original checkpoint evaluation | **VERIFIED** (all metrics EXACT) |
| LSTM retraining (original hyperparameters) | **Approximate reproduction** (reference only) |

**Overall:** **Full reproduction** of thesis window-level metrics via frozen checkpoint. Retrain path remains approximate.

See [`CHECKPOINT_VALIDATION.md`](CHECKPOINT_VALIDATION.md) and [`CHECKPOINT_PROVENANCE.md`](CHECKPOINT_PROVENANCE.md).

---

## 2. What was reproduced exactly

1. **Processed dataset tensors** rebuilt to shape `(21249, 31, 99)` with `float32` / `int64` dtypes.
2. **SHA-256 checksums** of rebuilt artifacts match `baseline_tfm/manifest.json`:

   | File | SHA-256 | Manifest match |
   |------|---------|----------------|
   | `X.npy` | `8497a69a2c6d80f24c0fc6242500aa931ab2c00e8172b534a98f86d92ed698b4` | **Yes** |
   | `y.npy` | `0175c1c314fd22fef37d4b16a96b038d4643765c323c8b13599ff9a9b17c3546` | **Yes** |
   | `meta.csv` | `6b1fc02b4062be11781f675bf1c79cc5272198882cfe48b6784b35dbe1089278` | **Yes** (baseline file; size differs from manifest byte count — see audit) |

3. **Split integrity:** 49/10/11 athletes; 14,140 / 3,232 / 3,877 windows; no athlete or video overlap across splits.
4. **Test sample count:** 3,877 (matches thesis).

---

## 3. What was reproduced approximately

**LSTM retraining** on rebuilt data (CPU, seed 42, original hyperparameters):

| Metric | Thesis | Reproduced | Δ |
|--------|--------|------------|---|
| Accuracy | 0.9518 | 0.9440 | −0.0077 |
| Macro precision | 0.9132 | 0.8997 | −0.0135 |
| Macro recall | 0.9250 | 0.9015 | −0.0235 |
| Macro F1 | 0.9186 | 0.8992 | −0.0194 |
| Weighted F1 | 0.9524 | 0.9445 | −0.0079 |
| Test samples | 3877 | 3877 | 0 |

Per-class F1 deltas largest for `transition` (−0.057) and `second_pull` (−0.046). See `docs/reproduction/reports/metrics_comparison.json`.

This is **retraining reproduction**, not checkpoint evaluation. README of the student repo documents similar CPU retrain drift (~0.9435 accuracy).

---

## 4. Checkpoint evaluation (verified)

Recovered binary: `Paper_TFM-main/best_model.pt` (478,137 B; SHA-256 `ea5ff9ca…b7fb`).  
Canonical copy: `outputs/baseline/best_model.pt`.

| Metric | Thesis | Checkpoint eval | Δ | Status |
|--------|--------|-----------------|---|--------|
| Accuracy | 0.9518 | 0.9518 | 0 | EXACT |
| Macro precision | 0.9132 | 0.9132 | 0 | EXACT |
| Macro recall | 0.9250 | 0.9250 | 0 | EXACT |
| Macro F1 | 0.9186 | 0.9186 | 0 | EXACT |
| Weighted F1 | 0.9524 | 0.9524 | 0 | EXACT |
| Test samples | 3877 | 3877 | 0 | EXACT |

`matches_saved_report: true`. Full tables: [`CHECKPOINT_VALIDATION.md`](CHECKPOINT_VALIDATION.md).

---

## 5. What could not be reproduced (unchanged)

1. **Byte comparison to snapshot `X.npy`/`y.npy`** — LFS pointers in export; manifest hash comparison used instead (rebuild matches manifest).
2. **MediaPipe pose re-extraction** — `pose_landmarker_full.task` is an LFS pointer; not required for keypoint-based path.

---

## 6. Remaining blockers

See [`REMAINING_BLOCKERS.md`](REMAINING_BLOCKERS.md). Checkpoint validation is **not** a blocker.

---

## 7. Confidence in the baseline

| Aspect | Confidence |
|--------|------------|
| Dataset construction pipeline | **High** — manifest hash match |
| Split protocol | **High** — automated validation PASS |
| Reported thesis metrics (checkpoint eval) | **High** — EXACT match on rebuilt data |
| Retrained LSTM as proxy for checkpoint | **Medium-low** — use checkpoint only for official numbers |

---

## 8. Ready for benchmark development?

**Yes** — checkpoint validation gate passed (2026-07-13).

Benchmark tier implementation (B0–B3) may proceed per [`../benchmark/BENCHMARK_PLAN.md`](../benchmark/BENCHMARK_PLAN.md). Do not overwrite the frozen thesis checkpoint or conflate retrain metrics with official baseline numbers.

---

## 9. Environment

See `docs/reproduction/reports/environment.json`:

- Python 3.12.3, Linux x86_64
- CPU only (CUDA unavailable)
- numpy 2.4.3, pandas 3.0.1, torch 2.10.0+cu128, scikit-learn 1.8.0

---

## 10. Commands executed

```bash
cd ~/papers/snatch-phase-bench/snatch-phase-bench
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements-reproduction.txt && pip install -e .
pytest tests/
python scripts/run_phase2_reproduction.py
```

Dataset rebuild runtime: **~7.9 s**. LSTM retraining runtime: **~40 s** (CPU, early stopping).

---

## 11. Related reports

- `docs/reproduction/CHECKPOINT_PROVENANCE.md`
- `docs/reproduction/CHECKPOINT_VALIDATION.md`
- `docs/benchmark/BASELINE_SPECIFICATION.md`
- `docs/reproduction/REMAINING_BLOCKERS.md`
- `docs/reproduction/code_provenance.md`
- `docs/reproduction/temporal_autocorrelation.md`
- `docs/reproduction/reports/dataset_audit.md`
- `docs/reproduction/reports/split_validation.md`
- `docs/reproduction/reports/metrics_comparison.json`
