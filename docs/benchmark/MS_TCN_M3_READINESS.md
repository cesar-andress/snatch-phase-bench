# MS-TCN M3 experiment readiness (RTX 4090)

**Date:** 2026-07-22  
**Status:** PASSED — no blocking issues; canonical three-seed GPU campaign authorized  
**Git commit at assessment:** `96508c99e484b5f0e0a28b069b161416944b5321`  
**Machine-readable:** `outputs/benchmark/ms_tcn/aggregate/readiness_assessment.json`

## 1. Estimated GPU memory usage

| Sequence length | Peak allocated | Peak reserved |
|-----------------|----------------|---------------|
| 75 (min) | 12.9 MiB | 14.0 MiB |
| 175 (median) | 13.0 MiB | 34.0 MiB |
| 425 (max) | 19.7 MiB | 40.0 MiB |

Available VRAM: **24564 MiB**. OOM risk: **LOW** at batch size 1 / FP32.

## 2. Estimated training time per epoch

- Train forward+backward (145 videos, real lengths): **~1.3 s**
- Val inference (30 videos): **~0.07 s**
- Canonical segment eval overhead (estimated): **~5 s**
- **Per-epoch wall ≈ 6.3 s** (dominated by validation segment metrics)

## 3. Estimated total training time (one seed)

| Scenario | Estimate |
|----------|----------|
| ~25 epochs (typical early stop) | **~3.6 min** |
| 50 epochs (max) | **~6.3 min** |

## 4. Estimated total time (three seeds)

| Scenario | Estimate |
|----------|----------|
| ~25 epochs × 3 | **~11 min** |
| 50 epochs × 3 | **~19 min** |

## 5. Model parameter count

**670,688** parameters (`num_classes=8`, stages=4, layers=10, f_maps=64).

## 6. Checkpoint size

| Artifact | Size |
|----------|------|
| `best_model.pt` | ~2.62 MiB |
| `checkpoint_last.pt` | ~7.88 MiB |

## 7. Expected disk usage

| Scope | Estimate |
|-------|----------|
| Per seed | ~12 MiB |
| Three seeds + aggregate | ~40 MiB |
| Free disk at assessment | 103.3 GiB |

## 8. Risks

| Risk | Assessment |
|------|------------|
| OOM | **Low** (~20 MiB peak vs 24 GiB) |
| Sequence length | Max 425 frames (val); batch size 1 handles variable length |
| Batching | Frozen at 1; OOM policy requires full restart if changed |
| CUDA | RTX 4090 validated; torch 2.10.0+cu128; driver 595.71.05 |
| Mixing CPU/GPU runs | CPU pilot archived to `outputs/benchmark/ms_tcn_cpu_pilot_20260714/` |

## 9. Protocol freeze confirmation

**FROZEN** — do not change after viewing test results:

| Item | Value |
|------|-------|
| Seeds | 42, 123, 456 |
| LR / WD | 0.0005 / 0.0 |
| Batch size | 1 |
| Epochs / patience | 50 / 15 |
| Monitor | `val_segmental_f1_at_50` |
| Dropout / TMSE λ / τ | 0.5 / 0.15 / 4 |
| Device / precision | cuda / FP32 |
| Config | `configs/benchmark/ms_tcn.yaml` |
| Config SHA-256 | `cc3e59d349cee2e48c00dafe926ab53838ecb457b8ef17ed90d6e9a0190aaf70` |

Preflight: **PASSED** (208 videos, disjoint athlete split, no NaN/Inf).
