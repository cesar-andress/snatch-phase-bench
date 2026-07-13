# MS-TCN M3 benchmark results (summary)

**Status:** CPU pilot complete; **canonical GPU rerun pending (RTX 4090)**  
**Warning:** Metrics below are from a **CPU-only preliminary run** and must be superseded by CUDA runs on the reference GPU before manuscript finalization.

## Protocol

| Item | Value |
|------|-------|
| Seeds | 42, 123, 456 |
| Checkpoint monitor | `val_segmental_f1_at_50` |
| Hardware | **CPU-only (preliminary)** — canonical target: RTX 4090 + CUDA |
| Parameters | 670,688 |
| Test videos | 33 (11 athletes) |

## Test metrics (mean ± std over seeds)

| Metric | Mean | Std | Min | Max |
|--------|------|-----|-----|-----|
| Frame macro-F1 | 0.9066 | 0.0083 | 0.8953 | 0.9149 |
| Segment F1@50 | 0.7680 | 0.0114 | 0.7582 | 0.7839 |
| Segment F1@25 | 0.8754 | — | 0.8474 | 0.8897 |
| Segment F1@10 | 0.9143 | — | 0.8870 | 0.9394 |
| Edit score | 0.8756 | 0.0341 | 0.8309 | 0.9135 |
| Boundary MAE (frames) | 1.176 | 0.257 | 0.947 | 1.535 |
| Boundary F1 | 0.9463 | 0.0086 | 0.9364 | 0.9574 |

## Per-seed training

| Seed | Runtime (s) | Best epoch | Val F1@50 (best) | Test F1@50 |
|------|---------------|------------|------------------|------------|
| 42 | 310.7 | 22 | 0.7386 | 0.7839 |
| 123 | 121.0 | 2 | 0.7116 | 0.7582 |
| 456 | 228.2 | 10 | 0.7373 | 0.7617 |

## Per-class recall (mean over seeds)

| Phase | Recall |
|-------|--------|
| setup (1) | 0.986 |
| first_pull (2) | 0.880 |
| transition (3) | 0.889 |
| second_pull (4) | 0.900 |
| turnover (5) | 0.911 |
| catch (6) | 0.871 |
| recovery (7) | 0.967 |

Lowest: **catch** (6), **first_pull** (2).

## Boundary MAE by transition (mean frames, 3 seeds)

| Transition | MAE (frames) |
|------------|--------------|
| second_pull → turnover | 0.43 |
| first_pull → transition | 0.87 |
| transition → second_pull | 0.57 |
| setup → first_pull | 1.16 |
| turnover → catch | 1.39 |
| catch → recovery | 3.39 |

Highest error: **catch → recovery**.

## Failure analysis (first pass)

- All 33 test videos show prediction differences across seeds (segment signatures differ).
- Over-segmentation proxy (pred segments > GT+2): 0 videos on average per seed.
- Missing short-phase proxy: 15–23 videos per seed (requires qualitative review; may reflect collapsed segment counts vs. noisy GT fragmentation).
- Seed 123 stopped early at epoch 2 (best val F1@50); test performance remained within one std of other seeds.

## LSTM comparability

Frozen LSTM (B1): window accuracy **0.9518**, macro-F1 **0.9186** — **not comparable** to dense MS-TCN segment/boundary metrics without a shared frame-level evaluation path.

## Verdict (preliminary CPU pilot)

MS-TCN trains stably and yields consistent test metrics on CPU, but **canonical M3 acceptance requires rerunning all three seeds on the reference RTX 4090** with recorded GPU memory and inference timings per `MS_TCN_M3_PROTOCOL.md`.
