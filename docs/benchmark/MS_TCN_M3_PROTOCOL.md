# MS-TCN M3 experiment protocol (frozen)

**Milestone:** M3 — first real benchmark evidence on the complete SnatchPhaseBench dataset  
**Frozen:** 2026-07-14  
**Status:** Pre-declared protocol; do not change seeds or hyperparameters after viewing results.

---

## Objective

Train and evaluate the canonical MS-TCN implementation (B2) on all 208 frame-sequence videos with three fixed seeds, using validation **segment F1@IoU=0.50** for checkpoint selection.

---

## Frozen versions

| Artifact | Version / path |
|----------|----------------|
| Dataset | `ds-v1.0` (`configs/benchmark.yaml`) |
| Ontology | `seven_phase_v1` (`configs/ontology/seven_phase_v1.yaml`) |
| Split | `athlete_split_v1` (`Paper_TFM-main/outputs/lstm_phases/athlete_split.json`) |
| Evaluator | `eval-v1.1.0` |
| MS-TCN config | `configs/benchmark/ms_tcn.yaml` |
| Implementation | `src/snatch_phase_bench/models/ms_tcn/` |

---

## Early-stopping decision (pre-run)

**Primary model-selection metric:** `val_segmental_f1_at_50`

Each training epoch runs dense inference on the validation split and computes segment metrics through the **canonical evaluator** (`evaluate_frame_predictions`). The checkpoint with highest validation segment F1@0.50 is retained.

Frame macro-F1 (`macro_f1` in epoch logs) is recorded but **not** used for selection, because segment F1@50 aligns with primary benchmark endpoints and avoids window-aggregation bias.

Fallback (not used): validation macro-F1 if segment computation failed — verified operational in integration tests.

---

## Seeds (fixed)

`42`, `123`, `456`

No additional seeds after viewing test results.

---

## Training hyperparameters (frozen)

| Parameter | Value |
|-----------|-------|
| Optimizer | Adam |
| Learning rate | 0.0005 |
| Weight decay | 0.0 |
| Batch size | 1 (variable-length videos) |
| Max epochs | 50 |
| Early-stopping patience | 15 |
| TMSE λ | 0.15 |
| TMSE τ | 4 |
| Stages / layers / f_maps | 4 / 10 / 64 |
| Dropout | 0.5 |
| Class weighting | true |
| Standardization | train-only |
| AMP | false |

---

## Evaluation protocol

- **Validation:** used only for checkpoint selection during training.
- **Test:** evaluated **once** per seed after training completes, using `best_model.pt`.
- Metrics: frame macro-F1, segment F1@10/25/50, edit score, boundary MAE (frames), boundary F1.
- Millisecond boundary metrics: **not reported** (FPS metadata not verified).

---

## Output layout

```text
outputs/benchmark/ms_tcn/
  aggregate/
    preflight_report.json
    protocol_freeze.json
    test_metrics_aggregate.json
    failure_analysis.json
    figures/
  seed42/
  seed123/
  seed456/
```

Large artifacts (checkpoints, predictions, logs) remain gitignored.

---

## Runner

```bash
python scripts/run_ms_tcn_benchmark.py --config configs/benchmark/ms_tcn.yaml
```

Preflight only:

```bash
python -c "from snatch_phase_bench.benchmark.preflight import run_preflight, write_preflight_report; from pathlib import Path; r=run_preflight(); write_preflight_report(Path('outputs/benchmark/ms_tcn/aggregate/preflight_report.json'), r); print(r.passed)"
```

---

## LSTM comparison policy

Frozen LSTM (B1) window-level metrics are **not** directly comparable to dense MS-TCN segment/boundary metrics. Any side-by-side table must include an explicit comparability warning.

---

## Related documents

- `docs/benchmark/MS_TCN_DESIGN.md`
- `docs/benchmark/MS_TCN_USAGE.md`
- `docs/literature/CAO_CHEN_ALIGNMENT.md`
