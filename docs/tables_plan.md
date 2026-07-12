# Tables Plan

| ID | Table | Content | Status |
|----|-------|---------|--------|
| T1 | Dataset statistics | Videos, athletes, frames, windows, features | **Draft ready** — see `docs/dataset/dataset.md` |
| T2 | Split statistics | Athletes, videos, windows per split | **Verified** — split validation report |
| T3 | Class distribution | Frames and windows per phase | **Verified** — rebuild audit |
| T4 | Baseline LSTM config | Hyperparameters | **Verified** — `configs/baseline_lstm.yaml` |
| T5 | Baseline results | Accuracy, macro/weighted F1, per-class F1 | **Partial** — thesis JSON; exact repro pending checkpoint |
| T6 | Reproduction comparison | Thesis vs rebuilt vs retrain | **Available** — `metrics_comparison.json` |
| T7 | Benchmark comparison | Multiple models × metrics | **Future** |
| T8 | Segment metrics | Edit score, F1@10/25/50 | **Future** |
| T9 | Ablation studies | Coordinates, window, stride | **Future** |
| T10 | Runtime comparison | Train/infer time, parameters | **Future** |
| T11 | Autocorrelation summary | Overlap %, independent sample ratio | **Available** — temporal_autocorrelation.md |

## Rules

- Do not report T5 as final until checkpoint validation passes.
- T6 distinguishes **exact**, **approximate**, and **not run**.
- Per-class tables should include support counts.
