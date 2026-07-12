# Frozen Baseline Policy

The thesis LSTM baseline is **frozen** until the original `best_model.pt` checkpoint
has been received and validated.

## Do not modify

- `src/snatch_phase_bench/data/dataset_builder.py`
- `src/snatch_phase_bench/training/lstm_trainer.py`
- `src/snatch_phase_bench/evaluation/checkpoint_eval.py`
- `scripts/run_phase2_reproduction.py` (behavior)
- `configs/baseline_lstm.yaml` (parameter values)
- `docs/reproduction/REPRODUCTION_SUMMARY.md` (scientific conclusions)

## Allowed

- Infrastructure wrappers (model adapters, evaluation extensions)
- Documentation and tests
- New models registered separately from `lstm_baseline`

## Validation gate

When `best_model.pt` is available, run checkpoint evaluation and confirm:

- Test accuracy `0.9517668300`
- Macro-F1 `0.9186193965`
- `Matches saved report: YES`

Only then may benchmark model development begin.
