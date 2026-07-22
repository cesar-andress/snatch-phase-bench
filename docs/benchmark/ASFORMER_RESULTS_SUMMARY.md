# ASFormer B3 benchmark results (summary)

**Status:** Canonical RTX 4090 CUDA campaign **complete**  
**Protocol commit (pre-run):** `14483a5`  
**Hardware:** NVIDIA GeForce RTX 4090, driver 595.71.05, PyTorch 2.10.0+cu128, FP32, batch size 1  
**Machine-readable:** `docs/benchmark/results/asformer_b3/test_metrics_aggregate.json`

## Protocol

| Item | Value |
|------|-------|
| Seeds | 42, 123, 456 |
| Checkpoint monitor | `val_segmental_f1_at_50` |
| Parameters | 1,004,768 |
| Peak allocated VRAM | 99.93 MiB |
| Test videos | 33 (11 athletes) |

## Test metrics (mean ± std over seeds)

| Metric | Mean | Std | Min | Max |
|--------|------|-----|-----|-----|
| Frame macro-F1 | 0.9019 | 0.0171 | 0.8812 | 0.9230 |
| Segment F1@50 | 0.7897 | 0.0011 | 0.7882 | 0.7910 |
| Segment F1@25 | 0.8614 | — | — | — |
| Segment F1@10 | 0.9065 | — | — | — |
| Edit score | 0.8545 | 0.0475 | 0.8022 | 0.9173 |
| Boundary MAE (frames) | 0.977 | 0.058 | 0.916 | 1.055 |
| Boundary F1 | 0.9529 | 0.0073 | 0.9427 | 0.9592 |

## Per-seed training (GPU)

| Seed | Runtime (s) | Best epoch | Val F1@50 | Test F1@50 |
|------|-------------|------------|-----------|------------|
| 42 | 503.7 | 9 | 0.7427 | 0.7882 |
| 123 | 943.3 | 35 | 0.7458 | 0.7898 |
| 456 | 625.9 | 19 | 0.7432 | 0.7910 |

## Comparison with frozen MS-TCN (B2)

| Metric | ASFormer (B3) | MS-TCN (B2) | Δ |
|--------|---------------|-------------|---|
| Frame macro-F1 | 0.9019 | 0.9048 | −0.0029 |
| Segment F1@50 | 0.7897 | 0.7747 | **+0.0149** |
| Edit score | 0.8545 | 0.8505 | +0.0041 |
| Boundary MAE (f) | 0.977 | 1.322 | **−0.345** |
| Boundary F1 | 0.9529 | 0.9474 | +0.0055 |

Same dataset, split, ontology, evaluator, hardware, seeds, and early-stopping rule.

## Per-class recall (mean)

| Phase | Recall |
|-------|--------|
| setup | 0.956 |
| first_pull | 0.901 |
| transition | 0.875 |
| second_pull | 0.922 |
| turnover | 0.879 |
| catch | 0.897 |
| recovery | 0.973 |

Lowest: **transition**, **turnover**.

## Boundary MAE by transition (mean frames)

| Transition | MAE (f) |
|------------|---------|
| second_pull → turnover | 0.49 |
| transition → second_pull | 0.51 |
| first_pull → transition | 0.60 |
| turnover → catch | 1.12 |
| setup → first_pull | 1.30 |
| catch → recovery | 2.49 |

Highest error: **catch → recovery** (same primary error mode as B2, lower absolute MAE).

## Verdict

**ASFormer is accepted as Benchmark Baseline B3.**

Evidence: architecture audit + author-release port with documented deviations; full test suite passed; three-seed RTX 4090 campaign completed; canonical JSON/CSV/figures generated; segment F1@50 and boundary MAE improve over frozen B2 under identical protocol. Hyperparameters were not tuned after viewing test results.
