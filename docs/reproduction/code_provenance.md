# Code Provenance — Phase 2 Baseline Reproduction

Documentation of files ported or adapted from the read-only student snapshot
(`~/papers/Paper_TFM-main`). The snapshot itself was **not modified**.

| Original source | Destination | Change | Reason |
|-----------------|-------------|--------|--------|
| `Paper_TFM-main/scripts/build_phase_dataset.py` | `src/snatch_phase_bench/data/dataset_builder.py` | Modified | Extract functions; add `build_phase_dataset()` API; configurable paths via caller |
| `Paper_TFM-main/scripts/train_lstm_phases.py` | `src/snatch_phase_bench/training/lstm_trainer.py` | Modified | Extract `train_lstm_baseline()`; remove CLI; preserve training logic |
| `Paper_TFM-main/scripts/evaluate_checkpoint.py` | `src/snatch_phase_bench/evaluation/checkpoint_eval.py` | Modified | Extract `evaluate_checkpoint()`; add LFS pointer guard |
| `Paper_TFM-main/scripts/train_lstm_phases.py` (`LSTMClassifier`) | `src/snatch_phase_bench/models/lstm_classifier.py` | Copied unchanged | Model architecture must match checkpoint |
| `Paper_TFM-main/scripts/verify_project.py` | — | Not ported | Replaced by modular tests + reproduction scripts |
| `Paper_TFM-main/baseline_tfm/manifest.json` | Read via config path only | Not copied | Referenced read-only for SHA-256 expectations |
| `Paper_TFM-main/requirements-original.txt` | `requirements-reproduction.txt` | Modified | Subset: numpy, pandas, scipy, scikit-learn, torch, PyYAML, tqdm, pytest |
| — | `src/snatch_phase_bench/config.py` | New | Load `configs/reproduction.yaml` |
| — | `src/snatch_phase_bench/reproduction/artifact_inventory.py` | New | Phase 2 artifact inspection |
| — | `src/snatch_phase_bench/reproduction/dataset_audit.py` | New | Dataset verification |
| — | `src/snatch_phase_bench/reproduction/split_validation.py` | New | Split checks |
| — | `src/snatch_phase_bench/reproduction/temporal_autocorrelation.py` | New | Overlap analysis |
| — | `scripts/run_phase2_reproduction.py` | New | Orchestration CLI |

## Data access

No files were copied from the snapshot into git-tracked directories during Phase 2 setup.
The reproduction runner reads annotations, keypoints, split JSON, and baseline meta **read-only**
via absolute paths in `configs/reproduction.yaml`.

Generated tensors and checkpoints are written to gitignored paths:

- `data/processed/rebuilt/`
- `outputs/reproduction/`

## Scientific behavior preserved

- Window size 31, stride 1, center-frame labels
- Drop `unlabeled` windows
- x/y/z for 33 landmarks (99 features)
- Keypoint interpolation + ffill/bfill
- Athlete-level split from frozen `athlete_split.json`
- LSTM: hidden 128, 1 layer, dropout 0.2, Adam, class-weighted CE, train-only standardization
- Early stopping on validation macro-F1, patience 8
