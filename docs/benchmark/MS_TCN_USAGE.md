# MS-TCN usage guide (SnatchPhaseBench)

**Design reference:** [`MS_TCN_DESIGN.md`](MS_TCN_DESIGN.md)  
**Config:** `configs/benchmark/ms_tcn.yaml`

---

## Installation

From the repository root with Python ≥ 3.11:

```bash
pip install -e ".[dev]"
```

Optional for TensorBoard logging during training:

```bash
pip install tensorboard
```

---

## Expected inputs

| Input | Source | Shape / format |
|-------|--------|----------------|
| Pose features | `keypoints/<athlete>/*.csv` | Per-frame 33×(x,y,z) = 99 dims |
| Frame labels | `master_frame_labels.csv` | `phase_id` 0–7 per frame |
| Split | `athlete_split.json` | Athlete-disjoint train/val/test |

The frame-sequence adapter aligns labels and keypoints on `(video_relpath, frame)`.

---

## Training

```bash
python scripts/train_ms_tcn.py --config configs/benchmark/ms_tcn.yaml --seed 42
```

Resume from the last epoch:

```bash
python scripts/train_ms_tcn.py --config configs/benchmark/ms_tcn.yaml --seed 42 --resume
```

**Outputs** (under `outputs/benchmark/ms_tcn/seed42/`):

| File | Description |
|------|-------------|
| `best_model.pt` | Best validation checkpoint |
| `checkpoint_last.pt` | Resume state (optimizer + epoch) |
| `feature_mean.npy`, `feature_std.npy` | Train-only standardization |
| `history.json` | Per-epoch train/val metrics |
| `tensorboard/` | Optional TB logs |

---

## Inference

Python API:

```python
from snatch_phase_bench.models.ms_tcn.inference import load_ms_tcn_from_checkpoint, predict_videos
from snatch_phase_bench.training.ms_tcn_trainer import MSTCNTrainer

model, _ = load_ms_tcn_from_checkpoint("outputs/benchmark/ms_tcn/seed42/best_model.pt")
mean, std = MSTCNTrainer.load_standardization("outputs/benchmark/ms_tcn/seed42")
preds = predict_videos(records, model=model, mean=mean, std=std)
```

Single video:

```python
trainer = MSTCNTrainer()
pred = trainer.predict_video(record.features, model=model, device=device, mean=mean, std=std)
```

---

## Benchmark evaluation

Uses the **canonical evaluator** (`evaluation/tas_hooks.py`) — no MS-TCN-specific metrics.

```bash
python scripts/eval_ms_tcn.py \
  --checkpoint outputs/benchmark/ms_tcn/seed42/best_model.pt \
  --split test \
  --output outputs/benchmark/ms_tcn/seed42/eval_test.json
```

Produces `BenchmarkEvaluationResult` JSON with segment and boundary metrics.

---

## Hyperparameters

All values are documented in [`MS_TCN_DESIGN.md`](MS_TCN_DESIGN.md) with paper citations and SnatchPhaseBench deviations.

Core architecture (paper defaults): 4 stages, 10 layers/stage, 64 feature maps, kernel 3, Adam lr=0.0005, λ=0.15, τ=4.

---

## Known limitations

| Limitation | Notes |
|------------|-------|
| Variable-length batching | Default `batch_size=1`; padding batches not yet optimized |
| Unlabeled frames | `phase_id=0` ignored in CE loss |
| No native FPS in ms metrics | Boundary ms requires explicit per-video FPS (benchmark policy) |
| Dropout rate | Not stated in CVPR 2019 paper; config uses author-release default 0.5 |
| Full benchmark runs | M2 delivers implementation only; multi-seed test evaluation is a separate milestone |

---

## Tests

```bash
pytest tests/test_ms_tcn_model.py tests/test_ms_tcn_loss.py tests/test_ms_tcn_trainer_smoke.py -q
```

Synthetic CI dataset is generated in `test_ms_tcn_trainer_smoke.py` (no snapshot required).
