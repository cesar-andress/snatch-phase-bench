# Frozen Baseline Policy

The thesis LSTM baseline is **frozen and verified** (2026-07-13).

**Specification:** [`benchmark/BASELINE_SPECIFICATION.md`](benchmark/BASELINE_SPECIFICATION.md)  
**Validation:** [`reproduction/CHECKPOINT_VALIDATION.md`](reproduction/CHECKPOINT_VALIDATION.md)

## Do not modify

- `src/snatch_phase_bench/data/dataset_builder.py`
- `src/snatch_phase_bench/training/lstm_trainer.py`
- `src/snatch_phase_bench/evaluation/checkpoint_eval.py`
- `scripts/run_phase2_reproduction.py` (behavior)
- `configs/baseline_lstm.yaml` (parameter values)
- Scientific conclusions in [`reproduction/REPRODUCTION_SUMMARY.md`](reproduction/REPRODUCTION_SUMMARY.md) regarding verified checkpoint metrics

## Allowed

- Infrastructure wrappers (model adapters, evaluation extensions)
- Documentation and tests
- New models registered separately from `lstm_baseline`

## Validation gate — PASSED

Checkpoint evaluation on canonical copy `outputs/baseline/best_model.pt`:

- Test accuracy `0.9517668300232138` — **EXACT**
- Macro-F1 `0.9186193964811207` — **EXACT**
- `Matches saved report: YES`

Benchmark model development (B0–B3) may proceed per [`benchmark/BENCHMARK_PLAN.md`](benchmark/BENCHMARK_PLAN.md). The frozen LSTM remains a historical reproduction artifact, not a substitute for B0/B1 TAS tiers.
