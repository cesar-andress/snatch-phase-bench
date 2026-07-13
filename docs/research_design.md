# Research design

## Scientific goals

SnatchPhaseBench reframes an MSc thesis proof-of-concept as a **reproducible dataset and benchmark** for temporal phase segmentation of the Olympic snatch from markerless pose sequences.

**Authoritative scientific reference:** [`SnatchPhaseBench_Literature_Foundation.md`](../../SnatchPhaseBench_Literature_Foundation.md)

**Honest positioning (literature Part 1.2):**

SnatchPhaseBench is a *fine-grained, single-actor, short-horizon temporal action segmentation benchmark on skeleton input* in a sports-biomechanics domain—not a new architecture paper.

Core question:

> Where do learned temporal segmenters improve over the knee-angle heuristic the biomechanics community already uses?

## Dataset (canonical construction)

**Full author clarifications:** [`reproduction/AUTHOR_CLARIFICATIONS.md`](reproduction/AUTHOR_CLARIFICATIONS.md)

The table below separates what is grounded in published literature, what was decided during dataset construction, and what was confirmed after reproduction began.

| Topic | Published literature | Dataset construction (author) | Post-reproduction clarification |
|-------|---------------------|------------------------------|--------------------------------|
| Phase count | Coaching: 3–4 pulls; CV: six phases (Cao et al., 2022); five-phase knee-angle model (Thiele et al., 2024) | Seven labels = six CV phases + Setup | Mapping to five-phase B0 ontology documented; labels released as-is |
| Phase names | M1–M6 barbell/joint events (Cao et al., 2022) | Setup, First Pull, Transition, Second Pull, Turnover, Catch, Recovery | Turnover/Catch split intentional |
| Boundaries | Knee-angle and bar-velocity events in biomechanics | Frame-by-frame visual biomechanical events | Recovery ends at full hip/knee extension with bar stable overhead |
| Annotations | IAA recommended in sports labelling | Single expert; consistency across athletes | IAA deferred to future work |
| Frame labels | — | Corrected `master_frame_labels.csv` | 35,825 rows canonical (37,125 export had duplicates/errors) |
| Videos | Competition snatch kinematics literature | 208 clips from Weightlifting House YouTube; manual trim | Redistribution rights under evaluation |
| Pose | MediaPipe widely used in sports CV | MediaPipe **0.10.30**, **Full** model | Fixed Stage-1 input for benchmark v1 |

**Verified benchmark facts (unchanged):** 208 videos, 70 athletes, 35,825 frame labels, 21,249 training windows, frozen LSTM baseline (B1-repro-v1), corrected canonical dataset.

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

This LSTM is **benchmark tier B1** — verified historical reference. Primary learned comparators are **B2** TAS models; primary heuristic comparator is **B0**. See [`benchmark/BENCHMARK_PROTOCOL.md`](benchmark/BENCHMARK_PROTOCOL.md).

## Benchmark strategy (post-checkpoint)

**Canonical specification:** [`benchmark/BENCHMARK_PROTOCOL.md`](benchmark/BENCHMARK_PROTOCOL.md)

### Tier hierarchy (Phase 3)

- **B0** Rule-based knee-angle threshold segmenter
- **B1** Frozen thesis LSTM (**verified**)
- **B2** MS-TCN, MS-TCN++, ASFormer (+ optional DiffAct, encoders)
- **B3** Foundation-model representations (optional)

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
| Phase ontology: 7 thesis labels vs 5-phase biomechanics standard | [`literature/GAP_ANALYSIS.md`](literature/GAP_ANALYSIS.md) §5.1; [`reproduction/AUTHOR_CLARIFICATIONS.md`](reproduction/AUTHOR_CLARIFICATIONS.md) |
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
| Single annotator / no IAA | Documented in [`reproduction/AUTHOR_CLARIFICATIONS.md`](reproduction/AUTHOR_CLARIFICATIONS.md); IAA planned |
| No public video license | Videos absent from snapshot |
| Window metrics ≠ segment quality | Baseline protocol is window classification |
| Class imbalance | `transition` smallest class |
| Pose upper-limb weakness at catch | Literature + limitation; not quantified locally |
| Metric saturation risk | Long phases dominate frame accuracy |

## Gates before benchmark implementation

1. ~~**Original `best_model.pt` must evaluate to thesis metrics**~~ — **DONE**
2. **Phase 3 benchmark design reviewed** — **DONE** ([`benchmark/BENCHMARK_PROTOCOL.md`](benchmark/BENCHMARK_PROTOCOL.md))
3. **Phase ontology reconciliation** with biomechanics standard — **DOCUMENTED** ([`reproduction/AUTHOR_CLARIFICATIONS.md`](reproduction/AUTHOR_CLARIFICATIONS.md); B0 mapping still implementation work)
4. **B0 + boundary metrics** before claiming benchmark completeness — **OPEN**

## Related documents

- [`literature/GAP_ANALYSIS.md`](literature/GAP_ANALYSIS.md)
- [`paper/REVIEWER_CHECKLIST.md`](paper/REVIEWER_CHECKLIST.md)
- [`paper/PAPER_TODO.md`](paper/PAPER_TODO.md)
- [`reproduction/AUTHOR_CLARIFICATIONS.md`](reproduction/AUTHOR_CLARIFICATIONS.md)
- [`reproduction/REPRODUCTION_SUMMARY.md`](reproduction/REPRODUCTION_SUMMARY.md)
