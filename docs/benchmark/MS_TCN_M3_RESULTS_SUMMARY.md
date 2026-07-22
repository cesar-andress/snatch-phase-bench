# MS-TCN M3 benchmark results (summary)

**Status:** Canonical RTX 4090 CUDA campaign **complete**  
**Protocol commit:** `6b1d7f0003782ba313e1d0a4e492183bbb209123`  
**Hardware:** NVIDIA GeForce RTX 4090, driver 595.71.05, PyTorch 2.10.0+cu128, FP32, batch size 1  
**Machine-readable:** `outputs/benchmark/ms_tcn/aggregate/test_metrics_aggregate.json`

The 2026-07-14 CPU pilot is archived under `outputs/benchmark/ms_tcn_cpu_pilot_20260714/` and is **not** the primary result.

## Protocol

| Item | Value |
|------|-------|
| Seeds | 42, 123, 456 |
| Checkpoint monitor | `val_segmental_f1_at_50` |
| Hardware | NVIDIA GeForce RTX 4090 (CUDA) |
| Parameters | 670,688 |
| Peak allocated VRAM | 15.51 MiB |
| Test videos | 33 (11 athletes) |

## Test metrics (mean ± std over seeds)

| Metric | Mean | Std | Min | Max |
|--------|------|-----|-----|-----|
| Frame macro-F1 | 0.9048 | 0.0092 | 0.8921 | 0.9131 |
| Segment F1@50 | 0.7747 | 0.0177 | 0.7523 | 0.7955 |
| Segment F1@25 | 0.8715 | — | 0.8347 | 0.8935 |
| Segment F1@10 | 0.9024 | — | 0.8506 | 0.9383 |
| Edit score | 0.8505 | 0.0644 | 0.7615 | 0.9118 |
| Boundary MAE (frames) | 1.322 | 0.301 | 1.089 | 1.746 |
| Boundary F1 | 0.9474 | 0.0086 | 0.9364 | 0.9574 |

## Per-seed training (GPU)

| Seed | Runtime (s) | Best epoch | Val F1@50 (best) | Test F1@50 |
|------|-------------|------------|------------------|------------|
| 42 | 27.7 | 3 | 0.7347 | 0.7763 |
| 123 | 39.4 | 10 | 0.7313 | 0.7955 |
| 456 | 50.4 | 15 | 0.7271 | 0.7523 |

## Per-class recall (mean over seeds)

| Phase | Recall |
|-------|--------|
| setup (1) | 0.989 |
| first_pull (2) | 0.890 |
| transition (3) | 0.889 |
| second_pull (4) | 0.905 |
| turnover (5) | 0.898 |
| catch (6) | 0.925 |
| recovery (7) | 0.938 |

Lowest: **transition** (3), **first_pull** (2).

## Boundary MAE by transition (mean frames, 3 seeds)

| Transition | MAE (frames) |
|------------|--------------|
| first_pull → transition | 0.63 |
| transition → second_pull | 0.62 |
| second_pull → turnover | 0.65 |
| turnover → catch | 1.28 |
| setup → first_pull | 1.30 |
| catch → recovery | 4.52 |

Highest error: **catch → recovery**.

## Failure analysis (first pass)

- All 33 test videos show prediction differences across seeds (segment signatures differ).
- Over-segmentation proxy: 0–1 videos per seed.
- Missing short-phase proxy: 3–27 videos per seed (requires qualitative review).
- Seed 42 stopped early at best epoch 3; test F1@50 remained within the observed seed spread.

## LSTM comparability

Frozen LSTM (B1): window accuracy **0.9518**, macro-F1 **0.9186** — **not comparable** to dense MS-TCN segment/boundary metrics without a shared frame-level evaluation path.

## Verdict

**MS-TCN is accepted as the first learned benchmark baseline (B2) of SnatchPhaseBench.**

Evidence: three-seed RTX 4090 campaign completed under the frozen M3 protocol; test segment F1@50 is stable ($0.775 \pm 0.018$); no OOM; peak VRAM ~16 MiB; canonical JSON/CSV/figures regenerated from experiment outputs. Hyperparameters were not tuned after viewing test results.
