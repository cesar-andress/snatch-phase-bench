# Research Design

## Scientific goals

SnatchPhaseBench aims to transform an MSc thesis proof-of-concept into a **reproducible dataset and benchmark** for temporal phase segmentation of the Olympic snatch from markerless pose sequences.

Primary contributions (planned):

1. Curated pose sequences with phase annotations.
2. Rigorous athlete-level evaluation protocol.
3. Segment-level metrics beyond overlapping window classification.
4. Comparable baselines (LSTM → modern temporal models).

## Current baseline (frozen)

| Item | Status |
|------|--------|
| Model | Single-layer LSTM, hidden 128, dropout 0.2 |
| Input | 31-frame windows, stride 1, 99-D MediaPipe x/y/z |
| Split | 49 / 10 / 11 athletes |
| Metrics | Window-level accuracy / macro-F1 |
| Dataset rebuild | **Verified exact** (manifest SHA-256 match) |
| Checkpoint eval | **Pending** (`best_model.pt` LFS pointer) |
| Retrain proxy | ~0.944 accuracy, ~0.899 macro-F1 (CPU) |

See `docs/reproduction/REPRODUCTION_SUMMARY.md` — **conclusions are frozen**.

## Future benchmark strategy

### Phase 3 (after checkpoint validation)

1. Validate exact checkpoint metrics.
2. Implement trivial baselines (majority, persistence).
3. Add GRU, TCN, MS-TCN++, ST-GCN, lightweight Transformer.
4. Report window + frame + segment metrics with athlete CV.

### Evaluation upgrades

- Frame-level aggregation to reduce overlap bias.
- Segmental F1@10/25/50 and edit score (implemented, not yet in baseline).
- Statistical comparison across folds.

### Ablations (later)

- x,y vs x,y,z; normalization; window size; stride; noise robustness.

## Reproducibility policy

- Read-only student snapshot — never modified.
- All development in this repository only.
- Pinned dependencies in `requirements-reproduction.txt`.
- Deterministic seeds; YAML configs; structured reports under `docs/reproduction/`.
- Large artifacts gitignored; Zenodo for public release (pending legal review).

## Limitations (verified or inferred)

| Limitation | Evidence |
|------------|----------|
| Window overlap (stride 1) | 96.77% frame sharing; ~36.6× autocorrelation ratio |
| Single annotator | Not documented in repository |
| No public video license | Videos absent from snapshot |
| Window metrics ≠ segment quality | Baseline protocol is window classification |
| Class imbalance | `transition` smallest class |

## Gate before benchmark development

**Original `best_model.pt` must evaluate to thesis metrics** before implementing new models or changing baseline conclusions.
