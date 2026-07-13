# MS-TCN integration infrastructure (pre-implementation)

**Status:** MS-TCN **implemented** (M2)  
**Parent:** [`BENCHMARK_PROTOCOL.md`](BENCHMARK_PROTOCOL.md)  
**Design:** [`MS_TCN_DESIGN.md`](MS_TCN_DESIGN.md) · **Usage:** [`MS_TCN_USAGE.md`](MS_TCN_USAGE.md)

This document describes the integration scaffolding so MS-TCN can be added with minimal engineering effort once architecture code is available.

---

## 1. Objective

Prepare a **frame-wise TAS pipeline** parallel to the frozen window-based LSTM (B1):

| Layer | Module | Status |
|-------|--------|--------|
| Labels | `snatch_phase_bench.data.labels` | Ready |
| Dense sequences | `snatch_phase_bench.data.frame_sequence` | Ready |
| Athlete split | `snatch_phase_bench.data.splits` | Ready |
| Model interface | `snatch_phase_bench.models.base` (`frame_sequence`) | Ready |
| Training interface | `snatch_phase_bench.training.ms_tcn_trainer` | **Implemented** |
| Evaluation hooks | `snatch_phase_bench.evaluation.tas_hooks` | Ready |
| Benchmark registry | `snatch_phase_bench.benchmark.registry` | Ready |
| Experiment config | `configs/benchmark/ms_tcn.yaml` | **Complete** |
| Model | `snatch_phase_bench.models.ms_tcn` | **Implemented** |

**No experimental results** are produced by this phase.

---

## 2. Data flow (planned)

```text
master_frame_labels.csv + keypoints/*.csv
        │
        ▼
FrameLabelStore / build_frame_sequence()
        │
        ▼
FrameSequenceRecord  (T × 99 features, T labels)
        │
        ▼
[TAS trainer — not implemented]
        │
        ▼
per-frame predictions  →  evaluate_frame_predictions()
        │
        ▼
BenchmarkEvaluationResult JSON
```

---

## 3. Adding MS-TCN (future steps)

1. Implement `MSTCNModel(TemporalSegmentationModel)` with `input_layout='frame_sequence'`.
2. Register in `models/registry.py` as `"ms_tcn"`.
3. Implement `MSTCNTrainer(TemporalSegmentationTrainer)` replacing `TASTrainerNotImplemented`.
4. Fill architecture fields in `configs/benchmark/ms_tcn.yaml`.
5. Wire `experiments/runner.py` to load config → build sequences → train → evaluate.

The frozen LSTM modules (`lstm_trainer.py`, `lstm_classifier.py`) must **not** be modified.

---

## 4. Evaluation contract

Learned segmenters are evaluated on the **seven-class ontology** (`seven_phase_v1`) using canonical segment and boundary metrics.

The five-phase knee-angle mapping (`seven_to_five_knee_angle_v1`) remains available for **exploratory B0 analysis only** and is disabled by default in `ms_tcn.yaml` (`use_b0_mapping: false`).

---

## 5. Configuration

| File | Purpose |
|------|---------|
| `configs/benchmark.yaml` | Manifest; `learned_models.ms_tcn` entry |
| `configs/benchmark/ms_tcn.yaml` | Per-model hyperparameters (stub) |
| `configs/reproduction.yaml` | Snapshot paths (read-only) |

---

## 6. Tests

| Test file | Coverage |
|-----------|----------|
| `tests/test_frame_labels.py` | Label store |
| `tests/test_frame_sequence.py` | Synthetic sequence builder |
| `tests/test_benchmark_registry.py` | Manifest registration |
| `tests/test_tas_hooks.py` | Evaluation payload + metrics hook |

Integration tests against the full snapshot run only when paths are available locally.
