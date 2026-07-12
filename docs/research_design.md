# Research design

## Scientific goals

SnatchPhaseBench reframes an MSc thesis proof-of-concept as a **reproducible dataset and benchmark** for temporal phase segmentation of the Olympic snatch from markerless pose sequences.

**Authoritative scientific reference:** [`SnatchPhaseBench_Literature_Foundation.md`](../../SnatchPhaseBench_Literature_Foundation.md)

**Honest positioning (literature Part 1.2):**

SnatchPhaseBench is a *fine-grained, single-actor, short-horizon temporal action segmentation benchmark on skeleton input* in a sports-biomechanics domain—not a new architecture paper.

Core question:

> Where do learned temporal segmenters improve over the knee-angle heuristic the biomechanics community already uses?

## Intended contributions (ranked)

| Rank | Contribution | Status |
|------|--------------|--------|
| 1 | Curated dataset (208 videos, 70 athletes, phase labels, keypoints) | Verified structure; public release pending |
| 2 | Reproducible benchmark protocol (splits, preprocessing, metrics, code) | Infrastructure ready; baselines incomplete |
| 3 | Domain formalization (short-horizon TAS + boundary-ms evaluation) | Planned; boundary metrics TODO |
| 4 | Software artifact | Active development |
| 5 | Novel model | **Not claimed** |

See [`release/PUBLICATION_STRATEGY.md`](release/PUBLICATION_STRATEGY.md) for venue alignment.

## Seven-field research map

```text
[1] Pose estimation          → MediaPipe keypoints (fixed for benchmark v1)
[2] Markerless validity      → justifies skeleton input; B0 heuristic threat
[3] Skeleton encoders        → optional CTR-GCN / PoseC3D (Tier 1)
[4] Temporal segmentation    → MS-TCN, ASFormer (Tier 0 benchmark)
[5–6] Sports analytics / biomechanics → evaluation stakes, phase ontology
[7] Weightlifting prior art  → gap vs barbell-tracking & validation studies
```

Do not blur stages 1–3 (literature Part 4.2). See [`project_architecture.md`](project_architecture.md).

## Current baseline (frozen — thesis reproduction)

| Item | Status |
|------|--------|
| Model | Single-layer LSTM, hidden 128, dropout 0.2 |
| Input | 31-frame windows, stride 1, 99-D MediaPipe x/y/z |
| Split | 49 / 10 / 11 athletes |
| Metrics | Window-level accuracy / macro-F1 |
| Dataset rebuild | **Verified exact** (manifest SHA-256 match) |
| Checkpoint eval | **Verified exact** (2026-07-13; see [`CHECKPOINT_VALIDATION.md`](reproduction/CHECKPOINT_VALIDATION.md)) |
| Retrain proxy | ~0.944 accuracy, ~0.899 macro-F1 (CPU) |

This LSTM is the **historical thesis baseline**, not the literature-recommended benchmark tier (B0–B3). See [`FROZEN_BASELINE.md`](FROZEN_BASELINE.md) and [`benchmark/BENCHMARK_PLAN.md`](benchmark/BENCHMARK_PLAN.md).

## Benchmark strategy (post-checkpoint)

Full plan: [`benchmark/BENCHMARK_PLAN.md`](benchmark/BENCHMARK_PLAN.md)

### Tier 0 (essential)

- **B0** Rule-based knee-angle threshold segmenter
- **B1–B3** MS-TCN, MS-TCN++, ASFormer on raw normalized keypoints

### Tier 1 (recommended)

- DiffAct; CTR-GCN and PoseC3D encoders → TAS head

### Evaluation priority

1. Boundary MAE (ms) per phase transition
2. Segmental F1@10/25/50 and edit score
3. Frame accuracy
4. Window-level metrics (thesis compatibility only)

Definitions: [`evaluation_metrics.md`](evaluation_metrics.md)

### Splits

- Primary: fixed 49/10/11 athlete holdout (verified)
- Required extension: grouped leave-one-athlete-out for uncertainty

## Known scientific gaps (from literature integration)

| Gap | Document |
|-----|----------|
| Phase ontology: 7 thesis labels vs 5-phase biomechanics standard | [`literature/GAP_ANALYSIS.md`](literature/GAP_ANALYSIS.md) §5.1 |
| No rule-based B0 baseline | [`paper/REVIEWER_CHECKLIST.md`](paper/REVIEWER_CHECKLIST.md) #1 |
| Boundary-ms metrics not implemented | `evaluation/metrics/boundary.py` |
| Prior-art table for weightlifting CV | [`paper/PAPER_TODO.md`](paper/PAPER_TODO.md) LIT-06 |

## Reproducibility policy

- Read-only student snapshot — never modified
- All development in this repository only
- Pinned dependencies in `requirements-reproduction.txt`
- Deterministic seeds; YAML configs; reports under `docs/reproduction/`
- Synchronization process: [`SCIENTIFIC_WORKFLOW.md`](SCIENTIFIC_WORKFLOW.md)

## Limitations (verified or documented)

| Limitation | Evidence |
|------------|----------|
| Window overlap (stride 1) | 96.77% frame sharing; autocorrelation analysis |
| Single annotator / no IAA | Not documented in repository |
| No public video license | Videos absent from snapshot |
| Window metrics ≠ segment quality | Baseline protocol is window classification |
| Class imbalance | `transition` smallest class |
| Pose upper-limb weakness at catch | Literature + limitation; not quantified locally |
| Metric saturation risk | Long phases dominate frame accuracy |

## Gates before benchmark development

1. **Original `best_model.pt` must evaluate to thesis metrics** (`FROZEN_BASELINE.md`)
2. **Phase ontology reconciliation** with biomechanics standard
3. **B0 implementation** before claiming benchmark completeness

## Related documents

- [`literature/GAP_ANALYSIS.md`](literature/GAP_ANALYSIS.md)
- [`paper/REVIEWER_CHECKLIST.md`](paper/REVIEWER_CHECKLIST.md)
- [`paper/PAPER_TODO.md`](paper/PAPER_TODO.md)
- [`reproduction/REPRODUCTION_SUMMARY.md`](reproduction/REPRODUCTION_SUMMARY.md)
