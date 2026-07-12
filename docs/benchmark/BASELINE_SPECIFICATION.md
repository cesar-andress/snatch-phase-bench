# Baseline specification — Thesis LSTM (frozen reproduction reference)

**Designation:** Official frozen baseline for SnatchPhaseBench historical reproduction  
**Registry name:** `lstm_baseline`  
**Status:** **VERIFIED** (2026-07-13)  
**Version:** B1-repro-v1

> **Naming note:** In [`BENCHMARK_PLAN.md`](BENCHMARK_PLAN.md), tier **B1** denotes MS-TCN on raw keypoints (planned). This document defines the **thesis LSTM reproduction baseline**—the first frozen model artifact validated against prior work. Report it separately from benchmark tiers B0–B3.

---

## 1. Purpose

This checkpoint is the immutable reference for:

- Independent verification of MSc thesis window-level metrics
- Baseline row “LSTM (thesis repro)” in manuscript tables
- Regression tests for the frozen evaluation pipeline

It is **not** the literature-recommended primary benchmark competitor (that role belongs to **B0** rule-based knee-angle segmentation once implemented).

---

## 2. Dataset version

| Field | Value |
|-------|-------|
| Source snapshot | `~/papers/Paper_TFM-main` (read-only) |
| Rebuilt tensors | `data/processed/rebuilt/` |
| `X.npy` SHA-256 | `8497a69a2c6d80f24c0fc6242500aa931ab2c00e8172b534a98f86d92ed698b4` |
| `y.npy` SHA-256 | `0175c1c314fd22fef37d4b16a96b038d4643765c323c8b13599ff9a9b17c3546` |
| Windows | 21,249 total; 3,877 test |
| Window size / stride | 31 / 1 |
| Features | 99-D (33 landmarks × 3 coords, z-scored per training stats in checkpoint) |
| Athletes | 70 (split 49 / 10 / 11 train / val / test) |
| Split file | `athlete_split.json` (student snapshot; athlete-disjoint) |

---

## 3. Checkpoint artifact

| Field | Value |
|-------|-------|
| File | `outputs/baseline/best_model.pt` |
| Size | 478,137 bytes |
| SHA-256 | `ea5ff9ca8a6dd163ad88efe06e1e221ae1b06393538c365b6c185faa7ef6b7fb` |
| Sidecar | `outputs/baseline/best_model.pt.sha256` |
| Git | Ignored (local / Zenodo); checksum tracked in docs |
| Provenance | [`../reproduction/CHECKPOINT_PROVENANCE.md`](../reproduction/CHECKPOINT_PROVENANCE.md) |

**Policy:** Never modify the read-only snapshot original. Updates require a new baseline version ID and full re-validation.

---

## 4. Model configuration

From `configs/baseline_lstm.yaml` and checkpoint metadata:

| Hyperparameter | Value |
|----------------|-------|
| Architecture | Single-layer LSTM + linear head |
| `hidden_size` | 128 |
| `num_layers` | 1 |
| `dropout` | 0.2 |
| Classes | 7 phases |
| Loss | Cross-entropy with class weights |
| Optimizer | Adam (`lr=1e-3`, `weight_decay=1e-4`) |
| Training budget | 40 epochs max, patience 8 (validation macro-F1) |
| Seed | 42 |

Implementation frozen in:

- `src/snatch_phase_bench/training/lstm_trainer.py`
- `src/snatch_phase_bench/evaluation/checkpoint_eval.py`

---

## 5. Evaluation protocol

| Step | Specification |
|------|---------------|
| Input | Rebuilt `X.npy`, `y.npy`, `meta.csv` |
| Split filter | Test athletes from `athlete_split.json` |
| Normalization | Training `mean` / `std` stored in checkpoint |
| Metrics | `sklearn.metrics.classification_report` (macro + weighted) |
| Entry point | `python -m snatch_phase_bench.evaluation.checkpoint_eval` or `scripts/run_phase2_reproduction.py` (eval-only mode) |
| Expected accuracy | 0.9517668300232138 |
| Expected macro-F1 | 0.9186193964811207 |
| Gate | `matches_saved_report == true` |

Full metric table: [`../reproduction/CHECKPOINT_VALIDATION.md`](../reproduction/CHECKPOINT_VALIDATION.md)

---

## 6. Hardware independence

Validation run: **CPU only** (PyTorch 2.10.0, Linux x86_64).

Inference is deterministic on CPU for this checkpoint; GPU is not required for evaluation. Retraining may show hardware-dependent drift (~0.8 pp accuracy on CPU retrain); **checkpoint evaluation is the authoritative metric**.

---

## 7. Reproducibility status

| Criterion | Status |
|-----------|--------|
| Dataset rebuild exact | **VERIFIED** |
| Split integrity | **VERIFIED** |
| Checkpoint metrics vs thesis | **VERIFIED (EXACT)** |
| Confusion matrix export | Pending figure generation |
| Public Zenodo bundle | Pending legal release |

**Overall:** Thesis LSTM baseline is **officially frozen** for SnatchPhaseBench reproduction.

---

## 8. Known limitations

1. **Window-level protocol** — stride-1 overlap inflates apparent independence; segment-level metrics remain primary for benchmark comparison.
2. **Seven-phase ontology** — thesis labels; literature and some coaching frameworks use five phases (reconciliation pending).
3. **Single split** — one 49/10/11 partition; cross-validation not yet run.
4. **Monocular MediaPipe inputs** — no multi-view or MOCAP ground truth.
5. **Class imbalance** — transition and second_pull are minority classes.
6. **Retrain ≠ checkpoint** — CPU retrain approximates but does not replace frozen weights.

---

## 9. Future compatibility policy

| Change type | Action |
|-------------|--------|
| Bug fix in evaluator (no metric change) | Patch + regression test against this checksum |
| Preprocessing / dataset rebuild change | New dataset version; **re-validate** checkpoint; bump baseline version |
| New checkpoint / retrain | New SHA-256; do not overwrite B1-repro-v1 |
| Benchmark models (B0–B3) | Separate registry entries; must use same split and data version |

Modifications to frozen files listed in [`../FROZEN_BASELINE.md`](../FROZEN_BASELINE.md) require explicit project approval after this validation.

---

## 10. References

- Validation: [`../reproduction/CHECKPOINT_VALIDATION.md`](../reproduction/CHECKPOINT_VALIDATION.md)
- Provenance: [`../reproduction/CHECKPOINT_PROVENANCE.md`](../reproduction/CHECKPOINT_PROVENANCE.md)
- Reproduction summary: [`../reproduction/REPRODUCTION_SUMMARY.md`](../reproduction/REPRODUCTION_SUMMARY.md)
- Benchmark tiers (separate): [`BENCHMARK_PLAN.md`](BENCHMARK_PLAN.md)
